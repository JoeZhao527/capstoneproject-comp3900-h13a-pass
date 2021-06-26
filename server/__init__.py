from flask import Flask
#from flask_sqlalchemy import SQLAlchemy

# create Application
app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')

'''
# create database for app as db
db_path = 'value_eat.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
db = SQLAlchemy(app)
'''

from server import routes