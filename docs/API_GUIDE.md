# Fashionary API Guide

This guide provides detailed information about the Fashionary backend API, including how to access its documentation, general principles, and specifics for each endpoint.

## Accessing Interactive API Documentation

When the backend server is running, navigating to the root URL (`http://localhost:8000/`) serves a simple HTML landing page (`backend/templates/index.html`). This page welcomes you to the Fashionary API and provides direct links to the comprehensive interactive API documentation interfaces:

-   **Swagger UI:** Available at `http://localhost:8000/docs`
-   **ReDoc:** Available at `http://localhost:8000/redoc`

These auto-generated interfaces (Swagger UI and ReDoc) offer detailed information about each API endpoint, including request parameters, expected response schemas, and often the ability to try out API calls directly from your browser. They are the primary resources for understanding how to interact with the API programmatically.

## General Information

-   **Base URL:** `http://localhost:8000` (when running locally)
-   **Response Format:** All API endpoints return JSON responses.
-   **Error Handling:** The API uses standard HTTP status codes to indicate the outcome of requests:
    -   `200 OK`: The request was successful.
    -   `400 Bad Request`: The request was malformed or contained invalid parameters (e.g., an invalid `sort_by` field).
    -   `404 Not Found`: The requested resource (e.g., a specific product or user ID) could not be found.
    -   `500 Internal Server Error`: An unexpected error occurred on the server while processing the request.

## Product Endpoints

### `GET /products`
Retrieves a list of all products. Supports optional sorting.
-   **Query Parameters:**
    -   `sort_by` (optional, string): Field to sort products by. Valid values are: `"stock"`, `"price"`, `"created_at"`.
    -   `order` (optional, string): Sort order. Valid values are: `"asc"` (ascending, default) or `"desc"` (descending).
-   **Example Requests:**
    ```bash
    # Get all products (default sorting)
    curl http://localhost:8000/products

    # Get products sorted by price in descending order
    curl "http://localhost:8000/products?sort_by=price&order=desc"
    ```
-   **Response:** An array of Product objects.
-   **Product Object Structure:**
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
      "created_at": "string" // ISO 8601 format
    }
    ```

### `GET /products/sort/stockouts`
Retrieves all products sorted by their stock level in ascending order (lowest stock first). Products with 0 stock will appear at the top of the list.
-   **Example Request:**
    ```bash
    curl http://localhost:8000/products/sort/stockouts
    ```
-   **Response:** An array of Product objects, sorted by stock.

### `GET /products/{product_id}`
Retrieves a specific product by its unique ID. Replace `{product_id}` in the URL with the actual ID of the product.
-   **Example Request:**
    ```bash
    curl http://localhost:8000/products/a1b2c3d4-e5f6-7890-1234-567890abcdef
    ```
-   **Response:** A single Product object if found, otherwise a `404 Not Found` error.

### `GET /products/{product_id}/display`
Retrieves formatted display data for a specific product by its ID, including a base64 encoded image.
-   **Example Request:**
    ```bash
    curl http://localhost:8000/products/a1b2c3d4-e5f6-7890-1234-567890abcdef/display
    ```
-   **Response (`ProductDisplay` Object):**
    ```json
    {
        "id": "string",
        "image": "string", // Base64 encoded image data (e.g., "data:image/jpeg;base64,...")
        "description": "string",
        "type": "string",
        "color": "string",
        "graphic": "string",
        "variant": "string",
        "stock": "integer",
        "price": "string", // Price formatted as a string (e.g., "$29.99")
        "created_at": "string", // ISO 8601 format
        "stock_status": "string" // e.g., "In Stock", "Low Stock", "Out of Stock"
    }
    ```
    The `image` field's value can be directly used as the `src` for an HTML `<img>` tag.

## User Endpoints

### `GET /users`
Retrieves a list of all users.
-   **Example Request:**
    ```bash
    curl http://localhost:8000/users
    ```
-   **Response:** An array of User objects.
-   **User Object Structure:**
    ```json
    {
      "id": "string", // e.g., "user_1"
      "name": "string",
      "description": "string",
      "style_preferences": ["string"], // Array of strings
      "image_url": "string",
      "purchase_history": ["string"], // Array of product IDs
      "cart_status": {
        "items": [
          {
            "product_id": "string",
            "quantity": "integer",
            "added_at": "string" // ISO 8601 format
          }
        ],
        "total_items": "integer",
        "total_price": "float"
      },
      "created_at": "string" // ISO 8601 format
    }
    ```

### `GET /users/{user_id}`
Retrieves a specific user by their unique ID. Replace `{user_id}` with the actual ID (e.g., "user_1").
-   **Example Request:**
    ```bash
    curl http://localhost:8000/users/user_1
    ```
-   **Response:** A single User object if found, otherwise a `404 Not Found` error.

### `GET /users/{user_id}/display`
Retrieves formatted display data for a specific user by ID, including a base64 encoded image.
-   **Example Request:**
    ```bash
    curl http://localhost:8000/users/user_1/display
    ```
-   **Response (`UserDisplay` Object Structure defined in `backend/api.py` and `backend/utils.py`):**
    ```json
    {
        "id": "string",
        "name": "string",
        "description": "string",
        "style_preferences": ["string"],
        "image": "string", // Base64 encoded user image data
        "purchase_history_count": "integer",
        "cart_items_count": "integer"
        // Other fields may be present based on format_user_display function
    }
    ```

### `GET /users/{user_id}/purchases`
Retrieves the purchase history for a specific user. The history consists of a list of full product objects that the user has purchased.
-   **Example Request:**
    ```bash
    curl http://localhost:8000/users/user_1/purchases
    ```
-   **Response:** An array of Product objects.

### `GET /users/{user_id}/cart`
Retrieves the current shopping cart status for a specific user.
-   **Example Request:**
    ```bash
    curl http://localhost:8000/users/user_1/cart
    ```
-   **Response (Cart Status Object):**
    ```json
    {
      "items": [
        {
          "product_id": "string",
          "quantity": "integer",
          "added_at": "string"
        }
      ],
      "total_items": "integer",
      "total_price": "float"
    }
    ```

### `GET /users/{user_id}/style-preferences`
Retrieves the list of style preferences for a specific user.
-   **Example Request:**
    ```bash
    curl http://localhost:8000/users/user_1/style-preferences
    ```
-   **Response:** An array of strings representing style preferences (e.g., `["t-shirt", "sweater"]`).

## Metadata Endpoints

### `GET /metadata/products`
Retrieves metadata about the product database.
-   **Example Request:**
    ```bash
    curl http://localhost:8000/metadata/products
    ```
-   **Response (Product Metadata Object):**
    ```json
    {
      "total_products": "integer",
      "types": { // Key-value pairs of product type and count
        "t-shirt": "integer",
        "sweater": "integer"
        // ... and other types
      },
      "price_range": {
        "min": "float",
        "max": "float",
        "average": "float"
      },
      "stock_stats": {
        "total": "integer", // Total stock of all products
        "average": "float" // Average stock per product
      },
      "generated_at": "string" // ISO 8601 timestamp of when metadata was last generated
    }
    ```

### `GET /metadata/users`
Retrieves metadata about the user database.
-   **Example Request:**
    ```bash
    curl http://localhost:8000/metadata/users
    ```
-   **Response (User Metadata Object):**
    ```json
    {
      "total_users": "integer",
      "generated_at": "string", // ISO 8601 timestamp
      "stats": {
        "total_purchases": "integer",    // Total items purchased by all users
        "total_cart_items": "integer", // Total items currently in all users' carts
        "total_cart_value": "float"    // Total monetary value of all items in all carts
      }
    }
    ```
