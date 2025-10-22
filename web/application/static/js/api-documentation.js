const jsonContainer = document.querySelector('pre.json-content');



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