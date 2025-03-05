from ultralytics import YOLO
import os
import torch

class CornerDetector:
    def __init__(self, model = "yolov8n.pt"):
        self.model = YOLO(model)
        self.model.info()

    def device_info(self):
        print(f"Is GPU available?: {torch.cuda.is_available()}")
        print(f"GPU count: {torch.cuda.device_count()}")
        if torch.cuda.is_available():
            print(f"Device name: {torch.cuda.get_device_name(0)}")
            self.device = 'cuda'
        else:
            self.device = 'cuda'
        self.model.to(self.device)


    def train(self, data, epochs=50, imgsz=640):
        self.device_info()
        if not os.path.exists(data):
            raise FileNotFoundError(f"Không tìm thấy file {data}. Hãy kiểm tra đường dẫn!")
        self.model.train(data=data, epochs=epochs, imgsz=imgsz, device=self.device, amp=True)

    def save(self, out="best_model.pt"):
        self.model.save(out)

    def predict(self, img):
        return self.model(img)

    def get_model(self):
        return self.model
    
if __name__ == '__main__':
    detector = CornerDetector()

    #detector.train()
    detector.train(data="src/modules/fields/data.yaml")
    detector.save("new_version.pt")

