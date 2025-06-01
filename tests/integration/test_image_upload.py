import pytest
import os
from PIL import Image
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def temp_image():
    """Generate a temporary image for testing and clean up afterward."""
    img_path = "temp_test_image.jpg"

    # Create a dummy image
    img = Image.new("RGB", (100, 100), color="red")
    img.save(img_path)

    yield img_path  # Provide image path for test use

    # Teardown: Remove the image file
    os.remove(img_path)

def test_image_upload_via_ui(temp_image):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Change to False for debugging UI
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the image upload page
        page.goto("http://localhost:5000/images/")

        # Upload the temporary image file via UI input
        page.set_input_files("input[type='file']", temp_image)

        # Click the submit button to upload
        page.click("button[type='submit']")

        # Wait for confirmation message to appear
        page.wait_for_selector("text=File uploaded successfully")

        # Validate that success message is present
        assert "File uploaded successfully" in page.inner_text("body"), "Upload confirmation missing"

        browser.close()
