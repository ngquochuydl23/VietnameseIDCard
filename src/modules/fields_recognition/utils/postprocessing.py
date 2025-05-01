front_class_names = [
    'id',
    'full_name',
    'date_of_birth',
    'sex',
    'nationality',
    'place_of_origin',
    'place_of_residence',
    'date_of_expiry',
    'qr_code'
]

back_class_names = [
    'fingerprint',
    'issue_date',
    'issue_place',
    'personal_identification'
]

def extract_field_images(detector, img):
    results = detector.predict(img)
    boxes = results[0].boxes.data
    boxes = sorted(boxes, key=lambda box: (box[5], box[1], box[0]))
    crops = []
    hit_poo = False

    for box in boxes:
        x1, y1, x2, y2, confidence, class_id = map(int, box[:6])

        crop = img[y1:y2, x1:x2]
        if class_id == 5 and hit_poo:
            crops.append({"class_name": "extend_place_of_residence", "field_img": crop})
        elif class_id == 5 and not hit_poo:
            hit_poo = (class_id == 5 and not hit_poo)
            crops.append({"class_name": "place_of_origin", "field_img": crop})
        else:
            crops.append({"class_name": front_class_names[class_id], "field_img": crop})
    return crops

def extract_back_field_images(detector, img):
    height, width = img.shape[:2]

    # Set pixels from center (height // 2) to bottom to white
    img[height // 2:] = 255  # white in BGR for all channels

    results = detector.predict(img)
    boxes = results[0].boxes.data
    boxes = sorted(boxes, key=lambda box: (box[5], box[1], box[0]))
    crops = []

    for box in boxes:
        x1, y1, x2, y2, confidence, class_id = map(int, box[:6])
        crop = img[y1:y2, x1:x2]
        crops.append({"class_name": back_class_names[class_id], "field_img": crop})
    return crops





