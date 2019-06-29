from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo, ObjectId, DESCENDING
import scrape_craigslist

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def render_home():
    # Return template and data
    return render_template("index.html")

@app.route("/map")
def render_map():
    # Return template and data
    return render_template("map.html")

@app.route("/pet/<pet_id>")
def render_pet(pet_id):
    pet_id = ObjectId(pet_id)
    pet_data = mongo.db.pets.find_one({'_id': pet_id})
    # Return template and data
    return render_template("pet.html", pet_data=pet_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    # Set up the mongo connection
    pets = mongo.db.pets
    # Pull the most recent craigslist url so that the scraper knows when to stop
    try:
        latest_url = pets.find_one({}, sort=[("time_posted", DESCENDING)])['craiglist_url']    
        # Run the scraper using the keyword pet and the most recent url
    except TypeError:
        latest_url = ''

    scraped_collection = scrape_craigslist.scrape_info('pet', latest_url)
    # Update the Mongo database using insert
    pets.insert_many(scraped_collection)
    
    # Redirect back to home page
    return redirect("/")

# Route that will serve as a query-able API and link between our database and the javascript
@app.route('/pets/', defaults={'search_term': None})
@app.route("/pets/<search_term>")
def json(search_term):
    # Normalize the search term to lower case and add a space in front to cut down on words appearing within other words
    if search_term:
        search_term = ' ' + search_term.lower()
        # print(search_term)
    # If there was no specified search term, create an empty string so the subsequent filter doesn't break
    else:
        search_term = ''

    # Query the MongoDB for all pet data
    pet_data = mongo.db.pets.find()
    pet_json = []
    for pet_datum in pet_data:

        # Filter the results so only pets with the search term in their title or description are added to our list
        if (search_term in pet_datum['title'].lower()) or (search_term in pet_datum['description'].lower()):
            pet_json.append({
                'id': str(pet_datum['_id']),
                'title': pet_datum['title'],
                'image_urls': pet_datum['image_urls'],
                'description': pet_datum['description'],
                'coordinates': pet_datum['coordinates'],
                'craiglist_url': pet_datum['craiglist_url'],
                'time_posted': pet_datum['time_posted']
            })

    # Output the filtered results as a json file
    return jsonify(pet_json)

# Another API route that converts Zipcodes to lat-lon coordinates
@app.route('/locations/', defaults={'zipcode': None})
@app.route('/locations/<zipcode>')
def zipcode_to_coordiantes(zipcode):
    try:
        location_data = mongo.db.zipcodes.find_one({'Zip': zipcode})
        coordinates = {'coordinates': [float(location_data['Latitude']),
                                    float(location_data['Longitude'])
                                    ]}
    
    # If the user inputs an invalid zipcode, simply use the coordinates for the City of Chicago
    except:
        coordinates = {'coordinates': [41.8781, -87.6298]}

    # Output results as json
    return jsonify(coordinates)

if __name__ == "__main__":
    app.run(debug=True)
