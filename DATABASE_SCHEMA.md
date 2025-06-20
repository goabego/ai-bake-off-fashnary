# Mock Database Schemas

The application uses JSON files located in the `db/` directory as mock databases for products and users. This document outlines their structure.

## Products Database (`db/product_database.json`)

This file contains all product information, including their details, stock levels, pricing, and associated metadata.

**Root Structure:**
The JSON file has two main keys:
- `products`: An array of product objects.
- `metadata`: An object containing aggregated statistics about the products.

**Product Object Structure (within `products` array):**
Each product object has the following fields:

| Field         | Type    | Description                                                                 | Example                                   |
|---------------|---------|-----------------------------------------------------------------------------|-------------------------------------------|
| `id`          | string  | Unique identifier for the product.                                          | `"a1b2c3d4-e5f6-7890-1234-567890abcdef"` |
| `image_path`  | string  | Relative path to the product image, from the root `images/` directory.      | `"products/tshirt_classic_blue.jpg"`      |
| `description` | string  | A textual description of the product.                                       | `"Classic blue t-shirt with a minimalist design."` |
| `type`        | string  | The category or type of the product.                                        | `"t-shirt"`, `"sweater"`, `"dress"`       |
| `color`       | string  | The primary color of the product.                                           | `"blue"`, `"black"`, `"multi-color"`      |
| `graphic`     | string  | Describes any graphic or pattern on the product.                            | `"logo"`, `"striped"`, `"floral"`         |
| `variant`     | string  | Specific variant of the product, if applicable (e.g., fit, style).          | `"regular"`, `"slim_fit"`, `"vintage"`    |
| `stock`       | integer | The number of units currently available in stock.                           | `50`                                      |
| `price`       | float   | The price of the product.                                                   | `29.99`                                   |
| `created_at`  | string  | ISO 8601 timestamp indicating when the product record was created/added.    | `"2024-03-14T12:00:00Z"`                  |

**Example Product Object:**
```json
{
  "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "image_path": "products/tshirt_classic_blue.jpg",
  "description": "Classic blue t-shirt with a minimalist design.",
  "type": "t-shirt",
  "color": "blue",
  "graphic": "minimalist",
  "variant": "regular",
  "stock": 75,
  "price": 24.99,
  "created_at": "2024-03-15T10:30:00Z"
}
```

**Metadata Object Structure (`metadata` key):**
The `metadata` object provides summary statistics about the product dataset:

| Field            | Type          | Description                                                                 |
|------------------|---------------|-----------------------------------------------------------------------------|
| `total_products` | integer       | Total number of products in the database.                                   |
| `types`          | object        | Key-value pairs where keys are product types and values are their counts.   |
| `price_range`    | object        | Contains `min`, `max`, and `average` price of products.                     |
| `  min`          | float         | Minimum product price.                                                      |
| `  max`          | float         | Maximum product price.                                                      |
| `  average`      | float         | Average product price.                                                      |
| `stock_stats`    | object        | Contains `total` and `average` stock levels.                                |
| `  total`        | integer       | Total stock count across all products.                                      |
| `  average`      | float         | Average stock count per product.                                            |
| `generated_at`   | string        | ISO 8601 timestamp indicating when this metadata was generated.             |

**Example Metadata Object:**
```json
{
  "total_products": 216,
  "types": {
    "t-shirt": 84,
    "sweater": 44,
    "dress": 44,
    "longsleeve": 44
  },
  "price_range": {
    "min": 20.12,
    "max": 129.85,
    "average": 54.01
  },
  "stock_stats": {
    "total": 10656,
    "average": 49.33
  },
  "generated_at": "2024-03-14T12:00:00Z"
}
```
*Note: The `image_path` is relative to the main `images/` directory in the project root.*

## Users Database (`db/users_database.json`)

This file contains user information, including their preferences, purchase history, and cart status.

**Root Structure:**
The JSON file has two main keys:
- `users`: An array of user objects.
- `metadata`: An object containing aggregated statistics about the users.

