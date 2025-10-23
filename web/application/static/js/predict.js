// Init the map
const map = L.map('map').setView([45.75, 4.85], 17);
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(map);

// Map element
const mapElement = document.querySelector('#map');

console.log('hello world');