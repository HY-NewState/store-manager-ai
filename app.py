import cv2 as cv
from datetime import datetime
from src.yolo import checkPerson, checkThings
import json

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
        result = checkThings(img)
        resultObj = json.loads(result)
        serverJson = []
        if (not result):
            print("No objects detected")
        else:
            for item in resultObj:
                serverJson.append(item['name'])
            
            print(json.dumps(serverJson))
                
        
    cv.waitKey(1)

cap.release()
cv.destroyAllWindows()