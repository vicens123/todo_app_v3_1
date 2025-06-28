from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from schema import ToDoRequest, ToDoResponse
from database import SessionLocal
import crud

# LangChain (actualizado con imports modernos)
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

langchain_llm = OpenAI(temperature=0)

# Summarize template
summarize_template_string = """
    Provide a summary for the following text:
    {text}
"""

summarize_prompt = PromptTemplate(
    template=summarize_template_string,
    input_variables=['text'],
)

summarize_chain = LLMChain(
    llm=langchain_llm,
    prompt=summarize_prompt,
)

# Poem template
write_poem_template_string = """
    Write a short poem with the following text:
    {text}
"""

write_poem_prompt = PromptTemplate(
    template=write_poem_template_string,
    input_variables=['text'],
)

write_poem_chain = LLMChain(
    llm=langchain_llm,
    prompt=write_poem_prompt,
)

router = APIRouter()

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD Endpoints
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

# ✅ Endpoint para resumen
class TextRequest(BaseModel):
    text: str

@router.post("/summarize-text")
async def summarize_text(request: TextRequest):
    summary = summarize_chain.run(text=request.text)
    return {"summary": {"text": summary}}

# ✅ Endpoint para poema
@router.post("/write-poem/{id}")
async def write_poem_by_todo(id: int, db: Session = Depends(get_db)):
    todo = crud.read_todo(db, id)
    if todo is None:
        raise HTTPException(status_code=404, detail="to do not found")
    poem = write_poem_chain.run(text=todo.name)
    return {"poem": poem}
