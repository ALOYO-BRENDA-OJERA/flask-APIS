from flask import Blueprint, request,jsonify, Book
from app.models import Book
from flask import db

book = Blueprint('book', __name__,url_prefix='api/v1/book')
@book.route('/register',methods=['POST'])
def register_book():
    id = request.json['id']
    title = request.json['title']
    description = request.json['description']
    image = request.json['image']
    price = request.json['price']
    price_unit = request.json['price_unit']
    pages = request.json['pages']
    publication_date = request.json['publication_date']
    isbn = request.json['isbn']
    genre = request.json['genre']
    created_at = request.json['created_at']
    updated_at = request.json['updated_at']

    if not id:
        return jsonify({"error":'your id is required'})    #this is the first approach
    
    if not title:
        return jsonify({"error":'your title is required'})
    
    if not description:
        return jsonify({"error":'The description is required'})
    
    if not price:
        return jsonify({"error":'The price is required'})
    
    if not price_unit:
        return jsonify({"error":'The price_unit is required'})
    
    if not publication_date:
        return jsonify({"error":'Please input the publication_date'})
    
    if not isbn:
        return jsonify({"error":'Please input the isbn'})
    
    if not genre:
        return jsonify({"error":'Please specif y the genre'})
    

    
    #to insert into the table
user = Book(id='id',title='title',description='description',price='price',price_unit='price_unit',publication_date='publication_date',isbn='isbn',genre='genre')
db.session.add(Book)
db.session.commit()
def message():
        return f"The Book {'title'},{'id'} has been Uploaded" 
    
    
    