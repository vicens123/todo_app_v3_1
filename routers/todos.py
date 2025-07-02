from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from schema import ToDoRequest, ToDoResponse
from database import SessionLocal
import crud

# LangChain moderno
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

# Inicializar modelo LLM
langchain_llm = OpenAI(temperature=0)

# Prompt para resumen
summarize_prompt = PromptTemplate.from_template(
    "Provide a summary for the following text:\n{text}"
)

# Prompt para poema
write_poem_prompt = PromptTemplate.from_template(
    "Write a short poem with the following text:\n{text}"
)

# Cadena en estilo moderno
summarize_chain: RunnableSequence = summarize_prompt | langchain_llm
write_poem_chain: RunnableSequence = write_poem_prompt | langchain_llm

# FastAPI router
router = APIRouter()

# Dependencia de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints CRUD
@router.get("/todos", response_model=List[ToDoResponse])
def get_todos(completed: bool = None, db: Session = Depends(get_db)):
    return crud.read_todos(db, completed)

@router.get("/todos/{id}", response_model=ToDoResponse)
def get_todo(id: int, db: Session = Depends(get_db)):
    todo = crud.read_todo(db, id)
    if todo is None:
        raise HTTPException(status_code=404, detail="To-do no encontrado")
    return todo

@router.post("/todos", response_model=ToDoResponse)
def create(todo: ToDoRequest, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)

@router.put("/todos/{id}", response_model=ToDoResponse)
def update(id: int, todo: ToDoRequest, db: Session = Depends(get_db)):
    updated = crud.update_todo(db, id, todo)
    if updated is None:
        raise HTTPException(status_code=404, detail="To-do no encontrado")
    return updated

@router.delete("/todos/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_todo(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="To-do no encontrado")
    return {"message": "To-do eliminado"}

# Modelo de entrada para resumen
class TextRequest(BaseModel):
    text: str

# Endpoint para generar resumen
@router.post("/summarize-text")
async def summarize_text(request: TextRequest):
    summary = summarize_chain.invoke({"text": request.text})
    return {"summary": {"text": summary}}

# Endpoint para generar poema a partir de ToDo
@router.post("/write-poem/{id}")
async def write_poem_by_todo(id: int, db: Session = Depends(get_db)):
    todo = crud.read_todo(db, id)
    if todo is None:
        raise HTTPException(status_code=404, detail="To-do no encontrado")
    poem = write_poem_chain.invoke({"text": todo.name})
    return {"poem": poem}
