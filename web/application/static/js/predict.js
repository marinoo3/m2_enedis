// Init the map
const map = L.map('map').setView([45.75, 4.85], 17);
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(map);
// Load Geosearch provider for searching places
const provider = new GeoSearch.OpenStreetMapProvider();

// Map element
const mapElement = document.querySelector('#map');
// Form
const form = document.querySelector('#predict-form');





// Function to requests python predict
async function fetchPredict(values) {

    const queryString = new URLSearchParams(values).toString();

    const response = await fetch('/ajax/predict?' + queryString, {
		method: 'GET',
		headers: { 'Content-Type': 'application/json' }
	});

	if (!response.ok) {
		throw new Error('Network response was not ok');
	}

	content = await response.json();
    return content
}




// Predict on form submit
form.addEventListener('submit', async function(event) {
    event.preventDefault();

    // Create a FormData object from the form
    const formData = new FormData(this);

    // Loop through the entries in the FormData object
    const formValues = {};
    formData.forEach((value, key) => {
        formValues[key] = value;
    });

    // Get coordinates from address
    const results = await provider.search({ query: formValues.address + ', France' });
    const place = results[0];

    // Add coordinates to formValues
    formValues['latitude'] = place.y;
    formValues['longitude'] = place.x;

    // Add marker to map
    map.fitBounds(place.bounds);
    const marker = L.marker([place.y, place.x]).addTo(map);
    marker.bindPopup(`<h1>${place.label}</h1>`);

    // Call python to predict results
    const result = await fetchPredict(formValues);
})