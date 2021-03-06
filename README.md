# glitchgen
Randomly generates glitch pattern collages.

Runs a Flask webserver with a small GUI for modifying image generation parameters,
and exposes a JSON API endpoint for creating images programmatically.

Collages are made up of sprites, which are loaded from the sprites folder and added to the collage at random. 
Black pixels in sprites are replaced with user-specified colors.

![Example](https://user-images.githubusercontent.com/830113/81886722-44a8ee00-9552-11ea-9c32-aaeba72f13e8.png)

# requirements
- python3
- flask
- opencv-python
- numpy

# usage
Run main.py using Flask, then visit http://127.0.0.1:5000 in your web browser.

Linux:
```bash
$ export FLASK_APP=main.py
$ flask run
```

On Windows, run `run.bat`

# api
The `/generate` endpoint accepts POST requests with JSON payloads and returns a .PNG image.

Example JSON payload (with comments):

```hjson
{
    # number of rows of sprites. integer
    "rows": 10,

    # number of columns of sprites. integer
    "columns": 10,
    
    # RNG seed (null to select a random seed on the server). string or null
    "seed": "abcdefg",
    
    # can be used to generate multiple full images and overlap them. integer
    "iterations": 2,
    
    # controls how colors are selected for sprites. string
    # "random" = selects colors at random from available colors array
    # "sequential" = selects colors in the order provided in the array, repeating when it reaches the end of the array
    "colorSelectionMode": "random",
    
    # which colors you want to apply to the sprites. an array of RGB color arrays
    "colors": [ [0, 0, 0], [255, 0, 0], [0, 255, 0] ]
}
```

# todo
To-do list in no particular order:

- random chance to overlap sprites when doing multiple interations (so some sprites will not be overlapped)
- random chance to rotate sprites
- multiple colors in each sprite
- add some way to show the seed used when the server randomly generates one (or generate one client-side instead)
