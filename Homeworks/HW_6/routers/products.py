from random import randint
from typing import List
from fastapi import APIRouter, HTTPException
from Homeworks.HW_6.database import products, db
from Homeworks.HW_6.models import Product, ProductIn

router = APIRouter()


@router.get("/fake_products/{count}")
async def create_some_products(count: int):
    for i in range(1, count + 1):
        query = products.insert().values(
            product_name=f"product_{i}",
            description=f"Information about product_{i}",
            price=randint(1, 100000)
        )
        await db.execute(query)
    return {"message": f'{count} fake products created'}


@router.post("/products/new", response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(
        product_name=product.product_name,
        description=product.description,
        price=product.price
    )
    last_record_id = await db.execute(query)
    return {**product.model_dump(), "id": last_record_id}


@router.get("/products", response_model=List[Product])
async def read_products():
    query = products.select()
    return await db.fetch_all(query)


@router.get("/products/product/{product_id}", response_model=Product)
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    product = await db.fetch_one(query)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, new_product: ProductIn):
    query = products.update().where(products.c.id == product_id).values(**new_product.model_dump())
    await db.execute(query)
    return {**new_product.model_dump(), "id": product_id}


@router.delete("/products/delete/{product_id}")
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await db.execute(query)
    return {"message": "Product deleted"}


