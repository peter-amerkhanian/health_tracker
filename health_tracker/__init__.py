from flask import Flask
from health_tracker.forms import HealthForm
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_ADDRESS']
db = SQLAlchemy(app)