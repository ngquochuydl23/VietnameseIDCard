from ultralytics import YOLO
import os
import torch
import numpy as np


class FieldDetector:
    def __init__(self, model="yolov8n.pt", verbose=False, fused=False):
        self.model = YOLO(model)
        self.model.info()

        if fused:
            print("Enabled fuse")
            self.model.fuse()

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
        self.model.train(
            data=data,
            epochs=epochs,
            imgsz=imgsz,
            device=self.device,
            amp=True,
            augment=True,
            hsv_h=0.015,
            hsv_s=0.7,
            hsv_v=0.4,
            degrees=10.0,
            translate=0.1,
            scale=0.5,
            shear=2.0,
            flipud=0.5,
            fliplr=0.5,
            mosaic=1.0,
            mixup=0.2)

    def save(self, out="best_model.pt"):
            self.model.save(out)

    def predict(self, img):
            return self.model(img, verbose=False)

    def get_model(self):
            return self.model

    def evaluate(self, data):
            metrics = self.model.val(data=data)
            return {
                "mean_mAP50": np.mean(metrics.box.map50),
                "mean_mAP50-95": np.mean(metrics.box.map),
                "mean_precision": np.mean(metrics.box.mp),
                "mean_recall": np.mean(metrics.box.mr)
            }
