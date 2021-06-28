from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_sqlalchemy import SQLAlchemy

# create Application
app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../backend/valueEats.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from server import routes