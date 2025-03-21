import cv2
import numpy as np

def get_centre_point_box(box):
    x_min, y_min, x_max, y_max = box.xyxy[0].tolist()
    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2
    
    return x_center, y_center


def get_centre_point_boxex(boxes):
    centre_points = []
    for box in boxes:
        x, y = get_centre_point_box(box)
        centre_points.append((x, y))
        #print(f'Center: ({x}, {y})')
        
    return centre_points
        
def draw_centre_points(original_img, points):
    cv2_img = np.array(original_img)

    # Convert RGB to BGR (for OpenCV)
    cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_RGB2BGR)
    for point in points:
        cv2.circle(cv2_img, (int(point[0]), int(point[1])), radius=5, color=(255, 0, 0), thickness=-1)
    return cv2_img