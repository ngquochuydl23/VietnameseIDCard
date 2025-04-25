import cv2
import numpy as np
import traceback

def order_points(c_pts):
    sorted_centre_points = sorted(c_pts, key=lambda x: x['class_id'])

    bottom_left = sorted_centre_points[0]
    bottom_right = sorted_centre_points[1]
    top_left = sorted_centre_points[2]
    top_right = sorted_centre_points[3]
    return [top_left, top_right, bottom_right, bottom_left]


def warp_image_with_centres(origin_img, centre_points, output_size=(800, 600)):
    try:
        width, height = output_size
        sorted_centre_points = order_points(centre_points)

        pts = np.array([[pt['x_center'], pt['y_center']] for pt in sorted_centre_points], dtype="float32")
        print(pts)

        dst_pts = np.array([
            [0, 0],
            [width - 1, 0],
            [width - 1, height - 1],
            [0, height - 1]
        ], dtype="float32")

        M = cv2.getPerspectiveTransform(pts, dst_pts)
        warped_img = cv2.warpPerspective(origin_img, M, (width, height))
        return warped_img
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return None