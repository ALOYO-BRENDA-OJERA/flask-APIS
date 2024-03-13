from flask import Blueprint, request,jsonify, User
from app.models import User
from flask import db

company = Blueprint('company', __name__,url_prefix='api/v1/company')
@company.route('/register',methods=['POST'])
def register_company():
    id = request.json['id']
    name = request.json['name']
    origin = request.json['origin']
    description = request.json['description']
    
    created_at = request.json['created_at']
    updated_at = request.json['updated_at']
    
    if not id:
        return jsonify({"error":'your first company id is required'})    #this is the first approach
    
    if not name:
        return jsonify({"error":'your company name is required'})
    
    if not origin:
        return jsonify({"error":'your origin is required'})
    
    if not description:
        return jsonify({"error":'please add a description of your company'})
     
     
    
    #to insert into the table
user = User(first_name='first_name',last_name='last_name',email='email',contact='contact',image='image',password='password',biography='biography',user_type='user_type')
db.session.add(user)
db.session.commit()
def message():
        return f"account {'first_name'},{'last_name'} company has been created" 
    
    
    
    
    
    
    
    
    
    
    