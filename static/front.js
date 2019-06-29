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
  var searchterm = inputElementsearchterm.property("value");

  console.log(zipcode);
  console.log(searchterm);

  
});
