"""
Product Management API

This module provides CRUD operations for products in an e-commerce system,
including product creation and filtered listing.

Endpoints:
1. POST /products
   - Creates a new product in the database
   - Request Body: Product model containing all product details
   - Returns: MongoDB ID of the created product
   - Status Code: 201 Created

2. GET /products
   - Retrieves paginated list of products with filtering capabilities
   - Query Parameters:
     - name: Optional string filter for product name (case-insensitive partial match)
     - size: Optional string filter for specific product size
     - limit: Pagination limit (default: 10, min: 1)
     - offset: Pagination offset (default: 0, min: 0)
   - Returns: Paginated response with product data (excluding size details)
   - Status Code: 200 OK

Data Structure:
- Products are stored with full details including:
  - name: Product name
  - price: Product price
  - sizes: Array of available sizes (filterable but not returned in listings)
  - (other fields as defined in Product model)

Filtering Logic:
- Name filter: Uses MongoDB regex for case-insensitive partial matching
- Size filter: Matches exact size value in 'sizes.size' array field
- Filters are combined with AND logic when both are provided

Pagination:
- Implements skip/limit pagination
- Returns pagination metadata including:
  - next: Next page offset
  - limit: Current page size
  - previous: Previous page offset

Security Note:
- Intentionally excludes 'sizes' array from listing responses
- No authentication in current implementation

Example Requests:
POST /products
{
    "name": "Running Shoes",
    "price": 89.99,
    "sizes": [{"size": "M", "stock": 10}]
}

GET /products?name=shoe&size=M&limit=5
"""
from fastapi import APIRouter
from app.models.product_model import Product
from app.db.database import product_collection

router = APIRouter()

@router.post("/products", status_code=201)
async def create_product(product: Product):
    product_dict = product.dict()
    result = await product_collection.insert_one(product_dict)
    return {"id": str(result.inserted_id)}

from fastapi import Query
from typing import Optional
from bson import ObjectId, regex
import re

@router.get("/products", status_code=200)
async def list_products(
    name: Optional[str] = Query(None),
    size: Optional[str] = Query(None),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    query = {}

    if name:
        query["name"] = {"$regex": re.compile(name, re.IGNORECASE)}

    if size:
        query["sizes.size"] = size

    cursor = product_collection.find(query).skip(offset).limit(limit)
    
    results = []
    async for product in cursor:
        results.append({
            "id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"]
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
