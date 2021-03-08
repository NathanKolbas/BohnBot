import sys
from enum import Enum
from google_images_search import GoogleImagesSearch
from PIL import Image
from pygifsicle import optimize
import io
import json
import os
from os.path import isfile, join
import re
import requests
import tempfile
from urllib.parse import urlparse


# Static methods
def atoi(text):
    """
    atio converts string to an integer. The naming convention comes from C

    :param text: The string you want to convert
    :return: The integer version of the string
    """
    return int(text) if text.isdigit() else text


def is_valid_url(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False


def natural_sort(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def translate_center(point, file):
    image_size = file.convert('RGB').size
    return int(point[0] - (image_size[0] / 2)), int(point[1] - (image_size[1] / 2))


def warning(message):
    message = f"\033[93mWARNING:\033[0m {message}"
    print(message)
# Static methods END


class Gifs(Enum):
    """
    This class is used to specify each type of gif that we can create stored as an enum.
    The enum is a dictionary containing the necessary information about how the gif is
    to be created.
    """
    AMONG_US_KILL = {
        'points': [(197, 174), (197, 174), (197, 174), (197, 174), (197, 174), (197, 174), (224, 162), (291, 176),
                   (291, 176), (315, 219), (316, 216), (319, 215), (322, 218), (322, 218), (321, 218), (321, 218),
                   (321, 218), (321, 218), (321, 218), (321, 218), (321, 218), (321, 218), (316, 192), (316, 192),
                   (316, 192), (316, 192), (316, 192), (316, 192), (316, 192), (316, 192), (316, 192), None, None,
                   None, None, None, None, None, None, None, None, None, None, None, None, None],
        'frames_path': 'among_us/',
        'custom_image_size': (64, 64),
        'fps': 25
    }
    CHALLENGER = {
        'points': [None if n < 7 else (350, 140) for n in range(76)],
        'frames_path': 'challenger/',
        'custom_image_size': (120, 120),
        'fps': 25
    }


class CreateGif:
    def __init__(self, custom_image=None):
        self._working_directory = os.getcwd()
        self._custom_image = custom_image
        with open('config.json') as f:
            self.config = json.load(f)

    @property
    def custom_image(self):
        return self._custom_image

    @custom_image.setter
    def custom_image(self, image):
        self._custom_image = image

    def _set_image(self, gif):
        custom_image = self._custom_image
        output = 'default.png'

        if custom_image:
            try:
                output = io.BytesIO()
                if is_valid_url(str(custom_image)):
                    # A URL or the discord image was given
                    # The header is used to spoof the website into thinking someone is using a browser.
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
                    }
                    response = requests.get(custom_image, headers=headers)
                    output.write(response.content)
                else:
                    # Text was given, lets find an image using Google
                    output = self.google_image_search(custom_image)
            except:
                print(sys.exc_info())
                output = 'default.png'

        image = Image.open(output).convert('RGBA')
        image.load()
        image.thumbnail(size=gif['custom_image_size'])
        return image

    def generate_gif(self, gif):
        # Local vars
        gif = gif.value
        frames = []
        custom_image = self._set_image(gif)

        # Get the frames for the gif and sort from 1 to n
        frames_path = f"{self._working_directory}/Frames/{gif['frames_path']}"
        filenames = [os.path.join(frames_path, f) for f in os.listdir(frames_path) if isfile(join(frames_path, f))]
        filenames.sort(key=natural_sort)

        # Verify that the number of points match the number of frames
        if len(filenames) != len(gif['points']):
            raise ValueError(f"The number of frames and files do not match! Files: {len(filenames)}, points: "
                             f"{len(gif['points'])}")

        # Create each frame
        overlay_points = gif['points']
        for n in range(len(filenames)):
            # Check if None
            if overlay_points[n]:
                background = Image.open(filenames[n]).convert('RGBA')
                background.paste(custom_image, translate_center(overlay_points[n], custom_image), custom_image)
                frames.append(background)
            else:
                frames.append(Image.open(filenames[n]).convert('RGBA'))

        # Generate the gif
        file = tempfile.NamedTemporaryFile(delete=False, suffix='.gif')
        frames[0].save(file.name,
                       format='GIF',
                       append_images=frames[1:],
                       save_all=True,
                       duration=1000 / gif['fps'],
                       loop=0)
        # Optimize the gif using gifsicle to reduce file size
        try:
            optimize(file.name)
        except FileNotFoundError:
            warning('Unable to optimize the gif. Please make sure gifsicle is installed.\nContinuing without '
                    'optimization...\n')

        return file

    def google_image_search(self, search_text):
        """
        Searches for an image with the given search text and downloads it into a io.BytesIO object
        :param search_text: The text you would like to search for in Google images
        :return: Returns a io.BytesIO with the given image
        """
        output = io.BytesIO()
        gis = GoogleImagesSearch(self.config['GIS_DEV_API_KEY'], self.config['GIS_PROJECT_CX'])
        _search_params = {
            'q': search_text,
            'num': 1,
            'safe': 'off',
            'imgSize': 'SMALL'
        }
        gis.search(_search_params)
        image = gis.results()[0]
        output.seek(0)  # Tell the BytesIO object to go back to address 0
        image.copy_to(output)
        output.seek(0)  # Go back to address 0 again so PIL can read it from start to finish
        return output