**User Object Structure (within `users` array):**
Each user object has the following fields:

| Field               | Type    | Description                                                                   | Example                                     |
|---------------------|---------|-------------------------------------------------------------------------------|---------------------------------------------|
| `id`                | string  | Unique identifier for the user.                                               | `"user_1"`, `"user_abc"`                    |
| `name`              | string  | The name of the user.                                                         | `"Jane Doe"`                                |
| `description`       | string  | A brief description or bio of the user.                                       | `"Fashion enthusiast, loves vintage styles."` |
| `style_preferences` | array   | A list of strings indicating the user's preferred product types or styles.    | `["vintage", "dress", "sweater"]`           |
| `image_url`         | string  | Relative path to the user's profile image, from the root `images/` directory. | `"users/user_1_avatar.jpg"`                 |
| `purchase_history`  | array   | A list of product `id` strings representing items the user has purchased.     | `["prod_id_1", "prod_id_2"]`                |
| `cart_status`       | object  | An object detailing the current state of the user's shopping cart.            | (See structure below)                       |
| `created_at`        | string  | ISO 8601 timestamp indicating when the user record was created.               | `"2024-01-10T09:00:00Z"`                    |

**Cart Status Object Structure (within `cart_status`):**

| Field         | Type    | Description                                                       | Example                          |
|---------------|---------|-------------------------------------------------------------------|----------------------------------|
| `items`       | array   | A list of items currently in the cart.                            | (See structure below)            |
| `total_items` | integer | The total number of individual items (sum of quantities) in the cart. | `3`                              |
| `total_price` | float   | The total monetary value of all items in the cart.                | `120.75`                         |

**Cart Item Object Structure (within `cart_status.items` array):**

| Field        | Type    | Description                                      | Example                  |
|--------------|---------|--------------------------------------------------|--------------------------|
| `product_id` | string  | The `id` of the product in the cart.             | `"prod_id_3"`            |
| `quantity`   | integer | The number of units of this product in the cart. | `2`                      |
| `added_at`   | string  | ISO 8601 timestamp of when the item was added.   | `"2024-03-16T14:20:00Z"` |

**Example User Object:**
```json
{
  "id": "user_123",
  "name": "Alex Smith",
  "description": "Loves modern and minimalist fashion.",
  "style_preferences": ["minimalist", "t-shirt", "modern"],
  "image_url": "users/alex_smith_avatar.png",
  "purchase_history": ["a1b2c3d4", "e5f6g7h8"],
  "cart_status": {
    "items": [
      {
        "product_id": "i9j0k1l2",
        "quantity": 1,
        "added_at": "2024-03-18T10:00:00Z"
      },
      {
        "product_id": "m3n4o5p6",
        "quantity": 2,
        "added_at": "2024-03-18T11:15:00Z"
      }
    ],
    "total_items": 3,
    "total_price": 89.97
  },
  "created_at": "2023-11-05T16:45:00Z"
}
```

**Metadata Object Structure (`metadata` key):**
The `metadata` object provides summary statistics about the user dataset:

| Field          | Type   | Description                                                        |
|----------------|--------|--------------------------------------------------------------------|
| `total_users`  | integer| Total number of users in the database.                             |
| `generated_at` | string | ISO 8601 timestamp indicating when this metadata was generated.    |
| `stats`        | object | Contains aggregated statistics about user activity.                |
| `  total_purchases` | integer | Total number of items purchased across all users.             |
| `  total_cart_items`| integer | Total number of items currently in all users' carts.          |
| `  total_cart_value`| float   | Total monetary value of all items currently in all users' carts. |

**Example Metadata Object:**
```json
{
  "total_users": 50,
  "generated_at": "2024-03-14T12:00:00Z",
  "stats": {
    "total_purchases": 150,
    "total_cart_items": 75,
    "total_cart_value": 2999.50
  }
}
```
*Note: The `image_url` is relative to the main `images/` directory in the project root. `purchase_history` contains product IDs.*
