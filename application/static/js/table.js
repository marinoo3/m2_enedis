// Table element
const tableElement = document.querySelector('#data');

// Filters elements
const filterForm = document.querySelector('#table-form');
const stateInput = filterForm.querySelector('#departement');
const yearSelect = filterForm.querySelector('#year');
const countLabel = document.querySelector('#count > p');
const densitySlider = filterForm.querySelector('#density-slider');
const altitudeSlider = filterForm.querySelector('#altitude-slider');

// Pagination elements
const indexForm = document.querySelector('form#pagination');
const previousButton = indexForm.querySelector('button[name="previous"]');
const nextButton = indexForm.querySelector('button[name="next"]');
const pageInput = indexForm.querySelector('input[name="index"]');

// Table size
let size = 15






// Create filter sliders
noUiSlider.create(densitySlider, {
	start: [scales['densite']['min'], scales['densite']['max']],
	connect: true,
	step: 1,
	tooltips: [wNumb({decimals: 0}), wNumb({decimals: 0})],
	range: {
		'min': scales['densite']['min'],
		'80%': (scales['densite']['max'] - scales['densite']['min']) / 50,
		'max': scales['densite']['max']
	}
});
noUiSlider.create(altitudeSlider, {
	start: [scales['altitude']['min'], scales['altitude']['max']],
	connect: true,
	step: 1,
	tooltips: [wNumb({decimals: 0, suffix: ' m'}), wNumb({decimals: 0, suffix: ' m'})],
	range: {
		'min': scales['altitude']['min'],
		'80%': (scales['altitude']['max'] - scales['altitude']['min']) / 5,
		'max': scales['altitude']['max']
	}
});





// Update silders range
function updateSliders() {
	densitySlider.noUiSlider.updateOptions({
		start: {
			'min': scales['densite']['min'],
			'max': scales['densite']['max']
		}
	})
}

// Function to fill the table with data given a specific page index
function fillTable(data=mapData, index=0) {

	// Update count
	countLabel.textContent = data.length;

	// Empty table
	trList = tableElement.querySelectorAll('tr:not(.header)');
	trList.forEach(element => {
		element.remove();
  	});

	const offset = index * size
	const subset = data.slice(offset, offset + size);
	const selectedKeys = ["code_commune", "nom_commune", "annee", "nombre_de_logements", "densite", "altitude", "conso_total_mwh", "conso_moyenne_mwh"];

	subset.forEach(item => {

		const tr = document.createElement('tr');

		selectedKeys.forEach(key => {
			if (item.hasOwnProperty(key)) {
				const td = document.createElement('td');
				td.textContent = item[key];
				tr.appendChild(td)
			}
		});

		tableElement.appendChild(tr);
	});
}

// Function to update the table when filtered
async function filterTable() {

	const filters = JSON.stringify([
		{ column: 'code_commune', type: 'startwith', value: stateInput.value },
		{ column: 'annee', type: 'startwith', value: yearSelect.value.toString() },
		{ column: 'densite', type: 'inrange', value: densitySlider.noUiSlider.get() },
		{ column: 'altitude', type: 'inrange', value: altitudeSlider.noUiSlider.get() }
	]);

	const queryString = new URLSearchParams({ // build query
        filters
    }).toString();

	// Requests filtered to python API

	const response = await fetch('/api/map_data/?' + queryString, {
		method: 'GET',
		headers: { 'Content-Type': 'application/json' }
	});

	if (!response.ok) {
		throw new Error('Network response was not ok');
	}

	content = await response.json();
	mapData = content['data']
	scales = content['scales']

	//updateSliders();
	fillTable();
	drawMap();
}

// Function to change the current table page
function changePage(page, data=mapData) {

	let index = page - 1;

	if (index == 0) {
		previousButton.disabled = true;
	} else {
		previousButton.disabled = false;
	}

	if (index*size >= data.length) {
		index = Math.floor(data.length / size);
		page = index + 1; 
		nextButton.disabled = true;
	} else {
		nextButton.disabled = false;
	}

	fillTable(data=data, index=index);
	pageInput.value = page;
}




// Update the table when filters applies
stateInput.addEventListener('change', () => {
	filterTable();
});
yearSelect.addEventListener('change', () => {
	filterTable();
});
densitySlider.noUiSlider.on('change', () => {
	filterTable();
});
altitudeSlider.noUiSlider.on('change', () => {
	filterTable();
});


// Update the table when changing page index
previousButton.addEventListener('click', () => {
	let newPage = parseInt(pageInput.value) - 1
	changePage(newPage);
});
nextButton.addEventListener('click', () => {
	let newPage = parseInt(pageInput.value) + 1;
	changePage(newPage);
});
pageInput.addEventListener('change', (e) => {
	changePage(e.target.value);
});




// Init the default table to page 1
fillTable();