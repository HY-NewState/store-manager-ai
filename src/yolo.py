import pathlib
import torch

class YOLO:
    def __init__(self):
        self.person_model = self.load_person_model()
        self.yolo_model = self.load_yolo_model()

    def load_person_model(self):
        return torch.hub.load('ultralytics/yolov5', 'yolov5s')

    def load_yolo_model(self):
        temp = pathlib.WindowsPath
        pathlib.WindowsPath = pathlib.PosixPath
        model = torch.hub.load('yolov5', 'custom', path='model/best.pt', source='local')
        model.conf = 0.5
        pathlib.WindowsPath = temp
        return model

    def check_person(self, img):
        results = self.person_model(img)
        return 'person' in results.pandas().xyxy[0]['name'].values

    def check_things(self, img):
        results = self.yolo_model(img)
        return results.pandas().xyxy[0].to_json(orient="records")
