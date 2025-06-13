# E-commerce API

A FastAPI-based REST API for managing e-commerce products with sorting capabilities.

## Features

- Get all products with optional sorting
- Get products sorted by stockouts (lowest stock first)
- Get individual product details by ID
- CORS enabled for cross-origin requests

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Run the API server:
```bash
poetry run uvicorn api:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints

#### GET /products

Get all products with optional sorting.

Query Parameters:
- `sort_by` (optional): Field to sort by. Must be one of: "stock", "price", "created_at"
- `order` (optional): Sort order. Must be either "asc" or "desc". Defaults to "asc"

Example:
```bash
# Get all products
GET /products

# Get products sorted by price in descending order
GET /products?sort_by=price&order=desc
```

#### GET /products/sort/stockouts

Get all products sorted by stock level (lowest to highest). Products with 0 stock will appear first.

Example:
```bash
GET /products/sort/stockouts
```

#### GET /products/{product_id}

Get a specific product by ID.

Example:
```bash
GET /products/424db09f-4329-4f98-81e0-0aecb7fd1958
```

#### GET /products/{product_id}/display

Get a specific product by ID with formatted display data including the base64 encoded image.

Example:
```bash
GET /products/424db09f-4329-4f98-81e0-0aecb7fd1958/display
```

Response format:
```json
{
    "id": "string",
    "image": "data:image/jpeg;base64,...",
    "description": "string",
    "type": "string",
    "color": "string",
    "graphic": "string",
    "variant": "string",
    "stock": "integer",
    "price": "string",
    "created_at": "string",
    "stock_status": "string"
}
```

The image is returned as a base64 encoded string that can be directly used in an HTML img tag:
```html
<img src="data:image/jpeg;base64,..." alt="Product Image">
```

### Response Format

All endpoints return JSON responses. The product object has the following structure:

```json
{
    "id": "string",
    "image_path": "string",
    "description": "string",
    "type": "string",
    "color": "string",
    "graphic": "string",
    "variant": "string",
    "stock": "integer",
    "price": "float",
    "created_at": "string"
}
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- 200: Success
- 400: Bad Request (e.g., invalid sort field)
- 404: Product Not Found
- 500: Internal Server Error

## Development

### Project Structure

```
.
├── api.py              # FastAPI application
├── product_database.json  # Product data
├── images/            # Product images
├── pyproject.toml     # Poetry dependencies
└── README.md         # This file
```

### Dependencies

- FastAPI
- Pydantic
- Uvicorn
- Poetry (for dependency management)

## License

MIT
