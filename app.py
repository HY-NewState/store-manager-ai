import cv2 as cv
import numpy as np
import requests
from src.yolo import YOLO
import json

def main():
    yolo = YOLO()
    prevPerson = False
    curPerson = False
    isOpen = False
    didSendAlert = False

    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Camera open failed")
        return

    while True:
        ret, img = cap.read()

        if not ret:
            print("Can't read camera")
            break

        cv.imshow('PC_camera', img)

        curPerson = yolo.check_person(img)

        if (not prevPerson and curPerson):
            try:
                response = requests.get(url="http://192.168.0.14:3000/onoff", timeout=1)
                isOpen = response.json()
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.HTTPError, requests.exceptions.RequestException) as err:
                    print("Error:", err)
                    
        # 매장 운영 OFF
        if (not isOpen and curPerson and not didSendAlert):
            didSendAlert = True
            try:
                response = requests.post(url="http://192.168.0.14:3000/people", json={"alert": "alert"}, timeout=1)
                print("매장 침입 알람 전송 성공")
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.HTTPError, requests.exceptions.RequestException) as err:
                print("Error:", err)
        # 매장 운영 ON
        if (isOpen and prevPerson and not curPerson):
            didSendAlert = False
            img_np = np.array(img)
            frame = cv.cvtColor(img_np, cv.COLOR_BGR2RGB)

            result = yolo.check_things(frame)
            resultObj = json.loads(result)
            serverJson = []

            if not result:
                print("No objects detected")
            else:
                for item in resultObj:
                    serverJson.append(item['name'])

                print(serverJson)

                try:
                    response = requests.post(url="http://192.168.0.14:3000/test", json=serverJson, timeout=1)
                    print(response)
                except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.HTTPError, requests.exceptions.RequestException) as err:
                    print("Error:", err)
            
        prevPerson = curPerson

        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
