from flask import Blueprint, jsonify, request
# from flask_expects_json import expects_json

auth_bp = Blueprint('auth', __name__)

# Define JSON schemas for request validation
# will use later rather than status 0 and 1
'''
register_schema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'},
        'email': {'type': 'string', 'format': 'email'}
    },
    'required': ['username', 'password', 'email']
    }

sign_in_schema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['username', 'password']
    }
'''

# @expects_json(register_schema)
@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    ---
    URL: /register
    Method: POST
    Request Payload: JSON containing username, password and email.
    Response: JSON with status and data fields.
    """
    # Validate
    req_data = request.get_json()
    data : str = str("data")
    status : int = int(0)

    if not req_data:
        status = int(1)
        response = {"status": status, "data": data}
        return jsonify(response)

    username = req_data.get("username")
    email = req_data.get("email")
    password = req_data.get("password")

    if not email or not isinstance(email, str) or not email.strip():
        status = int(1)
    elif not username or not isinstance(username, str) or not username.strip():
        status = int(1)
    elif not password or not isinstance(password, str) or not password.strip():
        status = int(1)

    # Stub response
    response = {"status": status, "data": data}
    return jsonify(response)

# @expects_json(sign_in_schema)
@auth_bp.route('/sign-in', methods=['POST'])
def sign_in():
    """
    Sign in an existing user.
    ---
    URL: /sign-in
    Method: POST
    Request Payload: JSON containing username and password.
    Response: JSON with status and data fields.
    """
    # Validate
    req_data = request.get_json()
    data : str = str("data")
    status : int = int(0)

    if not req_data:
        status = int(1)
        response = {"status": status, "data": data}
        return jsonify(response)

    username = req_data.get("username")
    password = req_data.get("password")

    if not username or not isinstance(username, str) or not username.strip():
        status = int(1)
    elif not password or not isinstance(password, str) or not password.strip():
        status = int(1)

    # Stub response
    response = {"status": status, "data": data}
    return jsonify(response)

@auth_bp.route('/sign-out', methods=['POST'])
def sign_out():
    """
    Sign out the current user.
    ---
    URL: /sign-out
    Method: POST
    Request Payload: None.
    Response: JSON with status and data fields.
    """
    # No payload to validate
    # Stub response
    status=int(0)
    data=str("data")
    response = {"status": status, "data": data}
    return jsonify(response)
