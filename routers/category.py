from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
import json

from db.database import get_db, redis_conn
from schemas.category import Category
from services.category import CategoryService

category_router = APIRouter(prefix='/category', tags=['categories'])

# Define the time limit for data stored in Redis (in seconds)
REDIS_TIME_LIMIT = 3600  # Set to 1 hour


@category_router.get('/', response_model=List[Category])
def get_all_categories(db=Depends(get_db)) -> List[Category]:
    categories = CategoryService(db).get_categories()
    return JSONResponse(content=jsonable_encoder(categories), status_code=200)


@category_router.get('/{category_id}', response_model=Category)
def get_category_by_id(category_id: int = Path(..., ge=1),
                       db=Depends(get_db)) -> Category:
    category_key = f'category:{category_id}'
    if redis_conn.exists(category_key):
        category = redis_conn.get(category_key)
        category = jsonable_encoder(category)
    else:
        category = CategoryService(db).get_category_by_id(category_id)
        if not category:
            return JSONResponse(
                content={"message": "Category not found"}, status_code=404)
        redis_conn.set(category_key, json.dumps(jsonable_encoder(category)))
        # Set the time limit for the category key
        redis_conn.expire(category_key, REDIS_TIME_LIMIT)
    return JSONResponse(content=jsonable_encoder(category), status_code=200)


@category_router.get('/title/{category_title}', response_model=Category)
def get_category_by_title(category_title: str, db=Depends(get_db)) -> Category:
    category_key = f'category:title:{category_title}'
    if redis_conn.exists(category_key):
        category = redis_conn.get(category_key)
        category = jsonable_encoder(category)
    else:
        category = CategoryService(db).get_category_by_title(category_title)
        if not category:
            return JSONResponse(
                content={"message": "Category not found"}, status_code=404)
        redis_conn.set(category_key, json.dumps(jsonable_encoder(category)))
        # Set the time limit for the category key
        redis_conn.expire(category_key, REDIS_TIME_LIMIT)
    return JSONResponse(content=category, status_code=200)


@category_router.post('/', response_model=Category)
def create_category(category: Category, db=Depends(get_db)) -> Category:
    new_category = CategoryService(db).create_category(category)
    # Delete the "categories" key to update the data
    redis_conn.delete('categories')
    return JSONResponse(content=jsonable_encoder(
        new_category), status_code=201)


@category_router.put('/{category_id}', response_model=Category)
def update_category(category_id: int, category: Category,
                    db=Depends(get_db)) -> Category:
    updated_category = CategoryService(
        db).update_category(category_id, category)
    if not updated_category:
        return JSONResponse(
            content={"message": "Category not found"}, status_code=404)
    category_key = f'category:{category_id}'
    # Delete the key of the updated object in Redis
    redis_conn.delete(category_key)
    return JSONResponse(content=jsonable_encoder(
        updated_category), status_code=200)


@category_router.delete('/{category_id}', response_model=Category)
def delete_category(category_id: int, db=Depends(get_db)) -> Category:
    deleted_category = CategoryService(db).delete_category(category_id)
    if not deleted_category:
        return JSONResponse(
            content={"message": "Category not found"}, status_code=404)
    category_key = f'category:{category_id}'
    # Delete the key of the deleted object in Redis
    redis_conn.delete(category_key)
    return JSONResponse(content=jsonable_encoder(
        deleted_category), status_code=200)


@category_router.delete('/', response_model=int)
def delete_all_categories(db=Depends(get_db)) -> int:
    deleted_count = CategoryService(db).delete_all_categories()
    redis_conn.delete('categories')  # Delete the "categories" key in Redis
    return JSONResponse(content=deleted_count, status_code=200)
