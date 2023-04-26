#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for, make_response
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import subprocess
import pymongo

# Initialize the Flask application
app = Flask(__name__)

# Set up the MongoDB client
# client = MongoClient()
# db = client['exampleapp']

uri = "mongodb+srv://ek3395:ek3395@webapps.r8y7smt.mongodb.net/?retryWrites=true&w=majority"
connection = pymongo.MongoClient(uri)
db = connection['ek3395']

@app.route('/')
def home():
    """
    Route for the home page
    """
    return render_template('index.html')

@app.route('/review')
def review():
    """
    Route for displaying all reviews.
    Retrieves all documents from the apartment_reviews collection and passes them to the reviews.html template.
    """
    reviews = db.apartment_reviews.find()
    return render_template('review.html', reviews=reviews)

 
@app.route('/create')
def create(): # creates the form 

    return render_template('create.html') # render the create template



@app.route('/create', methods=['POST'])
def create_post():
    """
    Route for POST requests to the create page.
    Accepts the form submission data for a new document and saves the document to the database.
    """
    name = request.form['name']
    address = request.form['address']
    rent = request.form['rent']
    borough = request.form['borough']
    bedrooms = request.form['bedrooms']
    bathrooms = request.form['bathrooms']
    washer_dryer = request.form['washer_dryer']
    dishwasher = request.form['dishwasher']
    message = request.form['message']

    # create a new document with the data the user entered
    doc = {
        "name": name,
        "address": address,
        "rent": rent,
        "borough": borough,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "washer_dryer": washer_dryer,
        "dishwasher": dishwasher,
        "message": message, 
        "created_at": datetime.datetime.utcnow()
    }

    db.apartment_reviews.insert_one(doc) # insert a new document

    return redirect(url_for('thankyou'))


@app.route('/thankyou', methods=['GET'])
def thankyou():
    return render_template('thankyou.html')

@app.route('/delete', methods=['POST'])
def delete_review():
    """
    Route for POST requests to delete a review.
    Accepts the form submission data for a review to be deleted and removes the corresponding document from the database.
    """
    
    # retrieve the ID of the document to be deleted from the form data
    review_id = request.form['review_id']
    
    # delete the document from the database using the ID
    db.apartment_reviews.delete_one({'_id': ObjectId(review_id)})
    
    return redirect(url_for('review'))

@app.route('/edit/<mongoid>')
def edit(mongoid):
    """
    Route for GET requests to the edit page.
    Displays a form users can fill out to edit an existing record.
    """
    doc = db.exampleapp.find_one({"_id": ObjectId(mongoid)})
    return render_template('edit.html', mongoid=mongoid, doc=doc) # render the edit template

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    GitHub can be configured such that each time a push is made to a repository, GitHub will make a request to a particular web URL... this is called a webhook.
    This function is set up such that if the /webhook route is requested, Python will execute a git pull command from the command line to update this app's codebase.
    You will need to configure your own repository to have a webhook that requests this route in GitHub's settings.
    Note that this webhook does do any verification that the request is coming from GitHub... this should be added in a production environment.
    """
    # run a git pull command
    process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
    pull_output = process.communicate()[0]
    # pull_output = str(pull_output).strip() # remove whitespace
    process = subprocess.Popen(["chmod", "a+x", "flask.cgi"], stdout=subprocess.PIPE)
    chmod_output = process.communicate()[0]
    # send a success response
    response = make_response('output: {}'.format(pull_output), 200)
    response.mimetype = "text/plain"
    return response

@app.errorhandler(Exception)
def handle_error(e):
    """
    Output any errors - good for debugging.
    """
    return render_template('error.html', error=e) # render the edit template

@app.route('/budget')
def budget():
    """
    Route that retrieves the cheapest reviews from the database and renders the budget.html template.
    """
    # Retrieve the cheapest reviews from the database
    cheapest_reviews = list(db.apartment_reviews.find().sort('rent', 1).limit(10))
    
    # Render the budget.html template with the cheapest_reviews variable
    return render_template('budget.html', cheapest_reviews=cheapest_reviews)


if __name__ == "__main__":
    #import logging
    #logging.basicConfig(filename='/home/ak8257/error.log',level=logging.DEBUG)
    app.run(debug = True)