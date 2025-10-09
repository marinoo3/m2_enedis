// Init the map
const map = L.map('map', {maxZoom: 14}).setView([46.603354, 1.888334], 6);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

const mapElement = document.querySelector('#map'); // Map element
var heat = null; // Heatmap layer
var irisData = [] // Data for zoomed view

// Load Geosearch provider for searching places
const provider = new GeoSearch.OpenStreetMapProvider();







// Function to draw a heatmap layer
function drawHeatMap(value, data=mapData) {

    const selectedKeys = ["latitude", "longitude", value];
    const formatedData = data.map(item => selectedKeys.map(key => item[key]));

    let h = L.heatLayer(formatedData, { radius: 20, blur: 20, max: 15}).addTo(map);
    return h;
}

// Lazy function to requests the python API and progressively fetch the map data
async function fetchMapData(queryString, mapValue) {

    mapElement.classList.add('waiting');

    const controller = new AbortController();
    const signal = controller.signal;

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
    
            while (!done) {
    
                if (mapElement.dataset.currentMapData != "adresse") {
                    controller.abort();
                    break
                }
    
                const chunk = decoder.decode(value);
                irisData = JSON.parse(chunk);
    
                map.removeLayer(heat);
                heat = drawHeatMap(mapValue, irisData);
    
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
        }
    } finally {
        mapElement.classList.remove('waiting', 'fetching');
    }
}

// Update map adresses with current bounding box
function updateMapAdresses(bbox) {

    mapElement.dataset.bbox = JSON.stringify(bbox);

    let queryString = new URLSearchParams({ // build query
        minLongitude: bbox._southWest.lng,
        minLatitude: bbox._southWest.lat,
        maxLongitude: bbox._northEast.lng,
        maxLatitude: bbox._northEast.lat
    }).toString();

    fetchMapData(queryString, mapValueSelect.value);
}




// Search the map with the search bar
const mapForm = document.querySelector('form#map-form');
const input = mapForm.querySelector('input[name="place"]');
mapForm.addEventListener('submit', async (event) => {

    event.preventDefault();

    const results = await provider.search({ query: input.value });
    map.fitBounds(results[0].bounds)
    input.blur()
});

// Change map value with the select
const mapValueSelect = document.querySelector('#map select#map-value');
mapValueSelect.addEventListener('change', (e) => {
    map.removeLayer(heat);
    if (mapElement.dataset.currentMapData == "adresse") {
        heat = drawHeatMap(e.target.value, irisData);
    } else {
        heat = drawHeatMap(e.target.value);
    }
});

// Update map data when zoom point reached
map.addEventListener('zoomend', () => {

    const zoom = map.getZoom()
    console.log(zoom);
    const currentMapData = mapElement.dataset.currentMapData;

    if (zoom > 10 & currentMapData != "adresse") {

        mapElement.dataset.currentMapData = "adresse";

        let bbox = map.getBounds();
        updateMapAdresses(bbox);

    } else if (zoom <= 10 & currentMapData != "communes") {

        mapElement.dataset.currentMapData = "communes";
        mapElement.classList.remove("waiting", "fetching");

        map.removeLayer(heat);
        heat = drawHeatMap(mapValueSelect.value);
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
const downloadButton = document.querySelector('a.download-button');
downloadButton.addEventListener('click', async () => {
    const width = mapElement.offsetWidth;
    const height = mapElement.offsetHeight;
    const dataURL = await domtoimage.toPng(mapElement, { width, height });
    const fileName = 'map-' + mapValueSelect.value + '.png'
    downloadDataUrl(dataURL, fileName);
});





// Create the default heatmap on `conso_moyenne_mwh`
heat = drawHeatMap('score_moyenne_conso');