import os
import cv2
from detector import FieldDetector
from src.modules.corner_detector.detector_v2 import CornerDetector
from src.modules.corner_detector.utils.centre_point_box import get_centre_point_boxex
from src.modules.corner_detector.utils.preprocessing import warp_image_with_centres
from multiprocessing import Process, Lock
from tqdm import tqdm
import threading
import logging

TYPES = ['train', 'test', 'valid']
ROOT_DATASET_DIR = 'dataset'
NEW_DATASET_DIR = './dataset_v2.1'


def generate(path, type, detector, corner_detector, position, lock):
    ds_path = os.path.join(path, type)

    img_dir = os.path.join(ds_path, 'images')
    total_items = len(os.listdir(img_dir))


    new_labels = os.path.join(NEW_DATASET_DIR, type, 'labels')
    new_imgs = os.path.join(NEW_DATASET_DIR, type, 'images')

    tqdm.set_lock(lock)
    for idx, img_path in tqdm(enumerate(os.listdir(img_dir)),
                              total=len(img_dir),
                              desc=f"Processing '{type}' dataset",
                              position=position,
                              leave=True,
                              dynamic_ncols=True):
        item_path = os.path.join(img_dir, img_path)
        img = cv2.imread(item_path)

        corner_result = corner_detector.predict(item_path)
        centre_points = get_centre_point_boxex(corner_result[0].boxes)
        wrapped_img = warp_image_with_centres(img, centre_points, output_size=(800, 600))

        if wrapped_img is None:
            continue

        results = detector.predict(wrapped_img)

        label_file_name = os.path.join(new_labels, f'{idx}.txt')
        img_file_name = os.path.join(new_imgs, f'{idx}.png')

        with open(label_file_name, 'w') as label_file:
            for result in results:
                for box in result.boxes:
                    confidence = box.conf[0].item()

                    if confidence > 0.75:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        class_id = int(box.cls[0])

                        img_h, img_w = wrapped_img.shape[:2]
                        center_x = ((x1 + x2) / 2) / img_w
                        center_y = ((y1 + y2) / 2) / img_h
                        width = (x2 - x1) / img_w
                        height = (y2 - y1) / img_h

                        # Write to the label file
                        cv2.imwrite(img_file_name, wrapped_img)
                        label_file.write(f"{class_id} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}\n")
        logging.info(f"Generate '{type}' dataset completed.")


if __name__ == '__main__':
    detector = FieldDetector('cccdYoloV8.pt', fused=True)
    corner_detector = CornerDetector('../corner_detector/models/corner_detector_v2.1.pt', fused=True)

    # detector.device_info()
    processes  = []
    lock = Lock()

    for idx, type_name in enumerate(TYPES):
        p = Process(
            target=generate,
            args=(ROOT_DATASET_DIR,type_name, detector, corner_detector, idx, lock)
        )
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    logging.info("All types processed.")
