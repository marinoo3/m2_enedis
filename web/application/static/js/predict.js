// Init the map
const map = L.map('map').setView([45.75, 4.85], 17);
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(map);
// Load Geosearch provider for searching places
const provider = new GeoSearch.OpenStreetMapProvider();

// Map element
const mapElement = document.querySelector('#map');
// Form
const form = document.querySelector('#predict-form');
let place = null;
// Result
const resultElement = document.querySelector('.result');
const dpeElement = resultElement.querySelector('.dpe');
const euroElement = resultElement.querySelector('.consommation .euro');


dpeElement


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

// Function to update the result on the HTML
function updateResult(result) {

    let dpe_type = 'passoire';

    if (result.passoire == false) {
        dpe_type = 'non-passoire';
    }

    dpeElement.dataset.selection = dpe_type;
    euroElement.textContent = result.consommation;
}



// Search place when searching postal code
const searchInput = form.querySelector('#address');
searchInput.addEventListener('change', async function(event) {

    const address = event.currentTarget.value + ', France'

    // Store first result in `place`
    const results = await provider.search({ query: address + ', France' });
    place = results[0];

    // Add point marker to map
    map.fitBounds(place.bounds);
    const marker = L.marker([place.y, place.x]).addTo(map);
    marker.bindPopup(`<h1>${address}</h1><p>${place.label}</p>`);
});


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

    // Add coordinates to formValues
    formValues['latitude'] = place.y;
    formValues['longitude'] = place.x;

    // Call python to predict results
    resultElement.classList.add('loading');
    const result = await fetchPredict(formValues);
    resultElement.classList.remove('loading');

    // Display results
    updateResult(result);
})