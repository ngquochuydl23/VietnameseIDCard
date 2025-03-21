import cv2
import numpy as np


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")

    # Tổng của x + y --> top-left có tổng nhỏ nhất, bottom-right có tổng lớn nhất
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # top-left
    rect[2] = pts[np.argmax(s)]  # bottom-right

    # Hiệu x - y --> top-right có hiệu nhỏ nhất, bottom-left có hiệu lớn nhất
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # top-right
    rect[3] = pts[np.argmax(diff)]  # bottom-left

    return rect

def warp_image_with_centres(origin_img, centre_points, output_size=(800, 600)):
    try:
        width, height = output_size
        pts = np.array(centre_points, dtype="float32")

        ordered_pts = order_points(pts)
        dst_pts = np.array([
            [0, 0],
            [width - 1, 0],
            [width - 1, height - 1],
            [0, height - 1]
        ], dtype="float32")

        # Tính ma trận biến đổi và warp
        M = cv2.getPerspectiveTransform(ordered_pts, dst_pts)
        return cv2.warpPerspective(origin_img, M, (width, height))
    except:
        return None