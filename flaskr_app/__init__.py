from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Create the app.
app = Flask(__name__)
app.secret_key = "IBelieveICanFly" 

# Configure the SQLite database, relative to the app instance folder.
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
# Don't print the DB warnings in the terminal. 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Create the DB extension instance. 
db = SQLAlchemy(app)

# Import routes. 
from flaskr_app import routes



