from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Flask web app instance creation
app = Flask(__name__)

# Database configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))                                                # gets this files path
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'finance_tracker.db')}"  # configure the sqlite URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)            # create the SQLAlchemy object and associate it with Flask app

migrate = Migrate(app, db)      # create the migration object and associate it with Flask app and the SQLAlchemy db
import models


@app.route('/')
def home():
    return {"message": "Hello, Flask!"}


if __name__ == '__main__':
    app.run(debug=True)

