from app.extensions import db
from datetime import datetime
from app.models.users import User  # Import User before Book
from app.models.companies import Company  # Import Company before Book

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    price_unit = db.Column(db.String(10), nullable=False, default='UGX')
    publication_date = db.Column(db.String(50), nullable=False)  # Changed to String for simplicity
    isbn = db.Column(db.String(30), nullable=False, unique=True)
    genre = db.Column(db.String(50), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Made nullable=False
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)  # Made nullable=False
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    user = db.relationship('User', backref='books')
    company = db.relationship('Company', backref='books')
    
    def __init__(self, title, description, price, price_unit, publication_date, isbn, genre, pages, user_id, company_id, image):
        super(Book, self).__init__()
        self.title = title
        self.description = description
        self.price = price
        self.price_unit = price_unit
        self.publication_date = publication_date
        self.isbn = isbn
        self.genre = genre
        self.pages = pages
        self.user_id = user_id
        self.company_id = company_id
        self.image = image

    def __repr__(self):
        return f'<Book {self.title}>'
