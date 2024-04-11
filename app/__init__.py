from flask import Flask
from app.extensions import migrate, db
from flask_sqlalchemy import SQLAlchemy
from app.contrallers.auth.auth_contraller import auth
from app.contrallers.auth.book_contraller import book_bp
from app.contrallers.auth.company_contraller import company_bp  # Corrected import statement
from flask_jwt_extended import JWTManager  # Import JWTManager
# Import your database model classes here


def create_app():  #application factory fucntion
    app = Flask(__name__)

    # Load configuration from the Config class
    app.config.from_object('config.Config')
    
     # Set the JWT secret key
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'
   
    # Initialize the Flask application with SQLAlchemy
    db.init_app(app)
    # Initialize JWTManager
    jwt = JWTManager(app)

    # Initialize Flask-Migrate for handling database migrations
    migrate.init_app(app, db)

    # Register blueprints or routes here
    
    
    from app.models.users import User
    from app.models.companies import Company
    from app.models.books import Book

    app.register_blueprint(auth)
    app.register_blueprint(book_bp)
    app.register_blueprint(company_bp)  # Register the company blueprint
    
    
    
    @app.route('/')
    def home():
        return "AUTHORS API project set up 1"

    return app

