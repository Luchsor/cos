from flask import Flask, request, jsonify
import my_functions
import inspect
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a random secret key!
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    # This is a simple example of auth; you'd likely check a username and password instead
    username = request.json.get('username', None)
    if username != 'admin':
        return jsonify({"error": "Bad username or password"}), 401

    # Identity can be any data that is json serializable; here it's just a username
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route('/api/<function_name>', methods=['POST'])
@jwt_required()  # Protects this route with JWTs
def api(function_name):
    current_user = get_jwt_identity()  # Get the identity of the JWT owner, if needed
    data = request.json
    args = data.get('args', {})

    func = getattr(my_functions, function_name, None)

    if func and callable(func):
        sig = inspect.signature(func)
        required_args = [name for name, param in sig.parameters.items() if param.default == inspect.Parameter.empty and param.kind in [inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY]]

        missing_args = [arg for arg in required_args if arg not in args]
        if missing_args:
            return jsonify({"error": "Missing required arguments", "missing_args": missing_args}), 400

        result = func(**args)
        return jsonify({"result": result})
    else:
        return jsonify({"error": "Function not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
