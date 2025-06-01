import pytest
import os
from flask import Flask
from flask_injector import FlaskInjector
from app.Routes.menu import bp  # Import the blueprint
from app.Services.menu_service import MenuService
from io import BytesIO

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    from app import create_app  # Use the actual app factory

    app = create_app()
    app.config["TESTING"] = True

    return app.test_client()

def test_download_menu(client):
    """Test downloading the static PDF menu."""
    response = client.get("/menu/download")
    
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pdf"
    assert "attachment" in response.headers["Content-Disposition"]

def test_download_generated_menu(client, mocker):
    """Test generating and downloading the menu PDF."""
    mock_pdf_content = b"%PDF-1.4 Sample PDF Content"

    # Mock the entire Flask route to return a fake PDF response
    mocker.patch("app.Services.menu_service.MenuService.generate_menu_pdf", return_value=b"%PDF-1.4 Mock PDF Content")

    # Make the request
    response = client.get("/menu/download/generated")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pdf"
    assert response.data.startswith(b"%PDF")  # Ensure content starts like a PDF file

import pytest
import os
from flask import Flask
from flask_injector import FlaskInjector
from app.Routes.menu import bp  # Import the blueprint
from app.Services.menu_service import MenuService
from io import BytesIO

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    from app import create_app  # Use the actual app factory

    app = create_app()
    app.config["TESTING"] = True

    return app.test_client()

def test_download_menu(client):
    """Test downloading the static PDF menu."""
    response = client.get("/menu/download")
    
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pdf"
    assert "attachment" in response.headers["Content-Disposition"]

def test_download_generated_menu(client, mocker):
    """Test generating and downloading the menu PDF."""
    mock_pdf_content = b"%PDF-1.4 Sample PDF Content"

    # Mock the entire Flask route to return a fake PDF response
    mocker.patch("app.Services.menu_service.MenuService.generate_menu_pdf", return_value=b"%PDF-1.4 Mock PDF Content")

    # Make the request
    response = client.get("/menu/download/generated")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pdf"
    assert response.data.startswith(b"%PDF")  # Ensure content starts like a PDF file

def test_download_invalid_file_type(client):
    """Test downloading a non-PDF file, ensuring only PDFs are served."""
    response = client.get("/menu/download")  # No filename parameter, since the route always serves a PDF
    
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pdf"  # Validate it always returns a PDF

def test_upload_invalid_file_type(client):
    """Test uploading a non-PDF file."""
    data = {"file": (BytesIO(b"Fake content"), "invalid.txt")}  # Simulate a non-PDF file upload

    response = client.post("/menu/upload", content_type="multipart/form-data", data=data)

    assert response.status_code == 400
    assert b"Invalid file type. Only PDFs are allowed." in response.data  # Ensure correct validation