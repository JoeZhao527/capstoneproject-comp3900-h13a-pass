from server import app
from flask import render_template, request
import json

@app.route('/')
def home():
    return render_template('eatery_home.html')

@app.route('/eatery/register')
def eatery_register():
    return render_template('eatery_register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/eatery_private_profile')
def eatery_private_profile():
    return render_template('eatery_private_profile.html')