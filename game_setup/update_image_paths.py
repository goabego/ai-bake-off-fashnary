import json
import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_image_paths():
    """
    Update image paths in product_database.json from 'images/<filename>' to 'images/products/<filename>'
    """
    try:
        # Load the product database
        db_path = Path("./product_database.json")
        with open(db_path, "r") as f:
            data = json.load(f)
        
        # Create backup of original file
        backup_path = db_path.with_suffix(".json.bak")
        with open(backup_path, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Created backup at {backup_path}")
        
        # Update image paths
        updated_count = 0
        for product in data["products"]:
            if product["image_path"].startswith("images/"):
                old_path = product["image_path"]
                filename = old_path.split("/")[-1]
                product["image_path"] = f"images/products/{filename}"
                updated_count += 1
                logger.info(f"Updated path: {old_path} -> {product['image_path']}")
        
        # Save updated database
        with open(db_path, "w") as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Successfully updated {updated_count} image paths")
        logger.info(f"Updated database saved to {db_path}")
        
    except Exception as e:
        logger.error(f"Error updating image paths: {str(e)}")
        raise

if __name__ == "__main__":
    update_image_paths() 