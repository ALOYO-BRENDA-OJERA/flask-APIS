from flask import Blueprint, request, jsonify
from app.models.books import Book  # Import the Book model
from app.extensions import db

book_bp = Blueprint('book', __name__, url_prefix='/api/v1/book')

@book_bp.route('/register', methods=['POST'])
def register_book():
    data = request.json
    
    #id = data.get('id')
    title = data.get('title')
    description = data.get('description')
    image = data.get('image')
    price = data.get('price')
    price_unit = data.get('price_unit')
    pages = data.get('pages')
    publication_date = data.get('publication_date')
    isbn = data.get('isbn')
    genre = data.get('genre')
    pages = data.get('pages')
    user_id = data.get('user_id')
    company_id = data.get('company_id')
    created_at = data.get('created_at')
    updated_at = data.get('updated_at')

    #if not id:
        #return jsonify({"error": 'Your id is required'})

    if not title:
        return jsonify({"error": 'Your title is required'})

    if not description:
        return jsonify({"error": 'The description is required'})

    if not price:
        return jsonify({"error": 'The price is required'})

    if not price_unit:
        return jsonify({"error": 'The price_unit is required'})

    if not publication_date:
        return jsonify({"error": 'Please input the publication_date'})

    if not isbn:
        return jsonify({"error": 'Please input the isbn'})

    if not genre:
        return jsonify({"error": 'Please specify the genre'})
    
    if not pages:
        return jsonify({"error":'please enter the number of pages'})
    
    if not user_id:
        return jsonify({"error":'what is your user_id'})
    
    if not company_id:
        return jsonify({"error":'enter company id'})

    #new_book = Book(title=title, description=description, price=price, price_unit=price_unit,
                    #publication_date=publication_date, isbn=isbn, genre=genre)
    new_book = Book(title=title, description=description, price=price, price_unit=price_unit,
                    pages=pages, user_id=user_id, company_id=company_id, image=image,
                    publication_date=publication_date, isbn=isbn, genre=genre)
    
    db.session.add(new_book)
    db.session.commit()

    return jsonify({"message": f"Book '{title}' has been uploaded"})
