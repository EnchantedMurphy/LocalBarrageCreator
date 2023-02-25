import pandas as pd
import json


def get_options():
    with open('options.json', 'r+') as options:
        data = json.load(options)
    textSpeedIndex = int(data['textSpeedIndex'])
    textSizeIndex = int(data['textSizeIndex'])
    PlayResX = int(data['PlayResX'])
    PlayResY = int(data['PlayResY'])
    host = data['host']
    return textSpeedIndex, textSizeIndex, PlayResX, PlayResY, host


def set_options(textSpeedIndex, textSizeIndex, PlayResX, PlayResY, host):
    data = {'textSpeedIndex': textSpeedIndex,
            "textSizeIndex": textSizeIndex,
            "PlayResX": PlayResX,
            "PlayResY": PlayResY,
            "host": host}
    with open('options.json', 'w+') as options:
        json.dump(data, options)
