from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
# import scrape_craigslist

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")



# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    pet_data = mongo.db.pets.find_one()

    # Return template and data
    return render_template("index.html", pet_data=pet_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function and save the results to a variable
    pets = mongo.db.pets

    # Example data
    result_data = {'title': 'Pet For Sale'}
    # result_data = scrape_craigslist.scrape_info()


    # Update the Mongo database using update and upsert=True
    pets.update({}, result_data, upsert=True)
    
    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
