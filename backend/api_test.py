# backend/api_test.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os

# Attempt to import app from api.py.
# This assumes that when pytest is run, the 'backend' directory is in PYTHONPATH
# or pytest is run from a location where 'backend.api' can be resolved.
# If api.py is in the same directory as api_test.py and pytest is run from backend/,
# then 'from api import app' should work.
from api import app

client = TestClient(app)

# Valid base64 encoded 1x1 transparent PNG for testing
VALID_BASE64_IMAGE = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
VALID_MIMETYPE = "image/png"

@pytest.fixture(autouse=True)
def manage_gemini_api_key():
    # This fixture ensures that GEMINI_API_KEY is managed correctly for each test.
    # It saves the original state of the key, allows tests to modify it,
    # and then restores it after the test.
    original_key = os.environ.get("GEMINI_API_KEY")
    yield # This is where the test runs
    if original_key is not None:
        os.environ["GEMINI_API_KEY"] = original_key
    elif "GEMINI_API_KEY" in os.environ: # If it was set during test but not originally
        del os.environ["GEMINI_API_KEY"]


def test_generate_tryon_success():
    os.environ["GEMINI_API_KEY"] = "test_api_key"

    # If api.py has `from product_utils import generate_gemini_tryon_image as func_in_api`,
    # and then this func_in_api is called, we mock 'api.func_in_api'.
    # Based on current api.py, it directly imports and uses generate_gemini_tryon_image.
    # So, the mock path should be 'api.generate_gemini_tryon_image'.
    with patch("api.generate_gemini_tryon_image") as mock_generate:
        # The actual function `generate_gemini_tryon_image` is async.
        # While TestClient handles the overall async endpoint, when mocking the direct function
        # that is awaited, the mock should also behave like an async function if it's directly awaited.
        # However, FastAPI's TestClient runs the event loop, so a simple return_value
        # on a MagicMock can often work if the TestClient abstracts the await.
        # For safety with `await` in the endpoint, an AsyncMock might be more robust if issues arise.
        # For now, the prompt example uses return_value, implying TestClient handles it.
        mock_generated_data_url = f"data:{VALID_MIMETYPE};base64,{VALID_BASE64_IMAGE}"
        mock_generate.return_value = mock_generated_data_url

        response = client.post(
            "/api/v1/tryon/generate",
            json={
                "user_image_base64": VALID_BASE64_IMAGE,
                "user_image_mimetype": VALID_MIMETYPE,
                "product_image_base64": VALID_BASE64_IMAGE,
                "product_image_mimetype": VALID_MIMETYPE,
            },
        )
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["generated_image_base64"] == mock_generated_data_url
        assert json_response["mimetype"] == VALID_MIMETYPE
        mock_generate.assert_called_once_with(
            model_image_base64=VALID_BASE64_IMAGE,
            model_image_mimetype=VALID_MIMETYPE,
            clothing_image_base64=VALID_BASE64_IMAGE,
            clothing_image_mimetype=VALID_MIMETYPE,
        )

def test_generate_tryon_no_api_key_at_endpoint():
    # This test targets the check within the endpoint itself.
    # The global genai.configure() in api.py might have already run with/without a key.
    # This test ensures the endpoint's specific guard works.
    os.environ.pop("GEMINI_API_KEY", None) # Ensure key is not set for this test execution path

    # To truly test the genai.configure() part, module reloading or app factory pattern would be needed.
    # This test relies on the endpoint's internal check of GEMINI_API_KEY.
    # We need to ensure that the `GEMINI_API_KEY` variable *within the scope of api.py* is None
    # when the endpoint is called. The fixture `manage_gemini_api_key` helps with os.environ.
    # The print warning in api.py about key not set is at module load time.
    # The HTTPException in the endpoint is what we're testing here.

    response = client.post(
        "/api/v1/tryon/generate",
        json={
            "user_image_base64": "test", "user_image_mimetype": "image/png",
            "product_image_base64": "test", "product_image_mimetype": "image/png",
        },
    )
    assert response.status_code == 500
    assert "Gemini API key not configured on server" in response.json()["detail"]


def test_generate_tryon_gemini_failure():
    os.environ["GEMINI_API_KEY"] = "test_api_key"

    with patch("api.generate_gemini_tryon_image") as mock_generate:
        # Simulate an error raised by the generate_gemini_tryon_image function
        mock_generate.side_effect = RuntimeError("Gemini processing failed")

        response = client.post(
            "/api/v1/tryon/generate",
            json={
                "user_image_base64": VALID_BASE64_IMAGE, "user_image_mimetype": VALID_MIMETYPE,
                "product_image_base64": VALID_BASE64_IMAGE, "product_image_mimetype": VALID_MIMETYPE,
            },
        )
        assert response.status_code == 500
        json_response = response.json()
        assert "detail" in json_response
        assert "Gemini processing failed" in json_response["detail"]


def test_generate_tryon_bad_request_missing_fields():
    os.environ["GEMINI_API_KEY"] = "test_api_key" # API key needed for endpoint to proceed to validation
    response = client.post(
        "/api/v1/tryon/generate",
        json={"user_image_base64": "test"}, # Missing other required fields
    )
    assert response.status_code == 422 # Unprocessable Entity for Pydantic validation errors
    # Optionally, check the content of the error if needed
    # json_response = response.json()
    # assert "product_image_base64" in [err['loc'][0] for err in json_response['detail']]
    # assert "user_image_mimetype" in ...
    # assert "product_image_mimetype" in ...
