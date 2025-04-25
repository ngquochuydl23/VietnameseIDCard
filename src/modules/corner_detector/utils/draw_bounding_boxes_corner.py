import cv2

def draw_bounding_box_corner(result, img, detector):
    drawed_img = img.copy()
    best_boxes = {}
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = box.conf[0].item()
        class_id = int(box.cls[0])
        class_name = detector.get_model().names[class_id]
        label = f"{class_name}: {confidence:.2f}"

        if class_id not in best_boxes or best_boxes[class_id]['confidence'] < confidence:
            best_boxes[class_id] = {
                'bbox': (x1, y1, x2, y2),
                'confidence': confidence,
                'label': f"{class_name}: {confidence:.2f}"
            }

            cv2.rectangle(drawed_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(drawed_img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return drawed_img
