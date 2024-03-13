from app.extensions import db
from datetime import datetime



class Book(db.Model):
    __tablename__= 'books'
    id = db.Column (db.Integer,primary_key=True)
    title= db.Column(db.String(20),nullable=False)
    description = db.Column(db.String(150),nullable=False)
    image = db.Column(db.String(255),nullable=True)
    price = db.Column(db.Integer,nullable=False)
    price_unit = db.Column(db.String(50),nullable=False,default='UGX')
    pages =db.Column(db.Integer,nullable=False)
    publication_date = db.Column(db.Date,nullable=False)
    isbn = db.Column(db.String(30),nullable=False,unique=True)
    genre = db.Column(db.String(50),nullable=False)
    

    #Relationship with Users
    users = db.relationship('Users',backref='book')
    
    #Relationship with Companies
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    Company = db.relationship ('Companies', backref='books')

    #user=db.relationship('User',backref='books')
    #Company = db.relationship('Company',backref='books)

    created_at = db.Column(db.DateTime,default=datetime.now())
    updated_at = db.Column(db.DateTime,onupdate=datetime.now())

    def __init__(self, id, title, description, image, price, price_unit, pages, publication_date, isbn, genre):
        super(Book, self).__init__()
        self.id = id
        self.title = title
        self.description = description
        self.image = image
        self.price = price
        self.price_unit = price_unit
        self.pages = pages
        self.publication_date = publication_date
        self.isbn = isbn
        self.genre = genre

    def __repr__(self):
        return f'<Book {self.title}>'