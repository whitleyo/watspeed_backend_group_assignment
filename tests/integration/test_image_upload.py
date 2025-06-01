import pytest
from playwright.sync_api import sync_playwright

def test_image_upload_via_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True to run silently
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the image upload page
        page.goto("http://localhost:5000/images/")

        # Upload a test image file via UI input
        page.set_input_files("input[type='file']", "../data/test_image.jpg")

        # Click the submit button to upload
        page.click("button[type='submit']")

        # Wait for confirmation message to appear
        page.wait_for_selector("text=File uploaded successfully")

        # Validate that success message is present
        assert "File uploaded successfully" in page.inner_text("body"), "Upload confirmation missing"

        browser.close()

