from app import db, bcrypt
import uuid
from .base_model import BaseModel  # Import BaseModel from its module

class User(BaseModel):
    __tablename__ = 'users'
    #### Task 6
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
   # def __init__(self, first_name, last_name, email, password=None, is_admin=False):
    #    self.id = str(uuid.uuid4())
    #    self.first_name = first_name
    #    self.last_name = last_name
    #    self.email = email
    #    self.password = None
   #     self.is_admin = is_admin
        
        # Hash password if provided
     #   if password:
    #        self.hash_password(password)
    
    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
    
    def to_dict(self):
        """Convert user object to dictionary, excluding password."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        }
