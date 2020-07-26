import requests
from urllib.parse import urlencode
import json
import numpy as np

from PIL import Image
import matplotlib.pyplot as plt

imgsize = 64

def prediction(DEFAULT_BASE_URL, imgs, url = None):
    url = (url or (DEFAULT_BASE_URL % "predict"))
    payload = urlencode({"json_args" : json.dumps(list(imgs))})

    headers = {'content-type': 'application/x-www-form-urlencoded'}
    # /predict  gives predictions in list format
    response = requests.request("POST", url, data=payload, headers=headers)
    try:
        return json.loads(response.text)
    except BaseException as e:
        raise RuntimeError("Error: caught %r while processing %r (%r)" % (e, response, response.text))


def load_images(img_path):
    imgs = []
    imgs.append(np.array(Image.open(img_path)))
    return np.array(imgs)


def transform(imgs):
    imgs = imgs / 255.0
    # reshape of the pixel array
    imgs = imgs.reshape(len(imgs), imgs.shape[1] * imgs.shape[2] * imgs.shape[3])
    return imgs


def get_predictions(DEFAULT_BASE_URL, img_path):
    imgs = load_images(img_path)
    imgs1 = transform(imgs)
    predictions = prediction(DEFAULT_BASE_URL, imgs1.tolist())

    return predictions

