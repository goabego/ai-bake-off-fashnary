from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from enum import Enum
from product_utils import format_product_display
from collections import defaultdict
from datetime import datetime

app = FastAPI(
    title="Fashnary API",
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

def load_products(db_path: str = "../db/product_database.json", data_field: str = "products"):
    try:
        with open(db_path, "r") as f:
            data = json.load(f)
            return data[data_field]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading products: {str(e)}")

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
async def list_products_stockouts():
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

@app.get("/metadata", response_model=Metadata)
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