from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
from flask_migrate import Migrate

import os

# Initialize Flask App
app = Flask(__name__)

# Initialize Database (and migrations)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Swagger API
api = Api(app)

import validateMe.views
