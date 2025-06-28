from sqlalchemy.orm import Session
import models, schema

def create_todo(db: Session, todo: schema.ToDoRequest):
    db_todo = models.Todo(name=todo.name, completed=todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def read_todos(db: Session, completed: bool = None):
    if completed is None:
        return db.query(models.Todo).all()
    else:
        return db.query(models.Todo).filter(models.Todo.completed == completed).all()

def read_todo(db: Session, id: int):
    return db.query(models.Todo).filter(models.Todo.id == id).first()

def update_todo(db: Session, id: int, todo: schema.ToDoRequest):
    db_todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    if db_todo is None:
        return None
    db_todo.name = todo.name
    db_todo.completed = todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, id: int):
    db_todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    if db_todo is None:
        return None
    db.delete(db_todo)
    db.commit()
    return True
