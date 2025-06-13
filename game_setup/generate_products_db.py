import uuid
import json
from pathlib import Path
from datetime import datetime
import random
from config import CLOTHING_CONFIGS

def get_type_specific_price(clothing_type):
    """Generate a price based on the clothing type"""
    price_ranges = {
        "t-shirt": (19.99, 39.99),      # Cheapest
        "long sleeve": (29.99, 49.99),  # Mid-range
        "sweater": (49.99, 89.99),      # More expensive
        "scarf": (59.99, 129.99)        # Most expensive
    }
    
    # Get the price range for the given clothing type from the price_ranges dictionary
    # If the clothing type doesn't exist in the dictionary, use default values (29.99, 99.99)
    min_price, max_price = price_ranges.get(clothing_type, (29.99, 99.99))
    return round(random.uniform(min_price, max_price), 2)

def get_product_details(filename):
    """Extract product details from filename and configs"""
    parts = filename.split('_')
    clothing_type = parts[0]  # e.g., "longsleeve", "scarf", "sweater", "tshirt"
    design = parts[1]  # e.g., "adk", "classic", "modern"
    variant = parts[2].split('.')[0]  # e.g., "1", "2", "3", "4"
    
    # Get configuration details
    config_key = f"{clothing_type}_{design}"
    config = CLOTHING_CONFIGS.get(config_key)
    
    if not config:
        return None
    
    return {
        "type": config["type"],
        "color": config["color"],
        "graphic": config["graphic"],
        "variant": variant
    }

def generate_product_database():
    products = []
    images_dir = Path("images/products")
    
    # Process each image file
    for image_path in images_dir.glob("*.jpg"):
        # Get product details from filename and configs
        details = get_product_details(image_path.name)
        if not details:
            continue
            
        # Create product entry
        product = {
            "id": str(len(products) + 1),
            "image_path": f"images/products/{image_path.name}",
            "description": f"{details['graphic']} on a {details['color']} {details['type']} - Variant {details['variant']}",
            "type": details["type"],
            "color": details["color"],
            "graphic": details["graphic"],
            "variant": details["variant"],
            "stock": random.randint(1, 100),
            "price": get_type_specific_price(details["type"]),
            "created_at": datetime.now().isoformat()
        }
        
        products.append(product)
    
    return products

def save_database(products):
    # Create the database structure
    database = {
        "products": products,
        "metadata": {
            "total_products": len(products),
            "types": {
                "t-shirt": len([p for p in products if p["type"] == "t-shirt"]),
                "sweater": len([p for p in products if p["type"] == "sweater"]),
                "scarf": len([p for p in products if p["type"] == "scarf"]),
                "long sleeve": len([p for p in products if p["type"] == "long sleeve"])
            },
            "price_range": {
                "min": min(p["price"] for p in products),
                "max": max(p["price"] for p in products),
                "average": round(sum(p["price"] for p in products) / len(products), 2)
            },
            "stock_stats": {
                "total": sum(p["stock"] for p in products),
                "average": round(sum(p["stock"] for p in products) / len(products), 2)
            },
            "generated_at": datetime.now().isoformat()
        }
    }
    
    # Save to JSON file
    with open("product_database.json", "w") as f:
        json.dump(database, f, indent=2)
    
    print(f"Generated database with {len(products)} products")
    print(f"Price range: ${database['metadata']['price_range']['min']} - ${database['metadata']['price_range']['max']}")
    print(f"Average price: ${database['metadata']['price_range']['average']}")
    print(f"Total stock: {database['metadata']['stock_stats']['total']}")

if __name__ == "__main__":
    products = generate_product_database()
    save_database(products) 