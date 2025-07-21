"""
E-Commerce API Main Application

This module serves as the entry point for the e-commerce API, configuring and mounting
all API routes from different domain modules.

Application Structure:
- Central FastAPI app instance
- Modular route mounting from:
  - products.py: Product management endpoints
  - orders.py: Order processing endpoints

Configuration:
- Creates base FastAPI application
- Includes routers from:
  - /app/routes/products.py
  - /app/routes/orders.py

API Documentation:
- Automatic documentation available at:
  - /docs - Interactive Swagger UI
  - /redoc - Alternative ReDoc documentation

Endpoints Summary:
1. Product Routes (/products prefix):
   - POST /products - Create new product
   - GET /products - List products with filtering

2. Order Routes (/orders prefix):
   - POST /orders - Create new order
   - GET /orders/{user_id} - Get user's order history

Environment Requirements:
- Requires MongoDB connection (configured in database.py)
- Python 3.7+ with FastAPI and Uvicorn

Example Startup:
uvicorn app.main:app --host 0.0.0.0 --port 8000

Version: 1.0.0
"""
from fastapi import FastAPI
from app.routes import products, orders

app = FastAPI()

# Mount individual route modules
app.include_router(products.router)
app.include_router(orders.router)