from detector import FieldDetector

if __name__ == '__main__':
    #detector = FieldDetector('cccdYoloV8.pt')yolov8x
    detector = FieldDetector(model='cccdYoloV8.pt')
    detector.train(data="data.yaml", epochs=100, patience=20, freeze=20)
    detector.save("field_model_v3.pt")