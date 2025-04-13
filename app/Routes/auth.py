from flask import Blueprint, jsonify
from flask_expects_json import expects_json

auth_bp = Blueprint('auth', __name__)

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

@auth_bp.route('/register', methods=['POST'])
@expects_json(register_schema)
def register():
    """
    Register a new user.
    ---
    URL: /register
    Method: POST
    Request Payload: JSON containing username, password and email.
    Response: JSON with status and data fields.
    """
    # Stub response
    status=int(1)
    data=str("data")
    response = {"status": status, "data": data}
    return jsonify(response)

@expects_json(sign_in_schema)
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
    # Stub response
    status=int(1)
    data=str("data")
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
    # Stub response
    status=int(1)
    data=str("data")
    response = {"status": status, "data": data}
    return jsonify(response)
