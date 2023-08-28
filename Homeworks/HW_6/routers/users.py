from typing import List
from fastapi import APIRouter, HTTPException
from Homeworks.HW_6.database import users, db
from Homeworks.HW_6.models import UserIn, User

router = APIRouter()


@router.get("/fake_users/{count}")
async def create_some_users(count: int):
    for i in range(1, count + 1):
        query = users.insert().values(
            name=f"user_{i}",
            surname=f"user_surname_{i}",
            email=f"mail_{i}@mail.ru",
            password=f"pwd_{i}"
        )
        await db.execute(query)
    return {"message": f'{count} fake users created'}


@router.post("/users/new", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(
        name=user.name,
        surname=user.surname,
        email=user.email,
        password=user.password
    )
    last_record_id = await db.execute(query)
    return {**user.model_dump(), "id": last_record_id}


@router.get("/users", response_model=List[User])
async def read_users():
    query = users.select()
    return await db.fetch_all(query)


@router.get("/users/user/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    user = await db.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.model_dump())
    await db.execute(query)
    return {**new_user.model_dump(), "id": user_id}


@router.delete("/users/del/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await db.execute(query)
    return {"message": "User was deleted"}
