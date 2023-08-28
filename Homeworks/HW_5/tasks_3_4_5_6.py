"""
Создать API для добавления нового пользователя в базу данных. Приложение
должно иметь возможность принимать GET, POST, PUT, DELETE запросы с данными нового
пользователя и сохранять их в базу данных.
Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс User с полями id, name, email и password.
Создайте список users для хранения пользователей.
Создайте маршруты для отображения списка пользователей (метод GET),
добавления нового пользователя (метод POST), обновления информации о пользователе (метод PUT),
удаления информации о пользователе (метод DELETE).
Реализуйте валидацию данных запроса и ответа.


Создать веб-страницу для отображения списка пользователей. Приложение
должно использовать шаблонизатор Jinja для динамического формирования HTML
страницы.
Создайте HTML шаблон для отображения списка пользователей. Шаблон должен
содержать заголовок страницы, таблицу со списком пользователей и кнопку для
добавления нового пользователя.
Реализуйте вывод списка пользователей через шаблонизатор Jinja.
"""
from typing import List
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from pathlib import Path
from starlette.responses import RedirectResponse


app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


class UserIn(BaseModel):
    name: str
    email: str
    password: str


class User(UserIn):
    id: int


users = []
for i in range(5):
    users.append(User(
        id=i + 1,
        name=f'User_{i + 1}',
        email=f'user_{i + 1}@mail.ru',
        password="******"
    ))


@app.get("/")
@app.get("/users", response_class=HTMLResponse)
async def read_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.post("/users/add", response_class=HTMLResponse)
async def get_add_user_form(request: Request):
    return templates.TemplateResponse("add_user.html", {"request": request})


@app.post("/users/add/add_form", response_class=RedirectResponse, status_code=302)
async def add_form(request: Request):
    data = await request.form()
    new_user = User(
        id=len(users) + 1,
        name=data.get("name"),
        email=data.get("email"),
        password=data.get("password")
    )
    users.append(new_user)
    return "/users"


@app.get("/users/{user_id}", response_model=User)
async def get_user_by_id(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/users/update/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: User):
    for user in users:
        if user.id == user_id:
            user.name = new_user.name
            user.email = new_user.email
            user.password = new_user.password
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/delete/{user_id}", response_model=List[User])
async def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return users
    raise HTTPException(status_code=404, detail="User not found")


if __name__ == '__main__':
    uvicorn.run(
        "tasks_3_4_5_6:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
