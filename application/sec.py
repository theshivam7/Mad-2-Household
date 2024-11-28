# from flask_security import SQLAlchemyUserDatastore
# from .models import db, User, Role

# datastore = SQLAlchemyUserDatastore(db, User, Role)

# Import the Flask-Security datastore interface for SQLAlchemy integration
from flask_security import SQLAlchemyUserDatastore
# Import database models and configuration
from .models import db, User, Role

# Method 1: Direct instantiation approach
# Creates a user datastore instance to manage users and roles using SQLAlchemy
# db: SQLAlchemy database instance
# User: User model class for storing user information
# Role: Role model class for storing role/permission information
datastore = SQLAlchemyUserDatastore(db, User, Role)

