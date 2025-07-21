"""
Database connection and setup for MongoDB.

This module handles the connection to the MongoDB database using Motor,
an asynchronous driver. It loads the database URI from environment
variables, initializes the client, and prepares database collections for use
in other parts of the application.
"""

import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI not found in environment variables.")


client = AsyncIOMotorClient(MONGO_URI)
db = client.hrone
product_collection = db.products
order_collection = db.orders


async def close_connection():
    """Gracefully closes the MongoDB client connection on app shutdown."""
    await client.close()