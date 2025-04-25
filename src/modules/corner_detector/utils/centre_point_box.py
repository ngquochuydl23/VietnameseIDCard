import cv2
import numpy as np

def get_centre_point_boxes(nms_result, classes):
    best_boxes = {}
    centre_points = []
    for box in nms_result:
        x_min, y_min, x_max, y_max, conf, class_id = box.tolist()
        class_name = classes[int(class_id)]
        if class_id not in best_boxes or best_boxes[class_id]['confidence'] < conf:
            x_center = (x_min + x_max) / 2
            y_center = (y_min + y_max) / 2
            best_boxes[class_id] = {
                'confidence': conf
            }
            centre_points.append({
                'x_center': x_center,
                'y_center': y_center,
                'confidence': conf,
                'class_id': class_id,
                'label': f"{class_name}: {conf:.2f}"
            })
    return interpolate_centre_points(centre_points, classes)


def interpolate_centre_points(centre_points, classes):

    # Helper mappings
    corner_names = {0: "bottom-left", 1: "bottom-right", 2: "top-left", 3: "top-right"}
    opposite_map = {0: 3, 1: 2, 2: 1, 3: 0}
    adjacent_map = {0: [1, 2], 1: [0, 3], 2: [3, 0], 3: [2, 1]}

    # Map class_id => point
    id_to_point = {int(p['class_id']): p for p in centre_points}
    known_ids = set(id_to_point.keys())
    all_ids = set(range(len(classes)))
    missing_ids = all_ids - known_ids

    if not missing_ids:
        return centre_points  # Không thiếu gì

    # Tính trọng tâm các điểm đã biết
    known_points = list(id_to_point.values())
    avg_x = np.mean([p['x_center'] for p in known_points])
    avg_y = np.mean([p['y_center'] for p in known_points])

    for missing_id in missing_ids:
        interpolated = None

        # Nếu có đủ 3 điểm để suy luận chính xác
        opp_id = opposite_map[missing_id]
        adj_ids = adjacent_map[missing_id]

        if opp_id in id_to_point and all(a in id_to_point for a in adj_ids):
            opp = id_to_point[opp_id]
            adj1 = id_to_point[adj_ids[0]]
            adj2 = id_to_point[adj_ids[1]]

            x_interp = (adj1['x_center'] + adj2['x_center']) - opp['x_center']
            y_interp = (adj1['y_center'] + adj2['y_center']) - opp['y_center']

            interpolated = {
                'x_center': x_interp,
                'y_center': y_interp,
                'confidence': 0.0,
                'class_id': float(missing_id),
                'label': f"{corner_names[missing_id]} (interpolated)"
            }
        else:
            # Fallback: đối xứng qua trọng tâm
            base = sorted(known_points, key=lambda p: abs(p['class_id'] - missing_id))[0]
            x_interp = 2 * avg_x - base['x_center']
            y_interp = 2 * avg_y - base['y_center']

            interpolated = {
                'x_center': x_interp,
                'y_center': y_interp,
                'confidence': 0.0,
                'class_id': float(missing_id),
                'label': f"{corner_names[missing_id]} (fallback)"
            }

        centre_points.append(interpolated)

    return centre_points

def draw_centre_points(original_img, points):
    cv2_img = np.array(original_img)

    # Convert RGB to BGR (for OpenCV)
    cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_RGB2BGR)
    for point in points:
        cv2.circle(cv2_img, (int(point[0]), int(point[1])), radius=5, color=(255, 0, 0), thickness=2)
    return cv2_img