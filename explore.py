from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
# import scrape_craigslist

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")

pet_data = mongo.db.pets.find()
for datum in pet_data:
    print(datum['title'])
