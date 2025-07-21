# HRONE E-commerce API

A FastAPI-based e-commerce backend service that manages products and orders with MongoDB as the database.

## Features

- **Product Management**
  - Create new products with multiple sizes and quantities
  - List products with filtering by name and size
  - Pagination support for product listings

- **Order Management**
  - Create new orders with multiple items
  - View order history by user
  - Automatic calculation of order totals

## Tech Stack

- **Framework**: FastAPI
- **Database**: MongoDB (using Motor for async support)
- **Environment Management**: python-dotenv
- **Data Validation**: Pydantic
- **API Documentation**: Automatic OpenAPI (Swagger) documentation

## Prerequisites

- Python 3.8+
- MongoDB instance (local or cloud)
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd hron
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your MongoDB connection string:
   ```env
   MONGO_URI=mongodb://localhost:27017/hrone
   ```

## Running the Application

Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### Products

- **Create a Product**
  - `POST /products`
  - Request body should include `name`, `price`, and `sizes` array

- **List Products**
  - `GET /products`
  - Query parameters:
    - `name`: Filter by product name (case-insensitive)
    - `size`: Filter by available size
    - `limit`: Number of items per page (default: 10)
    - `offset`: Pagination offset (default: 0)

### Orders

- **Create an Order**
  - `POST /orders`
  - Request body should include `userId` and `items` array with `productId` and `qty`

- **Get User Orders**
  - `GET /orders/{user_id}`
  - Query parameters:
    - `limit`: Number of items per page (default: 10)
    - `offset`: Pagination offset (default: 0)

## Project Structure

```
hron/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application setup
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py      # Database connection and configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── product_model.py # Product data models
│   │   └── order_model.py   # Order data models
│   └── routes/
│       ├── __init__.py
│       ├── products.py      # Product-related endpoints
│       └── orders.py        # Order-related endpoints
├── .env.example            # Example environment variables
├── requirements.txt         # Project dependencies
└── README.md               # This file
```

## Environment Variables

- `MONGO_URI`: MongoDB connection string (default: `mongodb://localhost:27017/hrone`)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
