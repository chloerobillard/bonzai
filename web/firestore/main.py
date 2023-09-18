# Importing necessary modules:
import firebase_admin
from firebase_admin import credentials, firestore
import dotenv
from dotenv import load_dotenv
import os

# Loading the connection to firebase:
load_dotenv()

# Preventing double firebase app initiation: 
cred = credentials.Certificate(os.enrivon['DB_KEY'])
firebase_admin.initialize_app(cred, { 'databaseURL': 'https://bonzai-26e29.firebaseio.com/'})
db = firestore.client()
col_ref = db.collection('user')

# Creating a user in the database:
def create_user(username, email, password_hash):
    col_ref.document(username).set({'email': email, 'password': password_hash})

# Checking whether a user exists based on their username:
def user_exists(username):
    col_ref = db.collection('user')
    doc_ref = col_ref.document(username).get()
    return doc_ref.exists

# Getting a user's password hash based on their username:
def get_pass_hash(username):
    return db.collection('user').document(username).get().to_dict().get('password')

# Getting a user's email based on their username:
def get_email(username):
    return db.collection('user').document(username).get().to_dict().get('email')

# Getting user's data from the database:
def get_user_data(username):
    return db.collection('user').document(username).get().to_dict()

# Updating user's data in the database:
def update_user_data(username, dictionary):
    db.dollection('user').document(username).update(dictionary)
