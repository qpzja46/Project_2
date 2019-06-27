from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo, ObjectId
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
    print(pet_data['title'])
    # Return template and data
    return render_template("pet.html", pet_data=pet_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    pets = mongo.db.pets
    latest_pet = pets.find_one()

    # Example data
    # scraped_collection = [{'title': 'Dog'},
    #                       {'title': 'Cat seeking home'},
    #                       {'title': 'Chicken, potentially tasty'},
    #                       {'title': 'Rabbit that walks like a man'}]
    scraped_collection = scrape_craigslist.scrape_info('pet', latest_pet['craiglist_url'])

    # Update the Mongo database using insert
    pets.insert_many(scraped_collection)
    
    # Redirect back to home page
    return redirect("/")

@app.route('/pets/', defaults={'search_term': None})
@app.route("/pets/<search_term>")
def json(search_term):
    if search_term:
        search_term = ' ' + search_term.lower()
        # print(search_term)
    else:
        search_term = ''

    # Query the MongoDB for all pet data
    pet_data = mongo.db.pets.find()
    pet_json = []
    for pet_datum in pet_data:
        # print(pet_datum)

        # Filter the results 
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

    return jsonify(pet_json)

# Zipcode to lat-lon
@app.route('/locations/<zipcode>')
def zipcode_to_coordiantes(zipcode):
    location_data = mongo.db.zipcodes.find_one({'Zip': zipcode})
    coordinates = {'coordinates': [float(location_data['Latitude']),
                                   float(location_data['Longitude'])
                                   ]}
    return jsonify(coordinates)

if __name__ == "__main__":
    app.run(debug=True)
