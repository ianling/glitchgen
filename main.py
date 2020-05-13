import cv2
import random
import numpy as np
from flask import Flask, make_response, render_template, request
from .config import Config
import os


app = Flask(__name__)
config = Config("config.cfg")


def get_all_sprites():
    sprites = []
    sprite_files = os.listdir(config.sprites_dir)
    for sprite_file in sprite_files:
        sprite = cv2.imread(os.path.join(config.sprites_dir, sprite_file))
        sprites.append(sprite)
    return sprites

# https://note.nkmk.me/en/python-opencv-hconcat-vconcat-np-tile/
def concat_sprites(im_list_2d):
    return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])


@app.route('/')
def builder():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    """
    Returns a collage of sprites as an image.
    
    Accepts POST requests with a JSON body.
    The following variables can be submitted in the JSON body:
        rows=<int> [8]
        columns=<int> [8]
        colors=<two-dimensional array of colors in RGB format> [ [[0, 0, 0], [255, 0, 0], [0, 255, 0], [0, 0, 255]] ]
        
    Example POST request body:
        {"rows":5,"columns":7,colors:[[100,100,100],[0,0,0]]}  (generates an image with 5 rows and 7 columns, with only the colors gray and black)
    """

    sprites = get_all_sprites()
    data = request.json
    if data is None:
        response = make_response("you fudged up")
        return response, 400
    rows = data.get('rows', 8)
    columns = data.get('columns', 8)
    color_selection_mode = data.get("colorSelectionMode", "random")
    colors = data.get('colors', [[0, 0, 0], [255, 0, 0], [0, 255, 0], [0, 0, 255]])
    
    sprite_grid = []
    # generate rows of sprites
    for y in range(rows):
        row = []
        # fill the row with sprites
        for x in range(columns):
            sprite = random.choice(sprites).copy()
            
            # change color of the sprite
            if color_selection_mode == "random":
                color = random.choice(colors)
            elif color_selection_mode == "sequential":
                color = colors[x % len(colors)]
            sprite[np.where((sprite == [0, 0, 0]).all(axis=2))] = color
            
            row.append(sprite)
        sprite_grid.append(row)
    
    # build the final image using the 2d array of sprites
    final_image = concat_sprites(sprite_grid)
    
    # display the final image on the webpage
    _, buffer = cv2.imencode('.png', final_image)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/png'
    
    return response
