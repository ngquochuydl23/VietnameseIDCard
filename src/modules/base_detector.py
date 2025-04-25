from abc import ABC, abstractmethod
from ultralytics import YOLO
import os
import torch
import numpy as np

class BaseDetector(ABC):
    def __init__(self, model="yolov8n.pt", verbose=False, fused=False):
        self.model = YOLO(model)
        self.model.info()
        self.device_info()
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
            self.device = 'cpu'
        self.model.to(self.device)

    @abstractmethod
    def train(self, data, epochs=50, imgsz=640):
        pass

    def predict(self, img):
        return self.model(img, verbose=False)

    def evaluate(self, data):
        metrics = self.model.val(data=data)
        return {
            "mean_mAP50": np.mean(metrics.box.map50),
            "mean_mAP50-95": np.mean(metrics.box.map),
            "mean_precision": np.mean(metrics.box.mp),
            "mean_recall": np.mean(metrics.box.mr)
        }

    def save(self, out="best_model.pt"):
            self.model.save(out)

    def get_model(self):
        return self.model
