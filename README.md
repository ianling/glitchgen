# glitchgen
Randomly generates glitch pattern collages.

Runs a Flask webserver with a small GUI for modifying image generation parameters,
and exposes a JSON API endpoint for creating images programmatically.

Sprites are loaded from the sprites folder and added to the collage at random. 
Black pixels in sprites are replaced with user-specified colors.

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

```json
{
    # number of rows of sprites. integer
    "rows": 10,

    # number of columns of sprites. integer
    "columns": 10,
    
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
    - overlap multiple full grids with each other
    - random chance to overlap individual sprites (like a "corruptor" or something)
    - multiple colors in each sprite