from datetime import datetime
from random import randint
from typing import List
from fastapi import APIRouter, HTTPException
from sqlalchemy import select, desc
from Homeworks.HW_6.database import orders, db, products, users
from Homeworks.HW_6.models import Order, OrderIn

router = APIRouter()


@router.get("/fake_orders/{count}")
async def create_some_orders(count: int):
    for i in range(1, count + 1):
        query = orders.insert().values(
            user_id=randint(1, 5),
            product_id=randint(1, 5),
            date=datetime.now(),
            status="created"
        )
        await db.execute(query)
    return {"message": f'{count} fake orders created'}


@router.post("/orders/new", response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(
        user_id=order.user_id,
        product_id=order.product_id,
        date=order.date,
        status=order.status
    )
    last_record_id = await db.execute(query)
    return {**order.model_dump(), "id": last_record_id}


@router.get("/orders", response_model=List[Order])
async def read_orders():
    query = orders.select()
    return await db.fetch_all(query)


@router.get("/orders/order/{order_id}", response_model=Order)
async def get_order_by_id(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    order = await db.fetch_one(query)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/orders/{order_id}", response_model=Order)
async def update_product(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.model_dump())
    await db.execute(query)
    return {**new_order.model_dump(), "id": order_id}


@router.delete("/orders/delete/{order_id}")
async def delete_product(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    order = await db.execute(query)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted"}
