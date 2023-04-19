#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for, make_response
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import subprocess

# Initialize the Flask application
app = Flask(__name__)

# Set up the MongoDB client
client = MongoClient()
db = client['exampleapp']

# Define the routes for the application
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'POST':
        # Retrieve the form data and insert a new document into the database
        title = request.form['title']
        author = request.form['author']
        published = request.form['published']
        doc = {
            "title": title,
            "author": author,
            "published": published,
            "created_at": datetime.datetime.utcnow()
        }
        db.books.insert_one(doc)
        return redirect(url_for('books'))
    else:
        # Retrieve all documents from the database and render them in a template
        docs = db.books.find({})
        return render_template('books.html', docs=docs)

@app.route('/books/<mongoid>', methods=['GET', 'POST'])
def edit_book(mongoid):
    if request.method == 'POST':
        # Retrieve the form data and update the specified document in the database
        title = request.form['title']
        author = request.form['author']
        published = request.form['published']
        db.books.update_one(
            {"_id": ObjectId(mongoid)},
            {"$set": {
                "title": title,
                "author": author,
                "published": published,
                "created_at": datetime.datetime.utcnow()
            }}
        )
        return redirect(url_for('books'))
    else:
        # Retrieve the specified document from the database and render it in a template
        doc = db.books.find_one({"_id": ObjectId(mongoid)})
        return render_template('edit_book.html', doc=doc)

@app.route('/books/<mongoid>/delete')
def delete_book(mongoid):
    # Delete the specified document from the database
    db.books.delete_one({"_id": ObjectId(mongoid)})
    return redirect(url_for('books'))

@app.route('/authors', methods=['GET', 'POST'])
def authors():
    if request.method == 'POST':
        # Retrieve the form data and insert a new document into the database
        name = request.form['name']
        nationality = request.form['nationality']
        birthyear = request.form['birthyear']
        doc = {
            "name": name,
            "nationality": nationality,
            "birthyear": birthyear,
            "created_at": datetime.datetime.utcnow()
        }
        db.authors.insert_one(doc)
        return redirect(url_for('authors'))
    else:
        # Retrieve all documents from the database and render them in a template
        docs = db.authors.find({})
        return render_template('authors.html', docs=docs)

@app.route('/authors/<mongoid>', methods=['GET', 'POST'])
def edit_author(mongoid):
    if request.method == 'POST':
        # Retrieve the form data and update the specified document in the database
        name = request.form['name']
        nationality = request.form['nationality']
        birthyear = request.form['birthyear']
        db.authors.update_one(
            {"_id": ObjectId(mongoid)},
            {"$set": {
                "name": name,
                "nationality": nationality,
                "birthyear": birthyear,
                "created_at": datetime.datetime.utcnow()
            }}
        )
