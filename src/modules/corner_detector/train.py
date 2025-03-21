from detector_v2 import CornerDetector
import logging

if __name__ == '__main__':
    detector = CornerDetector('yolov8s.pt')
    logging.info('Start to train')
    detector.train(data="./dataset_v2/data.yaml")
    detector.evaluate('./dataset_v2/data.yaml')
