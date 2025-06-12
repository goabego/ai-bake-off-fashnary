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
        image_path = Path(f"../{product['image_path']}") # Changed double quotes to single quotes for the key
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

def format_user_display(user: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format user details for display, including image data.
    Args:
        user: User dictionary from the database
    Returns:
        Dictionary with formatted user details and base64 encoded image
    """
    try:
        # Read and encode image
        image_path = Path(f"../{user['image_url']}")
        if not image_path.exists():
            return {
                "error": "Image not found",
                "user_details": user
            }

        with Image.open(image_path) as img:
            # Convert image to RGB if it's not
            if img.mode != 'RGB':
                img = img.convert('RGB')
            # Resize image if too large (max 400px)
            max_size = 400
            if max(img.size) > max_size:
                ratio = max_size / max(img.size)
                new_size = tuple(int(dim * ratio) for dim in img.size)
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            # Convert to base64
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG", quality=85)
            img_str = base64.b64encode(buffered.getvalue()).decode()

        formatted_user = {
            "id": user["id"],
            "image": f"data:image/jpeg;base64,{img_str}",
            "name": user["name"],
            "description": user["description"],
            "style_preferences": user["style_preferences"],
            "purchase_history": user["purchase_history"],
            "cart_status": user["cart_status"],
            "created_at": user["created_at"]
        }
        return formatted_user
    except Exception as e:
        return {
            "error": f"Error processing user: {str(e)}",
            "user_details": user
        }

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os

TEXT_MODEL_NAME = "gemini-1.5-flash-latest"
# Placeholder for image generation model name, as direct Imagen access via `google-generativeai`
# with a simple model name like this is not standard. This part remains conceptual.
IMAGE_GEN_MODEL_NAME = "imagen-3"

async def generate_gemini_tryon_image(
    model_image_base64: str,
    model_image_mimetype: str,
    clothing_image_base64: str,
    clothing_image_mimetype: str
):
    try:
        if not os.getenv("GEMINI_API_KEY"):
            raise ValueError("GEMINI_API_KEY not found in environment.")

        text_model = genai.GenerativeModel(TEXT_MODEL_NAME)
        model_image_part = {"mime_type": model_image_mimetype, "data": model_image_base64}
        clothing_image_part = {"mime_type": clothing_image_mimetype, "data": clothing_image_base64}

        description_prompt_text = """
You are a meticulous photorealistic image prompt engineer.
Image 1 shows a specific person. Image 2 shows a specific clothing item.
Your critical task is to generate a highly descriptive text prompt for an AI image generation model. This prompt will be used to create a new image.
The new image MUST depict the *EXACT SAME PERSON* from Image 1. All their physical characteristics (facial features, hair, skin tone, body type, age, ethnicity) must be preserved.
This person MUST be wearing the *EXACT SAME CLOTHING ITEM* from Image 2. All details of the clothing (type, color, pattern, texture, fit, specific features like buttons or logos) must be preserved.
If the person in Image 1 has a discernible pose that is suitable for wearing the clothing in Image 2, try to maintain a similar pose.
Combine these elements into a single, coherent, descriptive sentence or a short paragraph.
Focus on visual details that an image generator can understand.
Your output MUST be ONLY the generated text prompt.
Do NOT include any surrounding text, explanations, apologies, or markdown formatting (e.g., "Prompt:", ```json, etc.).
Example of your direct output (this is just an example, your output will depend on the provided images):
"Photorealistic depiction of the young East Asian woman with long, straight black hair and brown eyes from the reference image, now wearing the exact vibrant red, oversized, knitted wool sweater with a V-neck and ribbed cuffs from the reference clothing image. She is smiling faintly and looking directly at the camera, with a neutral studio background."
        """

        prompt_parts = [model_image_part, clothing_image_part, description_prompt_text]
        print(f"Generating description with model: {TEXT_MODEL_NAME}")
        generation_config_text = genai.types.GenerationConfig(temperature=0.2)
        safety_settings_text = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        # Using synchronous generate_content as FastAPI runs it in a threadpool.
        # For a fully async app, generate_content_async would be used with await.
        response = text_model.generate_content(
            prompt_parts,
            generation_config=generation_config_text,
            safety_settings=safety_settings_text
        )
        descriptive_prompt = response.text.strip()

        if not descriptive_prompt:
            raise ValueError("Failed to generate descriptive prompt. The prompt was empty.")
        if len(descriptive_prompt) < 20:
            print(f"Warning: Generated descriptive prompt is very short: {descriptive_prompt}")
        print(f"Generated Descriptive Prompt for Image Model: {descriptive_prompt}")

        # === Placeholder for Image Generation ===
        # Actual image generation using a model like Imagen via `google-generativeai` SDK
        # is complex and might require Vertex AI SDK for full control or specific model access.
        # The user's example `ai.models.generateImages` is not a standard method in this SDK.
        # So, this part will return a placeholder (the original model image).
        print(f"Warning: Actual image generation step is a placeholder. Returning original model image.")
        generated_image_base64 = model_image_base64
        generated_image_mimetype = model_image_mimetype

        if not generated_image_base64:
            raise ValueError("Generated image data is empty (placeholder error).")

        return f"data:{generated_image_mimetype};base64,{generated_image_base64}"

    except Exception as e:
        print(f"Error in generate_gemini_tryon_image: {str(e)}")
        error_message = f"Failed to generate image: {str(e)}"
        # Add more specific error checks as in the previous attempt
        if "api key not valid" in str(e).lower():
            error_message = "Invalid Gemini API Key. Please check your configuration."
        # ... (other specific error checks) ...
        raise RuntimeError(error_message) from e