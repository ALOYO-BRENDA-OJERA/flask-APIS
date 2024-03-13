from flask import Flask
from app.extensions import migrate,db

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

    
    return app
