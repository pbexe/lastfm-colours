# https://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user=pbexe&api_key=***REMOVED***&format=json&period=1month&limit=100

import colorsys
import io
import math
import random
import urllib
from pprint import pprint

import requests
from colorthief import ColorThief
from PIL import Image

r = requests.get("https://ws.audioscrobbler.com/2.0/",
                 {
                     "method": "user.gettopalbums",
                     "user": "pbexe",
                     "api_key": "***REMOVED***",
                     "format": "json",
                     "period": "1month",
                     "limit": 105
                 }).json()

albums = []

for album in r["topalbums"]["album"]:
    albums.append(album["image"][2]["#text"])


album_images = []


for image in albums:
    try:
        path = io.BytesIO(urllib.request.urlopen(image).read())
        rgb = ColorThief(path).get_color()
        hlsval = colorsys.rgb_to_hls(*rgb)
        image = Image.new("RGB", (174,174), rgb)
        album_images.append((image, hlsval, rgb))
        # image.show()
    except ValueError:
        pass


# album_images = sorted(album_images, key=lambda x: step(*x[2],8))
album_images = sorted(album_images, key=lambda x: x[2])[:100]

albums_twice_sorted = []

for i in range(0,91,10):
    albums_twice_sorted += sorted(album_images[i:i+10], key=lambda x: x[1][1])

def create_collage(width, height, listofimages):
    cols = 10
    rows = 10
    thumbnail_width = width//cols
    thumbnail_height = height//rows
    size = thumbnail_width, thumbnail_height
    new_im = Image.new('RGB', (width, height))
    ims = []
    for p in listofimages:
        try:
            im = p[0]
            im.thumbnail(size)
            ims.append(im)
        except ValueError:
            print("ERROR: MISSING URL!!")
    i = 0
    x = 0
    y = 0
    for col in range(cols):
        for row in range(rows):
            print(i, x, y)
            try:
                new_im.paste(ims[i], (x, y))
            except IndexError:
                pass
            i += 1
            y += thumbnail_height
        x += thumbnail_width
        y = 0

    new_im.save("CollageColours.jpg")

create_collage(1740, 1740, albums_twice_sorted)
