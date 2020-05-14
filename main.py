import cv2
import random
import numpy as np
from flask import Flask, make_response, render_template, request
from .config import Config
import os


app = Flask(__name__)
config = Config("config.cfg")


def _get_all_sprites():
    sprites = []
    sprite_files = os.listdir(config.sprites_dir)
    i = 0
    for sprite_file in sprite_files:
        sprite = cv2.imread(os.path.join(config.sprites_dir, sprite_file), cv2.IMREAD_UNCHANGED)
        if i == 0:
            print(sprite)
            i +=1
        sprites.append(sprite)
    return sprites


# https://note.nkmk.me/en/python-opencv-hconcat-vconcat-np-tile/
def _concat_sprites(im_list_2d):
    return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])


def _merge_images(image1, image2):
    #return cv2.addWeighted(image1, 0.5, image2, 0.5, 0.0)
    rows,cols,channels = image2.shape
    roi = image1[0:rows, 0:cols ]
    img2gray = cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 200, 255, cv2.THRESH_BINARY_INV)
    mask_inv = cv2.bitwise_not(mask)
    img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    img2_fg = cv2.bitwise_and(image2, image2, mask=mask)
    out_img = cv2.add(img1_bg,img2_fg)
    return out_img


def generate_image(rows, columns, iterations, color_selection_mode, colors):
    sprites = _get_all_sprites()
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

            r, g, b, a = sprite.T
            black_areas = (r == 0) & (g == 0) & (b == 0) & (a == 255)
            sprite[..., :][black_areas.T] = color
            #sprite[np.where((sprite == [0, 0, 0, 255]).all(axis=2))] = color
            
            row.append(sprite)
        sprite_grid.append(row)
    
    # build the image using the 2d array of sprites
    image = _concat_sprites(sprite_grid)
    
    # run this function recursively until we get through all the requested iterations
    while iterations > 1:
        image = _merge_images(image, generate_image(rows, columns, 1, color_selection_mode, colors))
        iterations -= 1

    # return cv2 image
    return image


@app.route('/')
def builder():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    """
    Returns a collage of sprites as an image.
    
    Accepts POST requests with a JSON body. See README.md for more details
    """
    data = request.json
    if data is None:
        response = make_response("you fudged up")
        return response, 400
    rows = data.get('rows', 8)
    columns = data.get('columns', 8)
    seed = data.get('seed', None)
    iterations = data.get('iterations', 2)
    color_selection_mode = data.get("colorSelectionMode", "random")
    colors = data.get('colors', [[0, 0, 0], [255, 0, 0], [0, 255, 0], [0, 0, 255]])
    # convert colors from RGB to BGR (used by cv2)
    for color in colors:
        color.reverse()
        # add alpha channel
        color += [255]
    
    # set seed here so it influences request from beginning to end
    random.seed(seed)

    image = generate_image(rows, columns, iterations, color_selection_mode, colors)
    print(image)
    _, buffer = cv2.imencode('.png', image)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/png'
    
    return response
