from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from enum import Enum
from utils import format_product_display, format_user_display
from collections import defaultdict
from datetime import datetime
import os

app = FastAPI(
    title="Fashionary API",
    description="API for managing e-commerce products with sorting capabilities",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/images", StaticFiles(directory="../images"), name="images")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Landing page for the API documentation
    """
    return templates.TemplateResponse("index.html", {"request": request})

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

class Product(BaseModel):
    id: str
    image_path: str
    description: str
    type: str
    color: str
    graphic: str
    variant: str
    stock: int
    price: float
    created_at: str

class ProductDisplay(BaseModel):
    id: str
    image: str
    description: str
    type: str
    color: str
    graphic: str
    variant: str
    stock: int
    price: str
    created_at: str
    stock_status: str

class Metadata(BaseModel):
    total_products: int
    types: Dict[str, int]
    price_range: Dict[str, float]
    stock_stats: Dict[str, float]
    generated_at: str

class User(BaseModel):
    id: str
    name: str
    description: str
    style_preferences: List[str]
    image_url: str
    purchase_history: List[str]
    cart_status: Dict[str, Any]
    created_at: str

class UserMetadata(BaseModel):
    total_users: int
    generated_at: str
    stats: Dict[str, Any]

def load_products(db_path: str = "../db/product_database.json", data_field: str = "products"):
    try:
        with open(db_path, "r") as f:
            data = json.load(f)
            return data[data_field]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading products: {str(e)}")

def load_users(db_path: str = "../db/users_database.json", data_field: str = "users"):
    """Load users from the database"""
    try:
        with open(db_path, "r") as f:
            data = json.load(f)
            return data[data_field]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading users: {str(e)}")

@app.get("/products", response_model=List[Product])
async def get_products(
    sort_by: Optional[str] = None,
    order: SortOrder = SortOrder.ASC
):
    """
    Get all products with optional sorting.
    
    Parameters:
    - sort_by: Field to sort by (e.g., "stock", "price", "created_at")
    - order: Sort order ("asc" or "desc")
    
    Returns:
    - List of products sorted according to parameters
    """
    products = load_products()
    
    if sort_by:
        if sort_by not in ["stock", "price", "created_at"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid sort field. Must be one of: stock, price, created_at"
            )
        
        # Sort products
        reverse = order == SortOrder.DESC
        products.sort(key=lambda x: x[sort_by], reverse=reverse)
    
    return products

@app.get("/products/sort/stockouts", response_model=List[Product])
async def get_products_stockouts():
    """
    Get all products sorted by stock level (lowest to highest).
    Products with 0 stock will appear first.
    
    Returns:
    - List of products sorted by stock level
    """
    products = load_products()
    products.sort(key=lambda x: x["stock"])
    return products

@app.get("/products/{product_id}", response_model=Product)
async def get_product_by_id(product_id: str):
    """
    Get a specific product by ID.
    
    Parameters:
    - product_id: The unique identifier of the product
    
    Returns:
    - Product details
    """
    products = load_products()
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/products/{product_id}/display", response_model=ProductDisplay)
async def get_product_display(product_id: str):
    """
    Get a specific product by ID with formatted display data including the image.
    
    Parameters:
    - product_id: The unique identifier of the product
    
    Returns:
    - Formatted product details with base64 encoded image
    """
    products = load_products()
    for product in products:
        if product["id"] == product_id:
            formatted_product = format_product_display(product)
            if "error" in formatted_product:
                raise HTTPException(
                    status_code=500,
                    detail=formatted_product["error"]
                )
            return formatted_product
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/metadata/products", response_model=Metadata)
async def get_metadata():
    """
    Get metadata about the products including:
    - Total number of products
    - Distribution of product types
    - Price range statistics
    - Stock statistics
    - Generation timestamp
    
    Returns:
    - Product metadata statistics
    """
    try:
        # Initialize metadata
        metadata = load_products(data_field="metadata")
        print(metadata)
        
        return metadata
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating metadata: {str(e)}"
        )

@app.get("/users", response_model=List[User])
async def get_users():
    """
    Get all users.
    
    Returns:
    - List of all users
    """
    return load_users()

@app.get("/users/{user_id}", response_model=User)
async def get_user_by_id(user_id: str):
    """
    Get a specific user by ID.
    
    Parameters:
    - user_id: The unique identifier of the user
    
    Returns:
    - User details
    """
    users = load_users()
    for user in users:
        if user_id in (user["id"], user["id"].replace("user_", "")):
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/users/{user_id}/purchases", response_model=List[Product])
async def get_user_purchases(user_id: str):
    """
    Get all products purchased by a specific user.
    
    Parameters:
    - user_id: The unique identifier of the user
    
    Returns:
    - List of purchased products
    """
    users = load_users()
    user = None
    for u in users:
        if u["id"] == user_id or u["id"].replace("user_", "") == user_id:
            user = u
            break
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get product details for each purchase
    products = load_products()
    purchased_products = []
    for product_id in user["purchase_history"]:
        for product in products:
            if product["id"] == product_id:
                purchased_products.append(product)
                break
    
    return purchased_products

@app.get("/users/{user_id}/cart", response_model=Dict[str, Any])
async def get_user_cart(user_id: str):
    """
    Get the current cart status for a specific user.
    
    Parameters:
    - user_id: The unique identifier of the user
    
    Returns:
    - User's cart status
    """
    users = load_users()
    for user in users:
        if user["id"] == user_id or user["id"].replace("user_", "") == user_id:
            return user["cart_status"]
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/users/{user_id}/style-preferences", response_model=List[str])
async def get_user_style_preferences(user_id: str):
    """
    Get the style preferences for a specific user.
    
    Parameters:
    - user_id: The unique identifier of the user
    
    Returns:
    - List of user's style preferences
    """
    users = load_users()
    for user in users:
        if user["id"] == user_id or user["id"].replace("user_", "") == user_id:
            return user["style_preferences"]
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/metadata/users", response_model=UserMetadata)
async def get_users_metadata():
    """
    Get metadata about the users including:
    - Total number of users
    - Generation timestamp
    - Statistics about purchases and cart items
    
    Returns:
    - Users metadata statistics
    """
    try:
        data = load_users(data_field="metadata");
        return data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading users metadata: {str(e)}"
        )

@app.get("/users/{user_id}/display")
async def get_user_display(user_id: str):
    """
    Get a specific user by ID with formatted display data including the image.
    Parameters:
    - user_id: The unique identifier of the user
    Returns:
    - Formatted user details with base64 encoded image
    """
    users = load_users()
    for user in users:
        if user["id"] == user_id or user["id"].replace("user_", "") == user_id:
            formatted_user = format_user_display(user)
            if "error" in formatted_user:
                raise HTTPException(
                    status_code=500,
                    detail=formatted_user["error"]
                )
            return formatted_user
    raise HTTPException(status_code=404, detail="User not found")