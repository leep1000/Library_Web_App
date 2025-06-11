from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy database instance 
db = SQLAlchemy()

def create_app():
    # Create the Flask app object
    app = Flask(__name__)

    # Set secret key and database location 
    app.config['SECRET_KEY'] = 'secretkey123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

    # Connect database to this Flask app
    db.init_app(app)

    # Import routing for the app
    with app.app_context():
        # Import models to ensure they are registered with SQLAlchemy
        from . import models  
        # Create the database tables if they do not exist
        db.create_all()
        # populate the database with 10 records
        from .populate_db import populate_database
        populate_database()
        
    # Import the routes blueprint
    from .routes import routes_bp
    # Register the blueprint with the Flask app
    app.register_blueprint(routes_bp)

    return app
