// Tbale element
const tableElement = document.querySelector('#data');

// Pagination elements
const indexForm = document.querySelector('form#pagination');
const previousButton = indexForm.querySelector('button[name="previous"]');
const nextButton = indexForm.querySelector('button[name="next"]');
const pageInput = indexForm.querySelector('input[name="index"]');

// Table size
let size = 15


// Function to fill the table with data given a specific page index
function fillTable(data=mapData, index=0) {

	// Empty table
	trList = tableElement.querySelectorAll('tr:not(.header)');
	trList.forEach(element => {
		element.remove();
  });

	const offset = index * size
	const subset = data.slice(offset, offset + size);
	const selectedKeys = ["code_commune", "nom_commune", "nombre_de_logements", "conso_total_mwh", "conso_moyenne_mwh"];

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