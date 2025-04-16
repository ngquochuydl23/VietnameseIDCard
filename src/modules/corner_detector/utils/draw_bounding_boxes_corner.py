import cv2

def draw_bounding_box_corner(result, img, detector):
    drawed_img = img.copy()
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Lấy toạ độ (x1, y1, x2, y2)
        confidence = box.conf[0].item()  # Lấy độ chính xác
        class_id = int(box.cls[0])  # Lấy ID của class
        label = f"{detector.get_model().names[class_id]}: {confidence:.2f}"  # Tạo label

            # Vẽ bounding box lên ảnh
        cv2.rectangle(drawed_img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Màu xanh lá, độ dày 2px
        cv2.putText(drawed_img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return drawed_img
