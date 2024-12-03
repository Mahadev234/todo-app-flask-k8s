from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import time

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Load configuration from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 'postgresql://postgres:password@db:5432/todo_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Wait for the database to be ready
    retries = 5
    while retries > 0:
        try:
            with app.app_context():
                from . import routes, models
                db.create_all()
                break
        except Exception as e:
            print(f"Database connection failed: {e}")
            retries -= 1
            time.sleep(5)

    if retries == 0:
        raise Exception("Database connection could not be established after retries.")

    return app
