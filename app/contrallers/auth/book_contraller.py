from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models.books import Book
from app.models.users import User
from app.models.companies import Company
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
            pages=pages, user_id=current_user_id, publication_date=publication_date,
            isbn=isbn, genre=genre
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
            'user_id': new_book.user_id
        }

        return jsonify({"message": message, "book": book_details}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@book_bp.route('/books/', methods=['GET'])
@jwt_required()  # Only authenticated users can access this route
def get_all_books():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if current_user.user_type == 'admin':
        books = Book.query.all()
    else:
        books = Book.query.filter_by(user_id=current_user_id).all()

    output = []
    for book in books:
        book_data = {
            'id': book.id,
            'title': book.title,
            'description': book.description,
            'price': book.price,
            'price_unit': book.price_unit,
            'pages': book.pages,
            'publication_date': book.publication_date.isoformat(),
            'isbn': book.isbn,
            'genre': book.genre,
            'user_id': book.user_id
        }
        output.append(book_data)
    
    return jsonify({'books': output})

@book_bp.route('/book/<int:id>', methods=['GET'])
@jwt_required()  # Only authenticated users can access this route
def get_book(id):
    book = Book.query.get_or_404(id)
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if current_user.user_type == 'admin' or current_user_id == book.user_id:
        book_data = {
            'id': book.id,
            'title': book.title,
            'description': book.description,
            'price': book.price,
            'price_unit': book.price_unit,
            'pages': book.pages,
            'publication_date': book.publication_date.isoformat(),
            'isbn': book.isbn,
            'genre': book.genre,
            'user_id': book.user_id
        }
        return jsonify(book_data)
    else:
        return jsonify({"error": "You are not authorized to access this book"}), 403

@book_bp.route('/book/<int:id>', methods=['PUT'])
@jwt_required()  # Only authenticated users can access this route
def update_book(id):
    try:
        data = request.get_json()
        book = Book.query.get_or_404(id)
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if current_user.user_type != 'admin' and current_user_id != book.user_id:
            return jsonify({"error": "You are not authorized to update this book"}), 403

        book.title = data.get('title', book.title)
        book.description = data.get('description', book.description)
        book.price = data.get('price', book.price)
        book.price_unit = data.get('price_unit', book.price_unit)
        book.pages = data.get('pages', book.pages)
        book.publication_date = datetime.strptime(data.get('publication_date'), '%Y-%m-%d').date()
        book.isbn = data.get('isbn', book.isbn)
        book.genre = data.get('genre', book.genre)
        
        db.session.commit()
        
        return jsonify({"message": "Book updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@book_bp.route('/book/<int:id>', methods=['DELETE'])
@jwt_required()  # Only authenticated users can access this route
def delete_book(id):
    book = Book.query.get_or_404(id)
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if current_user.user_type != 'admin' and current_user_id != book.user_id:
        return jsonify({"error": "You are not authorized to delete this book"}), 403
    
    db.session.delete(book)
    db.session.commit()
    
    return jsonify({"message": "Book deleted successfully"}), 200
