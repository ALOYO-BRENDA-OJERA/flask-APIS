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


@book_bp.route('/book/<int:book_id>', methods=['DELETE'])
@jwt_required()  # Only authenticated users can access this route
def delete_book(book_id):
    try:
        # Get current user ID from JWT token
        current_user_id = get_jwt_identity()
        
        # Check if the user is an author (user)
        current_user = User.query.get(current_user_id)
        if current_user.user_type != 'author':
            return jsonify({"error": "Only authors can delete books"}), 403
        
        # Find the book to delete
        book_to_delete = Book.query.filter_by(id=book_id, user_id=current_user_id).first()
        if not book_to_delete:
            return jsonify({"error": "Book not found or you don't have permission to delete it"}), 404

        db.session.delete(book_to_delete)
        db.session.commit()

        return jsonify({"message": f"Book with ID {book_id} has been deleted"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

#update
@book_bp.route('/book/<int:book_id>', methods=['PUT'])
@jwt_required()  # Only authenticated users can access this route
def update_book(book_id):
    try:
        data = request.get_json()

        # Get current user ID from JWT token
        current_user_id = get_jwt_identity()
        
        # Check if the user is an author (user)
        current_user = User.query.get(current_user_id)
        if current_user.user_type != 'author':
            return jsonify({"error": "Only authors can update books"}), 403

        # Find the book to update
        book_to_update = Book.query.filter_by(id=book_id, user_id=current_user_id).first()
        if not book_to_update:
            return jsonify({"error": "Book not found or you don't have permission to update it"}), 404

        # Update book details
        book_to_update.title = data.get('title', book_to_update.title)
        book_to_update.description = data.get('description', book_to_update.description)
        book_to_update.price = data.get('price', book_to_update.price)
        book_to_update.price_unit = data.get('price_unit', book_to_update.price_unit)
        book_to_update.pages = data.get('pages', book_to_update.pages)
        book_to_update.publication_date = datetime.strptime(data.get('publication_date'), '%Y-%m-%d').date() if data.get('publication_date') else book_to_update.publication_date
        book_to_update.isbn = data.get('isbn', book_to_update.isbn)
        book_to_update.genre = data.get('genre', book_to_update.genre)

        db.session.commit()

        return jsonify({"message": f"Book with ID {book_id} has been updated"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
