import cv2 as cv
from datetime import datetime

def Cam():
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
        if cv.waitKey(1) == ord('c'):
            cv.imwrite('imgs/{}.png'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), img)
        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()