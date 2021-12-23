from flask import *
import bcrypt
from flask_mail import Mail,Message
from flask_pymongo import PyMongo
app=Flask(__name__)
from werkzeug.utils import secure_filename
import os
import pandas as pd

app.config['SECRET_KEY']='rohit'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'rohit.naikade@gslab.com'
app.config['MAIL_PASSWORD'] = 'vgshfwkiyxjrnuyp'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
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