import json
from datetime import datetime

import cv2 as cv
import requests
import numpy as np

from src.yolo import checkPerson, checkThings

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("camera open failed")
    exit()
while True:
    ret, img = cap.read()
    if not ret:
        print("Can't read camera")
        break

    cv.imshow('PC_camera', img)
    if checkPerson(img):
        # cv.imwrite('imgs/{}.png'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), img)

        # RGB타입으로 변환
        img_np = np.array(img)
        frame = cv.cvtColor(img_np, cv.COLOR_RGB2BGR)
        
        result = checkThings(frame)
        resultObj = json.loads(result)
        serverJson = []
        if (not result):
            print("No objects detected")
        else:
            for item in resultObj:
                serverJson.append(item['name'])
            
            print(json.dumps(serverJson))
            requests.post("http://localhost:3000/test", json=serverJson)
                
        
    cv.waitKey(1)

cap.release()
cv.destroyAllWindows()