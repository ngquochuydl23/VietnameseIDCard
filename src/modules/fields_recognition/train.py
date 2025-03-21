from detector import FieldDetector

if __name__ == '__main__':
    #detector = FieldDetector('cccdYoloV8.pt')yolov8x
    detector = FieldDetector('yolov8n.pt')
    detector.device_info()
    detector.train(data="data.yaml", epochs=100)
    detector.save("field_model_v2.1.pt")