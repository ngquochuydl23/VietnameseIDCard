import os
import cv2
from src.modules.fields.detector import  CornerDetector

if __name__ == '__main__':
    detector = CornerDetector()
    detector.device_info()

    X_path = '../../../cccd'
    dataset_out = '../../../dataset-v2'

    # for file_path in os.listdir(X_path):
    #     img = cv2.imread(os.path.join(X_path, file_path))
    #     detector.predict(img)

    print(detector.predict(cv2.imread('../../../cccd/img910.jpg')))