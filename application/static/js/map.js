// Init the map
const map = L.map('map', {maxZoom: 14}).setView([46.603354, 1.888334], 6);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

var layer = null; // Map layer (heatmap or points)
var irisData = [] // Data for zoomed view

// Load Geosearch provider for searching places
const provider = new GeoSearch.OpenStreetMapProvider();

// Map element
const mapElement = document.querySelector('#map');
// Map form elements
const mapForm = document.querySelector('form#map-form');
const placeInput = mapForm.querySelector('input[name="place"]');
const mapStyleSelect = mapForm.querySelector('select[name="map-style"]')
// Heatmap value select element
const mapValueSelect = document.querySelector('#map select#map-value');
// Map download button element
const downloadButton = document.querySelector('a.download-button');








// Function to draw a heatmap layer
function drawHeatMap(value, data=mapData) {

    const selectedKeys = ["latitude", "longitude", value];
    const formatedData = data.map(item => selectedKeys.map(key => item[key]));

    let heat = L.heatLayer(formatedData, { radius: 20, blur: 20, max: 15}).addTo(map);
    return heat;
}

// Function to draw points layer
function drawPointsMap(data=mapData) {

    var markers = L.markerClusterGroup();

    data.forEach(function(item) {

        // Create HTML for popup content
        let popupContent = `<h1>${item.nom_commune}</h1>`;

        var marker = L.marker([item.latitude, item.longitude]).bindPopup(popupContent);
        markers.addLayer(marker);
    });

    map.addLayer(markers);
    return markers

}

// Function to draw map visualisation layer
function drawMap() {
    
    if (layer != null) {
        map.removeLayer(layer); // remove previous map layer
    }

    if (mapElement.dataset.currentMapData == "adresse") {
        data = irisData;
    } else {
        data = mapData;
    }

    const mapStyle = mapStyleSelect.value
    if (mapStyle == "heatmap") {
        const mapValue = mapValueSelect.value;
        layer = drawHeatMap(mapValue, data);
    } else {
        layer = drawPointsMap(data);
    }

    return layer;

}

// Lazy function to requests the python API and progressively fetch the map data
async function fetchMapData(queryString) {

    mapElement.classList.add('waiting');

    const controller = new AbortController();
    const signal = controller.signal;

    console.log('requesting');

    const response = await fetch('/api/zoomed_map_data/?' + queryString, {
        method: 'GET',
        headers: {'Content-Type': 'application/json'},
        signal: signal
    });

    try {

        if (response.ok) {

            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');
            let { value, done } = await reader.read();
            var chunk = null // TO REMOVE FROM HERE
    
            while (!done) {
    
                if (mapElement.dataset.currentMapData != "adresse") {
                    controller.abort();
                    break
                }
    
                chunk = decoder.decode(value);
                irisData = JSON.parse(chunk);
    
                layer = drawMap();
    
                mapElement.classList.remove('waiting');
                mapElement.classList.add('fetching');
    
                ({ value, done } = await reader.read());
            }
    
        } else {
            throw new Error('HTTP Error: ' + response.status);
        }

    } catch (error) {
        if (error.name === 'AbortError') {
            console.log('Request was aborted.');
        } else {
            console.log('Fetch error: ' + error);
            console.log(chunk);
        }
    } finally {
        mapElement.classList.remove('waiting', 'fetching');
    }
}

// Update map adresses with current bounding box
function updateMapAdresses(bbox) {

    mapElement.dataset.bbox = JSON.stringify(bbox);

    const queryString = new URLSearchParams({ // build query
        minLongitude: bbox._southWest.lng,
        minLatitude: bbox._southWest.lat,
        maxLongitude: bbox._northEast.lng,
        maxLatitude: bbox._northEast.lat
    }).toString();

    fetchMapData(queryString);
}




// Search the map with the search bar
mapForm.addEventListener('submit', async (event) => {

    event.preventDefault();

    const results = await provider.search({ query: placeInput.value });
    map.fitBounds(results[0].bounds)
    placeInput.blur()
});

// Swtich between map style (heatmap or points map)
mapStyleSelect.addEventListener('change', () => {
    drawMap();
});

// Change map value with the select
mapValueSelect.addEventListener('change', () => {
    drawMap();
});

// Update map data when zoom point reached
map.addEventListener('zoomend', () => {

    const zoom = map.getZoom()
    const currentMapData = mapElement.dataset.currentMapData;

    if (zoom > 10 & currentMapData != "adresse") {

        mapElement.dataset.currentMapData = "adresse";

        let bbox = map.getBounds();
        updateMapAdresses(bbox);

    } else if (zoom <= 10 & currentMapData != "communes") {

        mapElement.dataset.currentMapData = "communes";
        mapElement.classList.remove("waiting", "fetching");
        layer = drawMap();
    }
})

// Updqte map when moved around if zoomed
map.addEventListener('moveend', () => {

    const currentMapData = mapElement.dataset.currentMapData;

    if (currentMapData == "adresse") {
        
        const bboxLoaded = JSON.parse(mapElement.dataset.bbox);
        const coordinates = map.getCenter();

        // Is current map center out of loaded bounding box? (bools)
        const latOutbound = (coordinates.lat >  bboxLoaded._northEast.lat || coordinates.lat < bboxLoaded._southWest.lat);
        const lngOutbound = (coordinates.lng >  bboxLoaded._northEast.lng || coordinates.lng < bboxLoaded._southWest.lng);

        if (latOutbound || lngOutbound) {
            // If out of bounds, update maps adresse data
            let bbox = map.getBounds();
            updateMapAdresses(bbox);
        }
    }

});

// Save the map as image when download button is clicked
downloadButton.addEventListener('click', async () => {
    const width = mapElement.offsetWidth;
    const height = mapElement.offsetHeight;
    const dataURL = await domtoimage.toPng(mapElement, { width, height });
    const fileName = 'map-' + mapValueSelect.value + '.png'
    downloadDataUrl(dataURL, fileName);
});





// Create the default heatmap on `conso_moyenne_mwh`
layer = drawMap();