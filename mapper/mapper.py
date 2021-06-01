from typing import List, Tuple
import io
import json
import random
import os

import random
import requests
from PIL import Image


def get_image(url: str, filename: str, crop: bool = True):
    response = requests.get(url, timeout=5)

    with Image.open(io.BytesIO(response.content)) as img:
        if crop:
            img = img.crop((0, 0, 224, 224))
        img.save(filename)


def get_mapbox_url(coord: Tuple[float, float], scale: float, width: int = 224, height: int = 400):
    lon, lat = coord
    return (
        f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/{lon},{lat},{scale},0,0/{width}x{height}"
        "?access_token=pk.eyJ1IjoiYmFiaW9yIiwiYSI6ImNrbTRzbmw0ajA3cDAyb3BqajF3ZXppZHYifQ.-k9sjP0t4NqTy7R-6m8FvQ"
    )


def get_bing_url(coord: Tuple[float, float], scale: float, width: int = 224, height: int = 400):
    lon, lat = coord
    return (
        f"https://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial/{lat},{lon}/{scale}?mapSize={width},{height}&k"
        "ey=AinlihD-05xSPpRdaGyLlOkiA-oQ_oi5PnM6iMMbKuEIHyVIQlkZ97ZmuIf-myzH"
    )


def get_random_coord(
    used_coords: List[Tuple[float, float]], base_coord: Tuple[float, float], difference: float
) -> Tuple[float, float]:
    base_lon, base_lat = base_coord
    random_lat = base_lat - difference
    random_coord = (base_lon, random_lat)
    if random_coord in used_coords:
        return get_random_coord(used_coords, random_coord, difference)
    used_coords.append(random_coord)
    return (used_coords, random_coord)

img_count = 64
diff = 0.00015
start_lat = 56.145561897617235
start_lon = 21.82076853748342
coord = (start_lon, start_lat)
scale = 17
used_coords = []
downloaded_count = 0
a_number = 72
p_number = 73
negative_ids = list(range(3887, 1360*3, 3))
random.shuffle(negative_ids)

while downloaded_count < img_count:
    used_coords, coord = get_random_coord(used_coords, coord, diff)
    bing_url = get_bing_url(coord, scale, 1000, 1000)
    mapbox_url = get_mapbox_url(coord, scale - 1, 1000, 1000)
    try:    
        get_image(bing_url, f"test_a/img-{str(a_number).zfill(4)}.png", False)
        get_image(mapbox_url, f"test_p/img-{str(p_number).zfill(4)}.png", False)
        # get_image(mapbox_url, f"test_n_gamta_small_final/0/img-{str(negative_ids[downloaded_count]).zfill(4)}.png")
        a_number += 3
        p_number += 3
    except Exception as e:
        print("TIMEOUT...")
        print(e)
        continue
    downloaded_count += 1
    print(downloaded_count)
    coords_strs = [f"({lon}, {lat})" for lon, lat in used_coords]
    coords_file = open("coords.txt", "w")
    coords_file.write(json.dumps(coords_strs))
    coords_file.close()