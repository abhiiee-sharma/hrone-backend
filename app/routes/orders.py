"""
Order Management API

This module provides endpoints for creating and retrieving customer orders in an e-commerce system.
It handles order creation and retrieval with product details enrichment.

Endpoints:
1. POST /orders
   - Creates a new order in the database
   - Request Body: Order model containing userId and items (productId + quantity)
   - Returns: MongoDB inserted ID of the new order

2. GET /orders/{user_id}
   - Retrieves paginated order history for a specific user
   - Parameters:
     - user_id: Path parameter for the user's ID
     - limit: Query parameter for pagination limit (default: 10)
     - offset: Query parameter for pagination offset (default: 0)
   - Returns: 
     - List of orders with enriched product details
     - Calculated total price for each order
     - Pagination metadata

Data Flow:
- Orders are stored in MongoDB with references to products
- When retrieving orders, product details are looked up from the products collection
- Order totals are calculated dynamically based on current product prices

Dependencies:
- Requires MongoDB collections: 'order_collection' and 'product_collection'
- Uses Pydantic's Order model for request validation

Error Handling:
- FastAPI's default error handling for:
  - Invalid ObjectId formats
  - Database connection issues
  - Validation errors on request data

Example Usage:
- POST /orders { "userId": "123", "items": [{"productId": "abc", "qty": 2}] }
- GET /orders/123?limit=5&offset=0
"""
from fastapi import APIRouter
from app.models.order_model import Order
from app.db.database import order_collection
from fastapi import Path, Query
from typing import Optional
from app.db.database import product_collection
from bson import ObjectId


router = APIRouter()

@router.post("/orders", status_code=201)
async def create_order(order: Order):
    order_dict = order.dict()
    result = await order_collection.insert_one(order_dict)
    return {"id": str(result.inserted_id)}

@router.get("/orders/{user_id}", status_code=200)
async def get_orders(
    user_id: str = Path(...),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):

    query = { "userId": user_id }
    cursor = order_collection.find(query).skip(offset).limit(limit)
    results = []

    async for order in cursor:
        items = []
        total = 0

        for item in order["items"]:
            product = await product_collection.find_one({ "_id": ObjectId(item["productId"]) })

            product_details = {
                "id": str(product["_id"]),
                "name": product["name"]
            } if product else {}

            items.append({
                "productDetails": product_details,
                "qty": item["qty"]
            })

            if product:
                total += item["qty"] * product["price"]

        results.append({
            "id": str(order["_id"]),
            "items": items,
            "total": round(total, 2)
        })

    response = {
        "data": results,
        "page": {
            "next": offset + limit,
            "limit": len(results),
            "previous": offset - limit if offset - limit >= 0 else 0
        }
    }

    return response
