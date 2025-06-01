import pytest
from playwright.sync_api import sync_playwright

def test_image_upload():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        request = context.request

        with open("../data/test_image.jpg", "rb") as file:
            response = request.post(
                "http://localhost:5000/images/upload",
                headers={"Content-Type": "multipart/form-data"},  # Force multipart encoding
                multipart={
                    "file": ("test_image.jpg", file, "image/jpeg")  # Send file metadata & binary data properly
                }
            )

        # Debugging output
        # Print request details
        print(f"🔍 Sent request headers: {response.headers}")
        print(f"🔍 Sent request body: {response.text()}")
        print(f"Raw request data: {request.data}")

        assert response.status == 200, f"Unexpected status code: {response.status}"
