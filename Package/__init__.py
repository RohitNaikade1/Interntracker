from flask import *
from dotenv import load_dotenv
import bcrypt
from flask_mail import Mail,Message
from flask_pymongo import PyMongo
app=Flask(__name__)
from werkzeug.utils import secure_filename
import smtplib
from email.message import EmailMessage
import os
import pandas as pd

load_dotenv()

EMAIL_ADDRESS = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

app.config['SECRET_KEY']=os.getenv('SECRET_KEY')

UPLOAD_FOLDER = 'static/profiles'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
mail = Mail(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/InterTracker")
db = mongodb_client.db

from Package import adminRoutes,homeRoute,internRoutes,leaveRoutes,managerRoutes,mentorRoutes,planRoutes,profileRoutes