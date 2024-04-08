# Implement the server
from flask import Flask, request, jsonify
from cos_functions import create_request, policy_variables
from functools import wraps
import traceback

app = Flask(__name__)

# Define the decorator
def validate_policy(policy_variables_class):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            policy_variables_dict = request.get_json()
            try:
                # Try to cast the dict to the policy_variables object
                policy_variables = policy_variables_class(**policy_variables_dict)
            except Exception as e:
                return jsonify(success=False, error=str(e)), 400
            return f(policy_variables, *args, **kwargs)
        return decorated_function
    return decorator

# Use the decorator
@app.route('/create_request', methods=['POST'])
@validate_policy(policy_variables)  # Replace with your actual policy_variables class
def create_request_route(policy_variables):
    try:
        create_request(policy_variables)
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

if __name__ == '__main__':
    app.run(port=5000)