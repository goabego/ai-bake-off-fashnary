# To run this code you need to install the following dependencies:
# pip install google-genai pillow

from google import genai
import os
from PIL import Image
from io import BytesIO
from typing import List
import logging
from pathlib import Path
from config import CLOTHING_CONFIGS, ADK_CONFIGS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_images(config_name: str, graphic_tshirt_description: str, tshirt_color: str, clothing_type: str) -> List[str]:
    """
    Generate product images of clothing items with custom graphics using Google's Imagen model.
    
    Args:
        config_name (str): Name of the configuration
        graphic_tshirt_description (str): Description of the graphic design
        tshirt_color (str): Color of the clothing item
        clothing_type (str): Type of clothing item
        
    Returns:
        List[str]: List of paths to the generated images
        
    Raises:
        ValueError: If API key is not set
        Exception: For other errors during image generation or saving
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")

    try:
        client = genai.Client(api_key=api_key)
        
        result = client.models.generate_images(
            model="models/imagen-3.0-generate-002",
            prompt=f"""Product shot of a single {graphic_tshirt_description} on a {tshirt_color} {clothing_type} for e-commerce. 
            The {clothing_type} is displayed flat lay or on an invisible mannequin, wrinkle-free, with even, bright lighting. 
            The background is a solid, clean light grey or white. Focus on showcasing the {clothing_type} clearly. 
            High resolution, professional quality.
            Make the {clothing_type} in the style of high fashion.
            Do not include ANY MODELS or PEOPLE in the image.""",
            config=dict(
                number_of_images=4,
                output_mime_type="image/jpeg",
                person_generation="DONT_ALLOW",
                aspect_ratio="1:1",
            ),
        )

        if not result.generated_images:
            logger.warning("No images were generated")
            return []

        if len(result.generated_images) != 4:
            logger.warning(f"Expected 4 images, but got {len(result.generated_images)}")

        # Create images directory if it doesn't exist
        images_dir = Path("images/products")
        images_dir.mkdir(exist_ok=True)

        saved_image_paths = []
        for i, generated_image in enumerate(result.generated_images):
            try:
                image = Image.open(BytesIO(generated_image.image.image_bytes))
                # Add index to filename to prevent overwriting
                filename = f"{config_name}_{i+1}.jpg"
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

if __name__ == "__main__":
    # Create images directory if it doesn't exist
    os.makedirs("images", exist_ok=True)
    
    # Iterate through all clothing configurations
    for config_name, config in CLOTHING_CONFIGS.items():
        print(f"\nGenerating images for {config_name}...")
        graphic_tshirt_description = config["graphic"]
        tshirt_color = config["color"]
        clothing_type = config["type"]
        generate_images(config_name, graphic_tshirt_description, tshirt_color, clothing_type)
        print(f"Completed generating images for {config_name}")
