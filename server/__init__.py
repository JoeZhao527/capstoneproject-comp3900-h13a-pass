import os
from flask import Flask, render_template
#from flask_sqlalchemy import SQLAlchemy

# create Application
app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')

'''
# create database for app as db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///value_eat.db'
db = SQLAlchemy(app)
'''

from server import routes