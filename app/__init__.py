from flask import Flask
from app.extensions import migrate,db
from app.contrallers.auth.auth_contraller import auth
from app.contrallers.auth.book_contraller import book_bp
from app.contrallers.auth.company_contraller import company_bp  # Import the company blueprint


# Import your database model classes here

def create_app():
    app = Flask(__name__)

    # Load configuration from the Config class
    app.config.from_object('config.Config')
   
    # Initialize the Flask application with SQLAlchemy
    db.init_app(app)

    # Initialize Flask-Migrate for handling database migrations
    migrate.init_app(app,db)


    # Register blueprints or routes here
    
    @app.route('/')
    def home():
        return "AUTHORS API project set up 1"
    
    
    from app.models.users import User
    from app.models.companies import Company
    from app.models.books import Book

    app.register_blueprint(auth)
    app.register_blueprint(book_bp)  # Register the book blueprint with the specified URL prefix
    app.register_blueprint(company_bp)# Register the company blueprint with the specified URL prefix

    return app
