from flask import Blueprint, request, jsonify
from app.models.users import User, db
from flask_bcrypt import Bcrypt
from email_validator import validate_email, EmailNotValidError  # Make sure email_validator is imported correctly

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
bcrypt = Bcrypt()

@auth.route('/register', methods=['POST'])
def register():
    try:
        # Extracting request data
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        contact = request.json.get('contact')
        email = request.json.get('email')
        user_type = request.json.get('user_type', 'author')  # Default to 'author'
        password = request.json.get('password')
        biography = request.json.get('biography', '') if user_type == 'author' else ''

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Basic input validation
        required_fields = ['first_name', 'last_name', 'contact', 'password', 'email']
        if not all(request.json.get(field) for field in required_fields):
            return jsonify({'error': 'All fields are required'}), 400

        if user_type == 'author' and not biography:
            return jsonify({'error': 'Enter your author biography'}), 400

        if len(password) < 6:
            return jsonify({'error': 'Password is too short'}), 400

        # Email validation 
        try:
            validate_email(email)  # Corrected the email validation function
        except EmailNotValidError:
            return jsonify({'error': 'Email is not valid'}), 400

        # Check for uniqueness of email and contact separately
        if User.query.filter_by(email=email).first() is not None:
            return jsonify({'error': 'Email already exists'}), 409

        if User.query.filter_by(contact=contact).first() is not None:
            return jsonify({'error': 'Contact already exists'}), 409

        # Creating a new user
        new_user = User(first_name=first_name, last_name=last_name, email=email,
                        contact=contact, password=hashed_password, user_type=user_type,
                        biography=biography)

        # Adding and committing to the database
        db.session.add(new_user)
        db.session.commit()

        # Building a response
        username = f"{new_user.first_name} {new_user.last_name}"

        return jsonify({
            'message': f'{username} has been successfully created as an {new_user.user_type}',
            'user': {
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'contact': new_user.contact,
                'type': new_user.user_type,
                'biography': new_user.biography,
                'created_at': new_user.created_at,
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500