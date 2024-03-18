import torch

prevPerson = False
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

def checkPerson(img):
    global prevPerson
    results = model(img)
    print(results.pandas().xyxy[0])
    if ('person' in results.pandas().xyxy[0]['name'].values):
        prevPerson = True
    elif (prevPerson):
        prevPerson = False
        return True
    
    return False