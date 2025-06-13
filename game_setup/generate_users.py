from google import genai
import os
from PIL import Image
from io import BytesIO
from typing import List, Dict, Any
import logging
from pathlib import Path
from config import USERS_CONFIGS, GEN_USER_PROMPT
import json
import random
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_product_database() -> Dict[str, Any]:
    """Load the product database to get available types and product IDs"""
    try:
        with open("product_database.json", "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading product database: {str(e)}")
        raise

def generate_users(user_id: str, name: str, description: str, prompt: str) -> List[str]:
    """Generate user images and return their paths"""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")

    try:
        client = genai.Client(api_key=api_key)
        
        result = client.models.generate_images(
            model="models/imagen-3.0-generate-002",
            prompt=prompt,
            config=dict(
                number_of_images=1,
                output_mime_type="image/jpeg",
                person_generation="ALLOW_ADULT",
                aspect_ratio="1:1",
            ),
        )

        if not result.generated_images:
            logger.warning("No images were generated")
            return []

        if len(result.generated_images) != 1:
            logger.warning(f"Expected 1 image, but got {len(result.generated_images)}")

        # Create images directory if it doesn't exist
        images_dir = Path("images/users")
        images_dir.mkdir(exist_ok=True)

        saved_image_paths = []
        for i, generated_image in enumerate(result.generated_images):
            try:
                image = Image.open(BytesIO(generated_image.image.image_bytes))
                # Add index to filename to prevent overwriting
                filename = f"{user_id}_{name}_V{i+1}.jpg".replace(" ", "-")
                filepath = images_dir / filename
                image.save(filepath)
                saved_image_paths.append(str(filepath))
                logger.info(f"Saved image to {filepath}")
            except Exception as e:
                logger.error(f"Error saving image {i+1}: {str(e)}")

        return saved_image_paths

    except Exception as e:
        logger.error(f"Error generating images: {str(e)}")
        raise

def generate_user_data(
        user_id: str, 
         name: str, 
         description: str, 
         image_path: str, 
         product_db: Dict[str, Any]) -> Dict[str, Any]:
    """Generate user data with the specified schema"""
    
    # Get available product types from metadata
    product_types = list(product_db["metadata"]["types"].keys())
    
    # Generate style preferences (1-3 random types)
    num_preferences = random.randint(1, 3)
    style_preferences = random.sample(product_types, num_preferences)
    
    # Generate purchase history (3-10 random product IDs)
    num_purchases = random.randint(3, 10)
    purchase_history = random.sample([p["id"] for p in product_db["products"]], num_purchases)
    
    # Generate cart status
    num_cart_items = random.randint(1, 5)
    cart_items = random.sample(product_db["products"], num_cart_items)
    cart_status = {
        "items": [
            {
                "product_id": item["id"],
                "quantity": random.randint(1, 2),
                "added_at": (datetime.now() - timedelta(days=random.randint(0, 7))).isoformat()
            }
            for item in cart_items
        ],
        "total_items": num_cart_items,
        "total_price": sum(item["price"] * random.randint(1, 2) for item in cart_items)
    }
    
    return {
        "id": user_id,
        "name": name,
        "description": description,
        "style_preferences": style_preferences,
        "image_url": image_path,
        "purchase_history": purchase_history,
        "cart_status": cart_status,
        "created_at": datetime.now().isoformat()
    }

def generate_users_database() -> Dict[str, Any]:
    """Generate the complete users database"""
    try:
        # Load product database
        product_db = load_product_database()
        
        # Create images directory if it doesn't exist
        os.makedirs("images/users", exist_ok=True)
        
        users = []
        # Iterate through all User configurations
        for user_id, config in USERS_CONFIGS.items():
            logger.info(f"\nGenerating data for {user_id}...")
            name = config["name"]
            description = config["description"]
            prompt = GEN_USER_PROMPT(description)
            
            # Generate images
            image_paths = generate_users(user_id, name, description, prompt)
            if not image_paths:
                logger.warning(f"No images generated for {user_id}, skipping...")
                continue
                
            # Generate user data
            user_data = generate_user_data(user_id, name, description, image_paths[0], product_db)
            users.append(user_data)
            logger.info(f"Completed generating data for {user_id}")
        
        # Create database with metadata
        database = {
            "users": users,
            "metadata": {
                "total_users": len(users),
                "generated_at": datetime.now().isoformat(),
                "stats": {
                    "total_purchases": sum(len(u["purchase_history"]) for u in users),
                    "total_cart_items": sum(u["cart_status"]["total_items"] for u in users),
                    "total_cart_value": sum(u["cart_status"]["total_price"] for u in users)
                }
            }
        }
        
        # Save to file
        output_path = Path("users_database.json")
        with open(output_path, "w") as f:
            json.dump(database, f, indent=2)
        
        logger.info(f"Successfully generated users database with {len(users)} users")
        logger.info(f"Database saved to {output_path}")
        
        return database
        
    except Exception as e:
        logger.error(f"Error generating users database: {str(e)}")
        raise

if __name__ == "__main__":
    generate_users_database()
