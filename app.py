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
    h, w, c = img.shape
    crop_img = img[0:h,w//3:w*2//3]
    if not ret:
        print("Can't read camera")
        break

    cv.imshow('PC_camera', crop_img)
    if checkPerson(crop_img):
        # cv.imwrite('imgs/{}.png'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), img)

        # RGB타입으로 변환
        img_np = np.array(crop_img)
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
            try:
                response = requests.post(url="http://192.168.0.14:3000/test", json=serverJson, timeout=1)
                print(response)
            except requests.exceptions.Timeout as errd:
                print("Timeout Error : ", errd)
                
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting : ", errc)
                
            except requests.exceptions.HTTPError as errb:
                print("Http Error : ", errb)

            # Any Error except upper exception
            except requests.exceptions.RequestException as erra:
                print("AnyException : ", erra)
    cv.waitKey(1)

cap.release()
cv.destroyAllWindows()