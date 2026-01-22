import uuid
from app.extensions import bcrypt

class User:
    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = None
        self.is_admin = is_admin
        
        # Hash password if provided
        if password:
            self.hash_password(password)
    
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
