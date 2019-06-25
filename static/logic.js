function createMap(petFind) {

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
      center: [41.881832, -87.623177],
      zoom: 12,
      layers: [lightmap, petFind]
    });
  
    // Create a layer control, pass in the baseMaps and overlayMaps. Add the layer control to the map
    L.control.layers(baseMaps, overlayMaps, {
      collapsed: false
    }).addTo(map);
};
  
function createMarkers(response) {
    // Pull the "stations" property off of response.data
    var stations = response.data.stations;

    // Initialize an array to hold pet markers
    var petMarkers = [];

    // Loop through the stations array
    for (var index = 0; index < stations.length; index++) {
        var station = stations[index];

        // For each station, create a marker and bind a popup with the station's name
        var petMarker = L.marker([station.lat, station.lon])
        .bindPopup("<h3>" + station.name + "<h3><h3>Capacity: " + station.capacity + "<h3>");

        // Add the marker to the petMarkers array
        petMarkers.push(petMarker);
    };

    // Create a layer group made from the pet markers array, pass it into the createMap function
    createMap(L.layerGroup(petMarkers));
};

console.log('JS FIle loaded');

var url = '/pets/cat';

console.log('1');

d3.json(url).then(function(response) {
    console.log('adwa');
    console.log(response);
    console.log('adfnwalkd');
    createMarkers(response);
    
});