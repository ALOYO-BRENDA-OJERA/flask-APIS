from app.extensions import db
from datetime import datetime
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/new_api'
# config.py

# Secret key for encoding and decoding JWTs
JWT_SECRET_KEY = 'your-secret-key'

# Token expiration time (for example, set to 15 minutes)
JWT_ACCESS_TOKEN_EXPIRES = 900  # 15 minutes in seconds
