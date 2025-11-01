let baseURL = 'https://france-energie.koyeb.app/api/v1'
// baseURL = 'api/v1' // TRY IT OUT ONLY !!!

// Playground
const statusCodeElement = document.querySelector('.status-code');
const jsonContainer = document.querySelector('#requests pre.json-content');
const playgroundTabsForm = document.querySelector('form#endpoints-menu');
const playgroundRequestsUrl = document.querySelector('#requests-url')
const playgroundRequestsForms = document.querySelector('#requests form');





// Function to get the values of active playground subform
function getSubFormValues() {

    const endpoint = playgroundRequestsForms.dataset.tabView;
    const currentSubForm = playgroundRequestsForms.querySelector(`.sub-form[data-tab="${endpoint}"]`);
    const inputs = currentSubForm.querySelectorAll('input');
    const selects = currentSubForm.querySelectorAll('select');

    const formData = new FormData();
    inputs.forEach(input => {
        if (input.value != "") {
            formData.append(input.name, input.value);
        }
    });
    selects.forEach(select => {
        if (select.value != "") {
            formData.append(select.name, select.value);
        }
    });

    return [endpoint, Object.fromEntries(formData.entries())];
}

// Function to create the API requests URL
function getRequestsURL(endpoint, values) {

    const searchParams = new URLSearchParams(values);
    const requestUrl = `${baseURL}/${endpoint}?${searchParams.toString()}`;
    return requestUrl

}

// Function to request an API call
async function requestsAPI(url) {

    console.log(url);

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const json = await response.json();
        return {
          statusCode: response.status,
          json
        };
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        throw error;
    }

}

// Function to format the json API response (color highlighting)
function syntaxHighlight(json) {
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
            } else {
                cls = 'string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'boolean';
        } else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}





// Switch between Playground tabs when clicked
const playgroundTabs = playgroundTabsForm.querySelectorAll('li');
playgroundTabs.forEach(tab => {
    tab.addEventListener('click', () => {

        const endpoint = tab.dataset.view;
        playgroundRequestsForms.dataset.tabView = endpoint;

        playgroundRequestsUrl.textContent = getRequestsURL(endpoint);

        const currentActive = playgroundTabsForm.querySelector('.active');
        currentActive.classList.remove('active');
        tab.classList.add('active');
    });
});

// Requests API when `Executer` button clicked
playgroundRequestsForms.addEventListener('submit', async function(event) {

    event.preventDefault();

    const [endpoint, values] = getSubFormValues();
    const url = getRequestsURL(endpoint, values);
    const response = await requestsAPI(url);

    if (!response) {
        statusCodeElement.textContent = "";
        return
    }
    
    // Update requests URL
    playgroundRequestsUrl.textContent = url;
    // Display status code
    statusCodeElement.textContent = response.statusCode;
    statusCodeElement.dataset.status = response.statusCode;
    // Display content in json element
    const str = JSON.stringify(response.json, undefined, 4);
    jsonContainer.innerHTML = syntaxHighlight(str);
});

// Copy json when clicked
const copyButtons = document.querySelectorAll('#copy-json');
copyButtons.forEach(button => {
    button.addEventListener('click', (event) => {
        const parentElement = event.currentTarget.parentElement;
        const codeElement = parentElement.querySelector('pre');
        const text = codeElement.textContent;
        copyToClipboard(text);
    });
});