from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models.books import Book
from app.models.users import User
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

book_bp = Blueprint('book', __name__, url_prefix='/api/v1/book')

@book_bp.route('/register', methods=['POST'])
@jwt_required()  # Only authenticated users can access this route
def register_book():
    try:
        data = request.get_json()

        # Extract data from the request
        title = data.get('title')
        description = data.get('description')
        price = data.get('price')
        price_unit = data.get('price_unit')
        pages = data.get('pages')
        publication_date = data.get('publication_date')
        isbn = data.get('isbn')
        genre = data.get('genre')
        company_id = data.get('company_id')  # Corrected access to company_id
        
        # Get current user ID from JWT token
        current_user_id = get_jwt_identity()
        
        # Check if the user is an author (user)
        current_user = User.query.get(current_user_id)
        if current_user.user_type != 'author':
            return jsonify({"error": "Only authors can register books"}), 403

        # Convert publication_date to a Date object
        try:
            publication_date = datetime.strptime(publication_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid publication date format. Please use YYYY-MM-DD"}), 400

        # Create a new book instance
        new_book = Book(
            title=title, description=description, price=price, price_unit=price_unit,
            pages=pages, user_id=current_user_id, company_id=company_id,  # Include company_id here
            publication_date=publication_date, isbn=isbn, genre=genre
        )

        # Add the book to the database session and commit changes
        db.session.add(new_book)
        db.session.commit()
        
        # Construct response message with all book details
        message = f"Book '{new_book.title}' with ID '{new_book.id}' has been registered"
        book_details = {
            'id': new_book.id,
            'title': new_book.title,
            'description': new_book.description,
            'price': new_book.price,
            'price_unit': new_book.price_unit,
            'pages': new_book.pages,
            'publication_date': new_book.publication_date.isoformat(),
            'isbn': new_book.isbn,
            'genre': new_book.genre,
            'user_id': new_book.user_id,
            'company_id': new_book.company_id
        }

        return jsonify({"message": message, "book": book_details}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
