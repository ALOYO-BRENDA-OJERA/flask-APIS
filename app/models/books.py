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
    price_unit = db.Column(db.Integer, nullable=False, default='UGX')
    publication_date = db.Column(db.Date, nullable=False)
    isbn = db.Column(db.String(30), nullable=True, unique=True)
    genre = db.Column(db.String(50), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    user = db.relationship('User', backref='books')
    company = db.relationship('Company', backref='books')
    
    def __init__(self, title, price, description, pages, user_id, price_unit, publication_date, isbn, company_id, image, genre):
        super(Book, self).__init__()
        self.title = title
        self.description = description
        self.price = price
        self.user_id = user_id
        self.price_unit = price_unit
        self.pages = pages
        self.isbn = isbn
        self.publication_date = publication_date
        self.genre = genre
        self.company_id = company_id

    def __repr__(self):
        return f'<Book {self.title}>'
