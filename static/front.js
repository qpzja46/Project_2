var mapElement = d3.select('#map-id');
var frontElement = d3.select('#front-id');


// Select the submit button
var submit = d3.select("#submit");

submit.on("click", function() {

  // Prevent the page from refreshing
  d3.event.preventDefault();

  // Select the input element and get the raw HTML node
  var inputElementzipcode = d3.select("#zipcode");
  var inputElementsearchterm = d3.select("#searchterm");
  
  // Get the value property of the input element
  var zipcode = inputElementzipcode.property("value");
  var searchTerm = inputElementsearchterm.property("value");

  console.log(zipcode);
  console.log(searchTerm);

  var url = '/locations/' + zipcode;

  d3.json(url).then(function(zip_response) {
    console.log(zip_response.coordinates);
    var coordinates = zip_response.coordinates;
    url = '/pets/' + searchTerm;
    d3.json(url).then(function(pet_response) {
      console.log(pet_response);
      createMarkers(pet_response, coordinates);
      
    });
  });
  mapElement.style('display', 'block');
  frontElement.style('display', 'none');
});

function createMap(petFind, coordinates) {

  // Create the tile layer that will be the background of our map
  var lightmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, <a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"http://mapbox.com\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.light",
    accessToken: API_KEY
  });

  // Create a baseMaps object to hold the lightmap layer
  var baseMaps = {
    "Light Map": lightmap
  };

  // Create an overlayMaps object to hold the petFind layer
  var overlayMaps = {
    "Pet Find": petFind
  };

  // Create the map object with options
  var map = L.map("map-id", {
    center: coordinates,
    zoom: 13,
    layers: [lightmap, petFind]
  });

  // Create a layer control, pass in the baseMaps and overlayMaps. Add the layer control to the map
  L.control.layers(baseMaps, overlayMaps, {
    collapsed: false
  }).addTo(map);
};

function createMarkers(pets, coordinates) {
  // Pull the "stations" property off of response.data

  // Initialize an array to hold pet markers
  var petMarkers = [];

  // Loop through the stations array
  for (var index = 0; index < pets.length; index++) {
      var pet = pets[index];

      // For each station, create a marker and bind a popup with the station's name
      var petMarker = L.marker([pet.coordinates[0], pet.coordinates[1]])
      .bindPopup("<h4><a href=/pet/" + pet.id + ">" + pet.title + "</a><h4>");

      // Add the marker to the petMarkers array
      petMarkers.push(petMarker);
  };

  // Create a layer group made from the pet markers array, pass it into the createMap function
  createMap(L.layerGroup(petMarkers), coordinates);
};
