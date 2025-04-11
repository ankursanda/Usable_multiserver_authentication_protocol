from flask import Blueprint, request, jsonify, current_app
from .register import RegistrationCenter
from app.database import storage  # Import the storage instance
from datetime import datetime
import base64
import logging
import hmac
from functools import wraps
import time

logger = logging.getLogger(__name__)

register_bp = Blueprint('main', __name__)

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        # Use current_app.config to access the API key dynamically
        expected_api_key = current_app.config.get('API_KEY')
        if not api_key or not expected_api_key or not hmac.compare_digest(api_key, expected_api_key):
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated

def rate_limit(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        client_ip = request.remote_addr
        current_time = time.time()
        rate_limit_key = f"rate_limit_{client_ip}"
        
        # Initialize or clean old requests
        if rate_limit_key not in storage.rate_limit_storage:
            storage.rate_limit_storage[rate_limit_key] = []
        
        # Remove requests older than 1 minute
        storage.rate_limit_storage[rate_limit_key] = [
            req_time for req_time in storage.rate_limit_storage[rate_limit_key]
            if current_time - req_time < 60
        ]
        
        # Check rate limit
        rate_limit = current_app.config.get('RATE_LIMIT', 10)  # Default rate limit is 10 requests per minute
        if len(storage.rate_limit_storage[rate_limit_key]) >= rate_limit:
            return jsonify({'error': 'Rate limit exceeded'}), 429
        
        # Add current request
        storage.rate_limit_storage[rate_limit_key].append(current_time)
        
        return f(*args, **kwargs)
    return decorated

# Initialize Registration Center


@register_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@register_bp.route('/api/v1/register/user', methods=['POST'])
def register_user():
    registration_center = getattr(register_bp, 'registration_center', None)
    if not registration_center:
        return jsonify({'error': 'Service configuration issue'}), 500
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'user_id' not in data or 'A_i' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
            
        # Decode A_i from base64
        try:
            A_i = base64.b64decode(data['A_i'])
        except Exception:
            return jsonify({'error': 'Invalid A_i format'}), 400
            
        # Check if user already exists
        # if storage.get_user(data['user_id']):
        #     return jsonify({'error': 'User already registered'}), 409
            
        # Register user
        C_i, h_x = registration_center.register_user(data['user_id'], A_i)
        
        # Return response
        return jsonify({
            'status': 'success',
            'C_i': base64.b64encode(C_i).decode('utf-8'),
            'h_x': base64.b64encode(h_x).decode('utf-8')
        })
        
    except Exception as e:
        logger.error(f"Error in user registration endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@register_bp.route('/api/v1/register/server', methods=['POST'])
@require_api_key
@rate_limit
def register_server():
    """Server registration endpoint"""
    registration_center = getattr(register_bp, 'registration_center', None)
    if not registration_center:
        return jsonify({'error': 'Service configuration issue'}), 500
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'server_id' not in data or 'Q_j' not in data or 'V_j' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
            
        # Decode Q_j and V_j from base64
        try:
            Q_j = base64.b64decode(data['Q_j'])
            V_j = base64.b64decode(data['V_j'])
        except Exception:
            return jsonify({'error': 'Invalid format for Q_j or V_j'}), 400
            
        # Check if server already exists
        if storage.get_server(data['server_id']):
            return jsonify({'error': 'Server already registered'}), 409
            
        # Register server
        SM_j, SV_j = registration_center.register_server(data['server_id'], Q_j, V_j)
        
        # Return response
        return jsonify({
            'status': 'success',
            'SM_j': base64.b64encode(SM_j).decode('utf-8'),
            'SV_j': base64.b64encode(SV_j).decode('utf-8')
        })
        
    except Exception as e:
        logger.error(f"Error in server registration endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Error handlers
@register_bp.errorhandler(404)
def not_found(e):
    """Handler for 404 Not Found errors."""
    return jsonify({'error': 'Not found'}), 404

@register_bp.errorhandler(500)
def internal_error(e):
    """Handler for 500 Internal Server errors."""
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({'error': 'Internal server error'}), 500
