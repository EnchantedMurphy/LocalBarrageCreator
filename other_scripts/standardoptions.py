import pandas as pd
import json


def get_options():
    with open('options.json', 'r+') as options:
        data = json.load(options)
    textSpeedIndex = int(data['textSpeedIndex'])
    textSizeIndex = int(data['textSizeIndex'])
    PlayResX = int(data['PlayResX'])
    PlayResY = int(data['PlayResY'])
    return textSpeedIndex, textSizeIndex, PlayResX, PlayResY


def set_options(textSpeedIndex, textSizeIndex, PlayResX, PlayResY):
    data = {'textSpeedIndex': textSpeedIndex,
            "textSizeIndex": textSizeIndex,
            "PlayResX": PlayResX,
            "PlayResY": PlayResY}
    with open('options.json', 'w+') as options:
        json.dump(data, options)
