from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename

# Define Blueprint
bp = Blueprint('images', __name__, url_prefix='/images')

# Function to check if file type is allowed
def allowed_file(filename):
    allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS')  
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Route to handle image uploads
@bp.route('/upload', methods=['POST'])
def upload_file():
    print(f"Request content type: {request.content_type}")
    print(f"Raw request data: {request.data}")  # Print raw incoming request body
    print(f"Received files: {request.files}")
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']  
        os.makedirs(upload_folder, exist_ok=True)  
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    else:
        return jsonify({'error': 'Invalid file type. Only certain image files are allowed'}), 400