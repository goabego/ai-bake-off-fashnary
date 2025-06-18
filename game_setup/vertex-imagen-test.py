"""
Tutorial: Using Google's Vertex AI Imagen for Image Generation and Editing
This script demonstrates how to use Google's Vertex AI Imagen service to generate
and edit images using AI.
"""

# Import required libraries
import requests
from google.oauth2 import service_account
from google import genai
from google.genai import types
from google.genai.types import (
    Image,
    RawReferenceImage,
    MaskReferenceImage
)

def setup_vertex_client():
    """Initialize and return a Vertex AI client with proper credentials."""
    credentials = service_account.Credentials.from_service_account_file(
        './key.json',
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    
    return genai.Client(
        vertexai=True,
        project='bake-off-hosting',
        location='us-central1',
        http_options=types.HttpOptions(api_version='v1'),
        credentials=credentials
    )

def get_image_from_url(image_url):
    """Fetch an image from a URL and return its content."""
    response = requests.get(image_url)
    if response.status_code == 200:
        return response.content
    raise Exception(f"Failed to fetch image from URL: {image_url}")

def generate_image(client, prompt, output_path):
    """Generate a new image using Imagen."""
    image = client.models.generate_images(
        model="imagen-4.0-ultra-generate-exp-05-20",
        prompt=prompt
    )
    
    image.generated_images[0].image.save(output_path)
    print(f"Generated image saved to {output_path}")

def edit_image(client, prompt, reference_image, output_path):
    """Edit an existing image using Imagen's editing capabilities."""
    # Create reference images for editing
    raw_ref = RawReferenceImage(
        reference_id=1,
        reference_image=reference_image
    )
    
    mask_ref = MaskReferenceImage(
        reference_id=2,
        config=types.MaskReferenceConfig(
            mask_mode='MASK_MODE_BACKGROUND',
            mask_dilation=0
        )
    )
    
    # Perform the image edit
    response = client.models.edit_image(
        model='imagen-3.0-capability-001',
        prompt=prompt,
        reference_images=[raw_ref, mask_ref],
        config=types.EditImageConfig(
            edit_mode='EDIT_MODE_INPAINT_INSERTION',
            number_of_images=1,
            include_rai_reason=True,
            output_mime_type='image/jpeg'
        )
    )
    
    response.generated_images[0].image.save(output_path)
    print(f"Edited image saved to {output_path}")

def main():
    # Initialize the client
    client = setup_vertex_client()
    
    # Example 1: Generate a new image
    generate_image(
        client,
        "A dog reading a newspaper",
        "./images/imagen4-dog_reading_newspaper.png"
    )
    
    # Example 2: Edit an existing image pulling in an image from the API
    image_url = "https://backend-879168005744.us-west1.run.app/images/users/user_1_Marcus-W._V1.jpg"
    image_bytes = get_image_from_url(image_url)
    reference_image = Image(image_bytes=image_bytes)
    
    edit_image(
        client,
        "Add a big Big city, Sunlight and clear sky",
        reference_image,
        "./images/imagen3-edit-existing-image.png"
    )
    
    # Example 3: Edit another image using the display api
    response = requests.get("https://backend-879168005744.us-west1.run.app/users/4/display")
    api_image = Image(image_bytes=response.json()["image"].split(",")[1])
    
    edit_image(
        client,
        "A stunning boat in the ocean",
        api_image,
        "./images/imagen-3-existing-image-display.png"
    )

if __name__ == "__main__":
    main()
