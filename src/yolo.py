import pathlib

import cv2
import numpy as np
import torch

prevPerson = False
personModel = torch.hub.load('ultralytics/yolov5', 'yolov5s')
temp = pathlib.WindowsPath
pathlib.WindowsPath = pathlib.PosixPath
yoloModel = torch.hub.load('yolov5', 'custom', path='model/best.pt', source='local')

def checkPerson(img):
    global prevPerson
    results = personModel(img)

    if ('person' in results.pandas().xyxy[0]['name'].values):
        prevPerson = True
    elif (prevPerson):
        prevPerson = False
        return True
    
    return False

def checkThings(img):
    results = yoloModel(img)
    return results.pandas().xyxy[0].to_json(orient="records")