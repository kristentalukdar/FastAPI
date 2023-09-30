from fastapi import FastAPI, Depends, HTTPException, Path, Request, Form
from typing import Annotated, Optional

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse

import models
from models import ToDos
from database import engine, SessionLocal

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class ToDoRequest(BaseModel):
    id:Optional[int]=None
    title : str = Field(min_length=3)
    description: str= Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

@app.get('/', response_class=HTMLResponse)
async def read_all_todos(request: Request, db: Session = Depends(get_db)):
    todo_list = db.query(models.ToDos).all()
    return templates.TemplateResponse('home.html', {'request': request, 'todos': todo_list})

@app.get('/add-todo', response_class=HTMLResponse)
async def add_new_todo(request:Request):
    return templates.TemplateResponse('add-todo.html', {'request': request})

@app.post('/add-todo', response_class=HTMLResponse)
async def create_todo(request: Request,
                      title: str = Form(...),
                      description: str = Form(...),
                      priority: int = Form(...),
                      db: Session = Depends(get_db) ):
    todo = models.ToDos()
    todo.title = title
    todo.description = description
    todo.priority = priority
    todo.complete = False
    db.add(todo)
    db.commit()
    return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)

@app.get('/edit-todo/{todo_id}', response_class=HTMLResponse)
async def edit_todo(request:Request, todo_id:int, db: Session = Depends(get_db)):
    todo = db.query(ToDos).filter(ToDos.id == todo_id).first()
    return templates.TemplateResponse('edit-todo.html', {'request': request, 'todo': todo})

@app.get('/register', response_class=HTMLResponse)
async def read_all_user(request:Request):
    return templates.TemplateResponse('register.html', {'request': request})

@app.post('/edit-todo/{todo_id}', response_class=HTMLResponse)
async def edit_todo_commit(request: Request,
                      todo_id:int,
                      title: str = Form(...),
                      description: str = Form(...),
                      priority: int = Form(...),
                      db: Session = Depends(get_db) ):
    todo = db.query(models.ToDos).filter(models.ToDos.id==todo_id).first()
    todo.title = title
    todo.description = description
    todo.priority = priority

    db.add(todo)
    db.commit()
    return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)

@app.get('/delete/{todo_id}')
async  def delete_todo(reqest: Request, todo_id: int, db: Session = Depends(get_db) ):
    todo= db.query(models.ToDos).filter(models.ToDos.id==todo_id).first()
    if todo is None:
        return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
    db.query(models.ToDos).filter(models.ToDos.id == todo_id).delete()
    db.commit()
    return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)


@app.get('/complete/{todo_id}')
async  def complete_todo(reqest: Request, todo_id: int, db: Session = Depends(get_db) ):
    todo= db.query(models.ToDos).filter(models.ToDos.id==todo_id).first()
    if todo is None:
        return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
    todo.complete=not todo.complete
    db.add(todo)
    db.commit()
    return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)


# @app.get('/test')
# async  def test(request:Request):
#     return templates.TemplateResponse('register.html', {'request':request})
#
# @app.get('/', status_code=status.HTTP_200_OK)
# async def read_all(db : db_dependency):
#     return db.query(ToDos).all()
#
# @app.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
# async  def read_todo(db : db_dependency, todo_id:int= Path(gt=0)):
#     todo_model= db.query(ToDos).filter(ToDos.id==todo_id).first()
#     if todo_model is not None:
#         return  todo_model
#     raise  HTTPException(status_code=404, detail='Item not Found')
#
# @app.post('/todo', status_code=status.HTTP_201_CREATED)
# async def create_todo(db:db_dependency, todo_request: ToDoRequest ):
#     todo_model= ToDos(**todo_request.model_dump())
#     db.add(todo_model)
#     db.commit()
#
# @app.put('/todo', status_code=status.HTTP_204_NO_CONTENT)
# async def update_todo(db:db_dependency, todo_request: ToDoRequest):
#     todo_model=db.query(ToDos).filter(ToDos.id == todo_request.id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404, detail='Task not Found')
#     todo_model.title=todo_request.title
#     todo_model.description= todo_request.description
#     todo_model.priority= todo_request.priority
#     todo_model.complete= todo_request.complete
#
#     db.add(todo_model)
#     db.commit()
#
# @app.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
# async def delete_todo(db:db_dependency, todo_id:int= Path(gt=0)):
#     todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()
#     if todo_model is None:
#         raise  HTTPException(status_code=404, detail='Task not Found')
#     db.query(ToDos).filter(ToDos.id == todo_id).delete()
#     db.commit()