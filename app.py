from models import db,User
from flask_migrate import Migrate
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
# import datetime
from functools import wraps
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_cors import CORS  
import os
import time
from werkzeug.security import generate_password_hash


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'users.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY", "super-secret-key")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
jwt = JWTManager(app)
CORS(app)


#Initialize SQLAlchemy
db.init_app(app)

#Initialize Flask-Migrate after db 
migrate = Migrate(app, db)




@app.route('/')
def home():
    welcome = {"message":"Hello and welcome to my database url ,Proceed to /register or /login if have been here before explore the wonders of API's"}
    return welcome


# Adding New User !!
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not password:
        return jsonify({"msg": "Password is required"}), 400
    if not username:
        return jsonify({"msg": "Username is required"}), 400
    if not email:
        return jsonify({"msg": "Email is required"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        if existing_user.is_banned:
            return jsonify({"msg": "This account is banned and cannot be registered again."}), 403
        else:
            return jsonify({"msg": "Email already exists"}), 400

    new_user = User(username=username, email=email, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully!"}), 201


# Logging in The user to receive a jwt token
@app.route('/login', methods=["POST"])
def login():
    time.sleep(5)
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"Message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"Message": "Invalid credentials"}), 401

    if user.is_banned:
        return jsonify({"Message": "Your account is banned. Please contact support."}), 403

    if not user.check_password(password):
        return jsonify({"Message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))


    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "role": user.role
    }), 200

    
    
    # ROLE BASED ROUTES
def token_required(allowed_roles=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Verify JWT in request headers
                verify_jwt_in_request()

                # Get the current user ID from the token
                current_user_id = get_jwt_identity()
                current_user = db.session.get(User,current_user_id)
                print("Extracted User ID:", current_user_id)


                if not current_user:
                    return jsonify({'message': 'User not found'}), 404

                # Check if the user has the required role
                if allowed_roles and current_user.role not in allowed_roles:
                    return jsonify({'message': 'Unauthorized access'}), 403

                return f(current_user, *args, **kwargs)

            except Exception as e:
                return jsonify({'message': 'Token is invalid or expired', 'error': str(e)}), 401

        return decorated_function
    return decorator



# get all users route for admin
@app.route('/users',methods=['GET'])
@token_required(allowed_roles=['admin'])
def get_all_users(current_user):
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@app.route('/users',methods=['POST'])
@token_required(allowed_roles=['users','admin'])
def create_new_user(current_user):
    data = request.get_json()
    required_fields = ['username', 'email', 'password_hash']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"message": f"{field} is required"}), 400
        
    try:
        new_user=User(
            username=data['username'],
            email=data['email'],
            password_hash=data['password_hash']
        )
        new_user.set_password(data['password_hash'])
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"message": "Failed to create user", "error": str(e)}), 500    
    
    
@app.route('/users/<int:id>', methods=['PATCH'])
@token_required(allowed_roles=['admin'])
def update_user(current_user, id):
    user = User.query.get(id)
    if not user:
        return jsonify({"Error":f"User {id} not found"}),404
    data = request.get_json()

    if 'username' in data:
        user.username=data['username']
    if 'email' in data:
        user.email=data['email']
    if 'password_hash' in data:
        user.password_hash=generate_password_hash(data['password_hash'])
    if 'role' in data:
        user.role=data['role']

    db.session.commit()
    return jsonify(user.to_dict()),200

@app.route('/users/<int:id>', methods=['DELETE'])
@token_required(allowed_roles=['admin'])
def delete_user(current_user, id):
    user = User.query.get(id)
    if not user:
        return jsonify({"Error":f"User {id} not found"}),404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message":f"User {user.username} deleted"}),200

@app.route('/users/<int:user_id>/ban', methods=['POST'])
@token_required(allowed_roles=['admin'])
def ban_user(current_user, user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"Error": f"User with ID {user_id} not found"}), 404
    user.is_banned = True
    db.session.commit()
    return jsonify({"message": f"User {user.username} has been banned."}), 200


@app.route('/users/<int:user_id>/un-ban', methods=['POST'])
@token_required(allowed_roles=['admin'])
def unban_user(current_user, user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"Error": f"User with ID {user_id} not found"}), 404
    user.is_banned = False
    db.session.commit()
    return jsonify({"message": f"User {user.username} has been unbanned."}), 200


if __name__ == '__main__':
    app.run(debug=True, port=8888)    