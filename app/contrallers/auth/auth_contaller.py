from flask import Blueprint, request,jsonify, User
from app.models import User
from flask import db

auth = Blueprint('auth', __name__,url_prefix='api/v1/auth')
@auth.route('/register',methods=['POST'])
def register_user():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    contact = request.json['contact']
    image = request.json['image']
    password = request.json['password']
    biography = request.json['biography']
    user_type = request.json['user_type']
    created_at = request.json['created_at']
    updated_at = request.json['updated_at']
    
    if not first_name:
        return jsonify({"error":'your first name is required'})    #this is the first approach
    
    if not last_name:
        return jsonify({"error":'your last name is required'})
    
    if not email:
        return jsonify({"error":'your email is required'})
    
    if not contact:
        return jsonify({"error":'your contact is required'})
    
    if not image:
        return jsonify({"error":'your image is required'})
    
    
    if len (password) < 6:
        return jsonify({"error":'your password must be atleast 10 characters'})
    
    if not user_type:
        return jsonify({"error":'your user_type is required'})
    
    
    if user_type == 'author' and not biography:
        return jsonify({"error":'your biography is required'})  #this is only supposed to be for the author, so it must have a constraint.
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error' : " this user name was already taken"})#this is a constarint for the emails, just incase they are already taken.
    
    #to insert into the table
user = User(first_name='first_name',last_name='last_name',email='email',contact='contact',image='image',password='password',biography='biography',user_type='user_type')
db.session.add(user)
db.session.commit()
def message():
        return f"account {'first_name'},{'last_name'} has been created" 
    
    
    
    
    
    
    
    
    
    
    