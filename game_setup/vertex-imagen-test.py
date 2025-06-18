from google import genai
from google.genai import types
from google.genai.types import (
    ControlReferenceConfig,
    ControlReferenceImage,
    EditImageConfig,
    Image,
    SubjectReferenceConfig,
    SubjectReferenceImage,
    RawReferenceImage,
    MaskReferenceImage
)
import os
from google.oauth2 import service_account
import requests
from PIL import Image as PILImage
from io import BytesIO

# Set the path to your key.json file
credentials = service_account.Credentials.from_service_account_file(
    './key.json',
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

client = genai.Client(
    vertexai=True,
    project='bake-off-hosting',
    location='us-central1',
    http_options=types.HttpOptions(api_version='v1'),
    credentials=credentials  # Add the credentials here
)

# TODO(developer): Update and un-comment below line
output_file = "./images/imagen-test.png"

image = client.models.generate_images(
    # model="imagen-3.0-generate-002",
    model="imagen-4.0-ultra-generate-exp-05-20",
    prompt="A dog reading a newspaper",
)

image.generated_images[0].image.save(output_file)

print(f"Created output image using {len(image.generated_images[0].image.image_bytes)} bytes")
# Example response:
# Created output image using 1234567 bytes

# Create the raw reference image using the API image
def get_image_from_url(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to fetch image from URL: {image_url}")

image_bytes = get_image_from_url("https://backend-879168005744.us-west1.run.app/images/users/user_1_Marcus-W._V1.jpg")
url_image = Image(image_bytes=image_bytes)

raw_ref_image = RawReferenceImage(
    reference_id=1,
    reference_image=url_image
)

# Model computes a mask of the background
mask_ref_image = MaskReferenceImage(
    reference_id=2,
    config=types.MaskReferenceConfig(
        mask_mode='MASK_MODE_BACKGROUND',
        mask_dilation=0,
    ),
)

response3 = client.models.edit_image(
    model='imagen-3.0-capability-001',
    prompt='Big city, Sunlight and clear sky',
    reference_images=[raw_ref_image, mask_ref_image],
    config=types.EditImageConfig(
        edit_mode='EDIT_MODE_INPAINT_INSERTION',
        number_of_images=1,
        include_rai_reason=True,
        output_mime_type='image/jpeg',
    ),
)

response3.generated_images[0].image.save("imagen-3-capability-001.png")

print(f"Created output image using {len(response3.generated_images[0].image.image_bytes)} bytes")
# Example response:
# Created output image using 1234567 bytes



# Test 2
response = requests.get("https://backend-879168005744.us-west1.run.app/users/2/display")
url_image = Image(image_bytes=response.json()["image"].split(",")[1])

raw_ref_image = RawReferenceImage(
    reference_id=1,
    reference_image=url_image
)

# Model computes a mask of the background
mask_ref_image = MaskReferenceImage(
    reference_id=2,
    config=types.MaskReferenceConfig(
        mask_mode='MASK_MODE_BACKGROUND',
        mask_dilation=0,
    ),
)

response3 = client.models.edit_image(
    model='imagen-3.0-capability-001',
    prompt='A stunning boat in the ocean',
    reference_images=[raw_ref_image, mask_ref_image],
    config=types.EditImageConfig(
        edit_mode='EDIT_MODE_INPAINT_INSERTION',
        number_of_images=1,
        include_rai_reason=True,
        output_mime_type='image/jpeg',
    ),
)

response3.generated_images[0].image.save("imagen-3-capability-001-2.png")

print(f"Created output image using {len(response3.generated_images[0].image.image_bytes)} bytes")
# Example response:
# Created output image using 1234567 bytes