import os

from src.modules.base_detector import BaseDetector


class BackFieldDetector(BaseDetector):
    def train(self, data, epochs=50, imgsz=640):
        if not os.path.exists(data):
            raise FileNotFoundError(
                f"Không tìm thấy file {data}. Hãy kiểm tra đường dẫn!"
            )
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
            mixup=0.2,
        )
