from flask import Blueprint, request, jsonify
from app.models.companies import Company  # Importing the Company model
from app.extensions import db  # Importing the database instance

company_bp = Blueprint('company', __name__, url_prefix='/api/v1/company')

@company_bp.route('/register', methods=['POST'])
def register_company():
    try:
        # Extracting data from the request JSON
        name = request.json.get('name')
        origin = request.json.get('origin')
        description = request.json.get('description')
        user_id = request.json.get('user_id')
        
        # Basic input validation
        if not name:
            return jsonify({"error": 'Company name is required'}), 400
        
        if not origin:
            return jsonify({"error": 'Origin is required'}), 400
        
        if not description:
            return jsonify({"error": 'Description is required'}), 400

        # Create a new Company object and assign values from request JSON
        new_company = Company(name=name, origin=origin, description=description, user_id=user_id)
        
        # Add the new company to the database
        db.session.add(new_company)
        db.session.commit()

        return jsonify({"message": f"Company {new_company.name} has been created"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
