from typing import Dict, Any
from pathlib import Path
import base64
from PIL import Image
import io

def format_product_display(product: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format product details for display, including image data.
    
    Args:
        product: Product dictionary from the database
        
    Returns:
        Dictionary with formatted product details and base64 encoded image
    """
    try:
        # Read and encode image
        image_path = Path(f"../{product["image_path"]}")
        if not image_path.exists():
            return {
                "error": "Image not found",
                "product_details": product
            }
            
        with Image.open(image_path) as img:
            # Convert image to RGB if it's not
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize image if it's too large (max 800px width/height)
            max_size = 800
            if max(img.size) > max_size:
                ratio = max_size / max(img.size)
                new_size = tuple(int(dim * ratio) for dim in img.size)
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Convert to base64
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG", quality=85)
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
        # Format product details
        formatted_product = {
            "id": product["id"],
            "image": f"data:image/jpeg;base64,{img_str}",
            "description": product["description"],
            "type": product["type"].title(),
            "color": product["color"].title(),
            "graphic": product["graphic"],
            "variant": product["variant"],
            "stock": product["stock"],
            "price": f"${product['price']:.2f}",
            "created_at": product["created_at"],
            "stock_status": "Out of Stock" if product["stock"] == 0 else 
                          "Low Stock" if product["stock"] < 10 else 
                          "In Stock"
        }
        
        return formatted_product
        
    except Exception as e:
        return {
            "error": f"Error processing product: {str(e)}",
            "product_details": product
        } 