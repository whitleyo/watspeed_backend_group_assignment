from create_app import create_app  # Import factory function

app = create_app()  # Create the Flask app instance

if __name__ == "__main__":
    # Run the app on port 5001 (Watspeed web service runs on port 5000)
    app.run(port=5001)
