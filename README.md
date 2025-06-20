# Fashionary - AI Agent Bake Off - Google

Welcome to Fashionary! This starter code is provided to help with the AI Agent Bake Off.
You will have access to `product_database.json` and `users_database.json` which act as your mock databases.

Note: For this competition, the focus is on the Agent Developer Kit's uniqueness. Frontend design elements can be largely ignored.

## Table of Contents
- [Folder Structure](#folder-structure)
- [Mock Databases](#mock-databases)
  - [Products Database (`db/product_database.json`)](#products-database-dbproduct_databasejson)
  - [Users Database (`db/users_database.json`)](#users-database-dbusers_databasejson)
- [Features](#features)
  - [Backend (FastAPI)](#backend-fastapi)
  - [Frontend (Next.js)](#frontend-nextjs)
- [Installation](#installation)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Testing](#testing)
  - [Backend API Tests](#backend-api-tests)
  - [Docker Tests](#docker-tests)
- [API Documentation](#api-documentation)
  - [General Information](#general-information)
  - [Product Endpoints](#product-endpoints)
  - [User Endpoints](#user-endpoints)
  - [Metadata Endpoints](#metadata-endpoints)
- [Game Setup Directory (`game_setup/`)](#game-setup-directory-game_setup)


## Folder Structure

```
.
├── README.md                 # This file
├── backend/                  # FastAPI backend application
│   ├── api.py                # Main FastAPI application logic
│   ├── Dockerfile            # Dockerfile for the backend
│   ├── api_test.sh           # Script to test backend API endpoints
│   ├── product_utils.py      # Utility functions for product data
│   ├── requirements.txt      # Python dependencies (used by Docker)
│   ├── templates/            # HTML templates (e.g., for API root)
│   └── utils.py              # General utility functions for backend
├── db/                       # Contains the mock JSON databases
│   ├── product_database.json # Product data
│   └── users_database.json   # User data
├── frontend/                 # Next.js frontend application
│   ├── Dockerfile            # Dockerfile for the frontend
│   ├── package.json          # Node.js dependencies
│   └── src/                  # Frontend source code
├── game_setup/               # Scripts and resources for setting up game/database
│   ├── README.md             # Specific README for game setup utilities
│   ├── generate_products_db.py # Script to generate product_database.json
│   ├── generate_users.py     # Script to generate users_database.json
│   └── ...                   # Other utility scripts and images
├── images/                   # Static product and user images referenced by databases
│   ├── products/
│   └── users/
├── .docker-test.sh           # Script to build and run backend Docker image for testing
├── .gitignore
├── docker-compose.yml        # Docker Compose file for running services
├── poetry.lock               # Poetry lock file
├── pyproject.toml            # Poetry project configuration for backend
└── ...                       # Other configuration files and screenshots
```

## Mock Databases

The application uses JSON files in the `db/` directory as mock databases.

### Products Database (`db/product_database.json`)

This file contains product information.

**Structure:**
```json
{
  "products": [
    {
      "id": "string", // Unique identifier
      "image_path": "string", // Path to product image (relative to images/)
      "description": "string",
      "type": "string", // e.g., "t-shirt", "sweater"
      "color": "string",
      "graphic": "string",
      "variant": "string",
      "stock": "integer", // Available quantity
      "price": "float", // Product price
      "created_at": "string" // ISO 8601 timestamp
    }
    // ... more products
  ],
  "metadata": {
    "total_products": "integer",
    "types": {
      "t-shirt": "integer",
      // ... other types
    },
    "price_range": {
      "min": "float",
      "max": "float",
      "average": "float"
    },
    "stock_stats": {
      "total": "integer",
      "average": "float"
    },
    "generated_at": "string" // ISO 8601 timestamp
  }
}
```
*(Example values shown in the JSON above are placeholders; refer to the actual `db/product_database.json` for data examples.)*
The `id` field for products is a string. `image_path` is relative to the `images/` directory at the root of the project.

### Users Database (`db/users_database.json`)

This file contains user information.

**Structure:**
```json
{
  "users": [
    {
      "id": "string", // Unique identifier (e.g., "user_1")
      "name": "string",
      "description": "string",
      "style_preferences": ["string"], // List of preferred product types
      "image_url": "string", // Path to user's profile image (relative to images/)
      "purchase_history": ["string"], // List of purchased product IDs
      "cart_status": {
        "items": [
          {
            "product_id": "string",
            "quantity": "integer",
            "added_at": "string" // ISO 8601 timestamp
          }
        ],
        "total_items": "integer",
        "total_price": "float"
      },
      "created_at": "string" // ISO 8601 timestamp
    }
    // ... more users
  ],
  "metadata": {
    "total_users": "integer",
    "generated_at": "string", // ISO 8601 timestamp
    "stats": {
      "total_purchases": "integer",
      "total_cart_items": "integer",
      "total_cart_value": "float"
    }
  }
}
```
*(Example values shown in the JSON above are placeholders; refer to the actual `db/users_database.json` for data examples.)*
The `id` field for users is a string. `image_url` is relative to the `images/` directory at the root of the project. `purchase_history` contains product IDs.


## Features

### Backend (FastAPI)
- Serves product and user data from JSON files.
- Provides RESTful API endpoints for:
    - Listing all products with optional sorting (by stock, price, or creation date).
    - Retrieving products sorted by stockouts (lowest stock first).
    - Getting individual product details by ID.
    - Getting formatted product display data including base64 encoded images.
    - Listing all users.
    - Retrieving individual user details by ID.
    - Getting a user's purchase history (list of product details).
    - Getting a user's current cart status.
    - Getting a user's style preferences.
    - Retrieving formatted user display data including base64 encoded images.
    - Accessing aggregated metadata for products and users.
- Implements CORS (Cross-Origin Resource Sharing) middleware to allow requests from any origin.

![FastAPI Interactive Docs](./fast_api_screenshot.png)
*The FastAPI auto-generated interactive API documentation (Swagger UI) for Fashionary.*

### Frontend (Next.js)
- Modern, responsive product catalog user interface.
- Features category filtering for browsing products.
- Implements smooth animations and transitions for a better user experience.
- Displays real-time stock status indicators on product listings.
- Uses visually appealing product cards that include images.
- Designed to be mobile-friendly and adapt to various screen sizes.

![Fashionary Website Sample](./website-sample_screenshot.png)
*A sample of the Fashionary e-commerce website frontend UI.*


## Installation

### Prerequisites
- Python 3.8+ and [Poetry](https://python-poetry.org/docs/#installation) for the backend.
- Node.js (v18 or later recommended) and npm (or yarn) for the frontend.
- Docker (optional, for containerized deployment and running some tests).

### Backend Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/goabego/ai-bake-off-fashnary
    cd ai-bake-off-fashnary
    ```

2.  **Install dependencies using Poetry:**
    (This command should be run in the project's root directory where `pyproject.toml` is located)
    ```bash
    poetry install
    ```

3.  **Run the API server:**
    The FastAPI server can be started in a couple of ways:

    *   **From the project root directory:**
        ```bash
        poetry run uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000
        ```
    *   **Or, by first navigating to the `backend` directory:**
        ```bash
        cd backend
        poetry run uvicorn api:app --reload --host 0.0.0.0 --port 8000
        ```
    The API will then be available at `http://localhost:8000`. The `--reload` flag enables auto-reloading on code changes, useful for development.

### Frontend Setup

1.  **Navigate to the frontend directory:**
    (From the project root directory)
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Run the development server:**
    ```bash
    npm run dev
    ```
    The frontend application will be available at `http://localhost:3000`.

## Testing

This project includes scripts to help test the backend functionality.

### Backend API Tests
A shell script (`backend/api_test.sh`) is provided to test the backend API endpoints. This script uses `curl` to make requests to the running API server and `jq` (a command-line JSON processor) to validate the structure of JSON responses.

1.  **Ensure the backend server is running** (see Backend Setup instructions above).
2.  **Install `jq`:** If you don't have `jq` installed, you'll need to install it.
    -   On macOS (using Homebrew): `brew install jq`
    -   On Debian/Ubuntu: `sudo apt-get install jq`
    -   For other systems, see [jq installation instructions](https://stedolan.github.io/jq/download/).
3.  **Navigate to the `backend` directory** (from the project root):
    ```bash
    cd backend
    ```
4.  **Make the script executable (if you haven't already):**
    ```bash
    chmod +x api_test.sh
    ```
5.  **Run the test script:**
    ```bash
    ./api_test.sh
    ```
    The script will output the status (Pass/Fail) for each endpoint tested and provide a summary at the end.

### Docker Tests
A script (`.docker-test.sh`) is provided at the root of the project to build the backend Docker image and run it as a container. This can be used to test if the backend application containerizes correctly.

1.  **Ensure Docker is installed and running on your system.**
2.  **From the project root directory, make the script executable (if needed):**
    ```bash
    chmod +x .docker-test.sh
    ```
3.  **Run the Docker test script:**
    ```bash
    ./.docker-test.sh
    ```
    This script will:
    -   Build a Docker image tagged `backend:latest` using `backend/Dockerfile`.
    -   Attempt to run a container from this image. The script uses `docker run -p 8080:8080 backend:latest`. Note that the FastAPI application inside the Docker container (as defined in `backend/Dockerfile`) listens on port 8000. If you wish to access the API running inside Docker via port 8080 on your host, the `docker run` command should be `docker run -p 8080:8000 backend:latest`. The provided script might need this adjustment if direct access on host port 8080 is intended.

## API Documentation

When the backend server is running, navigating to the root URL (`http://localhost:8000/`) serves a simple HTML landing page (`backend/templates/index.html`). This page welcomes you to the Fashionary API and provides direct links to the comprehensive interactive API documentation interfaces:
-   **Swagger UI:** Available at `http://localhost:8000/docs`
-   **ReDoc:** Available at `http://localhost:8000/redoc`

These auto-generated interfaces (Swagger UI and ReDoc) offer detailed information about each API endpoint, including request parameters, expected response schemas, and often the ability to try out API calls directly from your browser. They are the primary resources for understanding how to interact with the API programmatically.

### General Information

-   **Base URL:** `http://localhost:8000` (when running locally)
-   **Response Format:** All API endpoints return JSON responses.
-   **Error Handling:** The API uses standard HTTP status codes to indicate the outcome of requests:
    -   `200 OK`: The request was successful.
    -   `400 Bad Request`: The request was malformed or contained invalid parameters (e.g., an invalid `sort_by` field).
    -   `404 Not Found`: The requested resource (e.g., a specific product or user ID) could not be found.
    -   `500 Internal Server Error`: An unexpected error occurred on the server while processing the request.

### Product Endpoints

#### `GET /products`
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

#### `GET /products/sort/stockouts`
Retrieves all products sorted by their stock level in ascending order (lowest stock first). Products with 0 stock will appear at the top of the list.
-   **Example Request:**
    ```bash
    curl http://localhost:8000/products/sort/stockouts
    ```
-   **Response:** An array of Product objects, sorted by stock.

#### `GET /products/{product_id}`
Retrieves a specific product by its unique ID. Replace `{product_id}` in the URL with the actual ID of the product.
-   **Example Request:**
    ```bash
    curl http://localhost:8000/products/a1b2c3d4-e5f6-7890-1234-567890abcdef
    ```
-   **Response:** A single Product object if found, otherwise a `404 Not Found` error.

#### `GET /products/{product_id}/display`
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

### User Endpoints

#### `GET /users`
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

#### `GET /users/{user_id}`
Retrieves a specific user by their unique ID. Replace `{user_id}` with the actual ID (e.g., "user_1").
-   **Example Request:**
    ```bash
    curl http://localhost:8000/users/user_1
    ```
-   **Response:** A single User object if found, otherwise a `404 Not Found` error.

#### `GET /users/{user_id}/display`
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

#### `GET /users/{user_id}/purchases`
Retrieves the purchase history for a specific user. The history consists of a list of full product objects that the user has purchased.
-   **Example Request:**
    ```bash
    curl http://localhost:8000/users/user_1/purchases
    ```
-   **Response:** An array of Product objects.

#### `GET /users/{user_id}/cart`
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

#### `GET /users/{user_id}/style-preferences`
Retrieves the list of style preferences for a specific user.
-   **Example Request:**
    ```bash
    curl http://localhost:8000/users/user_1/style-preferences
    ```
-   **Response:** An array of strings representing style preferences (e.g., `["t-shirt", "sweater"]`).

### Metadata Endpoints

#### `GET /metadata/products`
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

#### `GET /metadata/users`
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

## Game Setup Directory (`game_setup/`)

The `game_setup/` directory contains scripts and resources primarily intended for initializing or managing the data used by the application. This includes:

-   **Database Generation:** Scripts like `generate_products_db.py` and `generate_users.py` are responsible for creating the `product_database.json` and `users_database.json` files located in the `db/` directory. These scripts might use images from `game_setup/images/` as part of the data generation process.
-   **Image Utilities:** May include helper scripts for processing, validating, or managing the product and user images.
-   **Configuration:** Could hold configuration files or templates used by the data generation scripts.
-   **Testing Utilities:** Might also contain scripts for testing aspects of data generation or image processing, like `vertex-imagen-test.py`.

If you need to regenerate the mock databases, customize the data, or understand how the initial dataset was formed, the contents of the `game_setup/` directory (including its own `README.md`) are the place to look.

---

*If you encounter any issues getting the project set up or have questions about its functionality, please refer to the relevant sections of this README. For bake-off specific queries, contact the organizers.*