function generate(e) {
    e.preventDefault();
    
    let form = document.getElementById("form").elements;
    let data = {};
    
    data['rows'] = parseInt(form['rows'].value);
    data['columns'] = parseInt(form['columns'].value);
    data['seed'] = form['seed'].value ? form['seed'].value : null;
    data['iterations'] = parseInt(form['iterations'].value);
    data['colorSelectionMode'] = form['colorSelectionMode'].value;
    
    // parse and reformat the colors arrays before adding to JSON
    colors = form['colors[]'];
    // convert this to an array of strings
    if(colors.length === undefined) {
        // if the user only submitted a single color, we have to do something different
        colors = [colors.value];
    }
    else {
        colors = Array.from(colors).map(x => x.value);
    }
    // convert our array of strings to an array of RGB arrays
    colors = colors.map(x => rgbStringToArray(x));
    data['colors'] = colors;
    
    // POST the JSON to the /generate endpoint
    let http = new XMLHttpRequest();
    http.responseType = "blob";
    http.onreadystatechange = function () {
        if (http.readyState === 4 && http.status === 200) {
            // insert the new image into the page
            let blob = this.response;
            let imageElement = document.getElementById("image");
            let urlCreator = window.URL || window.webkitURL;
            let imageUrl = urlCreator.createObjectURL(blob);
            imageElement.src = imageUrl;
        }
    };
    http.open("POST", "/generate", true);
    http.setRequestHeader("Content-Type", "application/json");
    http.send(JSON.stringify(data));
    
    return false;
}

function rgbStringToArray(str) {
    // converts a string representing an RGB color like "255, 0, 0"
    // to an array of integers like [255, 0, 0]
    str = str.replace(/\s+/g, '');  // remove any spaces
    let rgb = str.split(",");
    rgb = rgb.map(x => parseInt(x));  // [255, 0, 0]
    
    return rgb;
}


function addColor(el) {
    let selectedDiv = el.parentNode;
    let colorsDiv = document.getElementById("colorInputs");
    let colorInput = selectedDiv.cloneNode(true);
    colorsDiv.insertBefore(colorInput, selectedDiv);
}

function removeColor(el) {
    let selectedDiv = el.parentNode;
    let colorsDiv = document.getElementById("colorInputs");
    // only let user remove a color if it will not leave them with zero colors
    if(colorsDiv.childElementCount > 1) {
        selectedDiv.remove();
    }
}