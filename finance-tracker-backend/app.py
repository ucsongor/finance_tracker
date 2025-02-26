from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

from extensions import db, migrate, jwt

# Load .env into os vars
load_dotenv()

# Flask web app instance creation
app = Flask(__name__)

# Configurations
BASE_DIR = os.path.abspath(os.path.dirname(__file__))                                                # gets this files path
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'finance_tracker.db')}"  # configure the sqlite URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

# Initialize extensions with the app
db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)

# Import models
from models import User, Transaction

# Register Blueprints
from auth import auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth")


@app.route('/')
def home():
    return {"message": "Hello, Flask!"}


if __name__ == '__main__':
    app.run(debug=True)

