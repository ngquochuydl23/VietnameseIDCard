import cv2
import numpy as np

def get_centre_point_boxes(nms_result, classes):
    best_boxes = {}
    centre_points = []
    for box in nms_result:
        x_min, y_min, x_max, y_max, conf, class_id = box.tolist()
        class_name = classes[int(class_id)]
        # print(f"Class: {class_id} {class_name}, Bounding Box: ({x_min}, {y_min}, {x_max}, {y_max}), Confidence: {conf:.2f}")

        if class_id not in best_boxes or best_boxes[class_id]['confidence'] < conf:
            best_boxes[class_id] = {
                'bbox': (x_min, y_min, x_max, y_max),
                'confidence': conf,
                'label': f"{class_name}: {conf:.2f}"
            }
            x_center = (x_min + x_max) / 2
            y_center = (y_min + y_max) / 2
            centre_points.append((x_center, y_center))
    return centre_points
        
def draw_centre_points(original_img, points):
    cv2_img = np.array(original_img)

    # Convert RGB to BGR (for OpenCV)
    cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_RGB2BGR)
    for point in points:
        cv2.circle(cv2_img, (int(point[0]), int(point[1])), radius=5, color=(255, 0, 0), thickness=2)
    return cv2_img