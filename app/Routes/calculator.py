from flask import Blueprint, request, jsonify, current_app, render_template
import os

# Define Blueprint
bp = Blueprint('calculator', __name__, url_prefix='/calculator')

@bp.route('/')
def calculator():
    return render_template('calculator.html')