from flask import Flask, render_template, redirect, jsonify
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
    scraped_collection = [{'title': 'Dog'},
                          {'title': 'Cat seeking home'},
                          {'title': 'Chicken, potentially tasty'},
                          {'title': 'Rabbit that walks like a man'}]
    # result_data = scrape_craigslist.scrape_info()

    # Update the Mongo database using update and upsert=True
    pets.insert_many(scraped_collection)
    
    # Redirect back to home page
    return redirect("/")

@app.route("/json")
def json():

    # Run the scrape function and save the results to a variable
    pet_data = mongo.db.pets.find()
    pet_json = []
    for pet_datum in pet_data:
        pet_json.append({
            'title': pet_datum['title']
            })

    # Redirect back to home page
    return jsonify(pet_json)


if __name__ == "__main__":
    app.run(debug=True)
