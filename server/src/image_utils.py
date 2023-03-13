from PIL import Image
from enum import Enum

import requests
import urllib.request as request



class Rotation(Enum):
    HORIZONTAL = 1
    MIRROR_HORIZONTAL = 2
    ROTATE_180 = 3
    MIRROR_VERTICAL = 4
    MIRROR_AND_ROTATE_270 = 5
    ROTATE_90 = 6
    MIRROR_AND_ROTATE_90 = 7
    ROTATE_270 = 8

def retrieve_image(image_url, output_path):
    # img_data = requests.get(image_url).content
    # with open(output_path, 'wb') as handler:
    #     handler.write(img_data)
    
    r = request.Request(image_url)
    f = request.urlopen(r)
    with open(output_path, 'wb') as handler:
        handler.write(f.read())


def convert_image(input_path, output_path):
    '''converts an image to RGBA format'''
    image = Image.open(input_path)
    image.convert("RGBA").save(output_path)

def resize_image(input_path, output_path, width, height):
    image = Image.open(input_path)
    image_resize_lanczos = image.resize((width, height), Image.LANCZOS)
    image_resize_lanczos.save(output_path)

def get_shape(input_path):
    '''returns the shape of an image'''
    image = Image.open(input_path)
    exif = image._getexif()
    # width, height, exif
    return image.width, image.height, exif

def preprocess(image_path):
    image_dir = "../../images"
    input_path = 'tmp/input.png'
    output_path = 'tmp/converted.png'
    image = Image.open(f'{image_dir}/{image_path}')
    image.save(input_path)
    convert_image(input_path, output_path)
    return output_path