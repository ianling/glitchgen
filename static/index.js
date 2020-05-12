function generate(e) {
    e.preventDefault();
    
    let form = document.getElementById("form").elements;
    let data = {};
    for(let i = 0; i < form.length; i++) {
        let field = form.item(i);
        if(field.name.length < 1) {
            continue;
        }
        data[field.name] = (field.dataset.type === "int" ? parseInt(field.value) : field.value);
    }
    
    let http = new XMLHttpRequest();
    http.responseType = "blob";
    http.onreadystatechange = function () {
        if (http.readyState === 4 && http.status === 200) {
            // insert the new image
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