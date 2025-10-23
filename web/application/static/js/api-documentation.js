const baseURL = 'https://france-energie.koyeb.app/api/v1'
// Playground
const jsonContainer = document.querySelector('#requests pre.json-content');
const playgroundTabsForm = document.querySelector('form#endpoints-menu');
const playgroundRequestsUrl = document.querySelector('#requests-url')
const playgroundRequestsForms = document.querySelector('#requests form');



const data = {
    inference_time_sec: 0.1,
    result: {
        prediction: {
            cout_chauffage_eur: 20
        },
        informations: {
            adresse: "30 rue de la République, 69001 Lyon",
            insee: 69123,
            coordinates: {
                longitude: 34.564830,
                latitude: 4.586023
            }
        }
    }
}

// Function to create the API requests URL
function getRequestsURL(endpoint) {

    // TODO: call python to compute the URL instead
    // or do it in JS but compoute the URL with the params (?value_1=)
    return baseURL + '/' + endpoint

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

var str = JSON.stringify(data, undefined, 4);
jsonContainer.innerHTML = syntaxHighlight(str);




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

// Copy json when clicked
const copyButton = document.querySelector('#copy-json');
copyButton.addEventListener('click', () => {
    const text = jsonContainer.textContent;
    copyToClipboard(text);
});