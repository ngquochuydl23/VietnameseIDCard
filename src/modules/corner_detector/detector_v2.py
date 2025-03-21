from ultralytics import YOLO
import os
import torch
import shutil
import numpy as np
import logging

class CornerDetector:
    def __init__(self, model="yolov8n.pt", verbose=False, fused = False):
        self.device = None
        self.model = YOLO(model, verbose=verbose)

        if fused:
            logging.info("Enabled fuse")
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

    def train(self, data, epochs=100, imgsz=640, batch = 16):
        self.device_info()
        if not os.path.exists(data):
            raise FileNotFoundError(f"{data} Not found!")

        # remove old historical training process
        if os.path.exists('./runs'):
            shutil.rmtree('./runs')
        self.model.train(data=data, epochs=epochs, imgsz=imgsz, device=self.device, amp=True, batch=batch)

    def save(self, out="best_model.pt"):
        self.model.save(out)

    def predict(self, img, save=False):
        return self.model(img, save=save, verbose=False)

    def evaluate(self, data):
        metrics = self.model.val(data=data)
        return {
            "mean_mAP50": np.mean(metrics.box.map50),
            "mean_mAP50-95": np.mean(metrics.box.map),
            "mean_precision": np.mean(metrics.box.mp),
            "mean_recall": np.mean(metrics.box.mr)
        }

    def get_model(self):
        return self.model