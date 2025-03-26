def extract_fields(boxes, img):
    NUM_CLASSES = 9  # total number of classes
    fields_per_class = [[] for _ in range(NUM_CLASSES)]  # initialize list of lists
    box_list = []

    for idx_box, box in enumerate(boxes):
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # convert box coordinates to int
        confidence = box.conf[0].item()         # confidence score
        class_id = int(box.cls[0])              # class label

        cropped_object = img[y1:y2, x1:x2]

        if cropped_object.size == 0:
            print(f"Warning: Empty crop at box {idx_box} in result")
            continue

        box_list.append({
            'class_id': class_id,
            'confidence': confidence,
            'box': (x1, y1, x2, y2),
            'cropped': cropped_object
        })

    # Sort by y1 (top to bottom), then x1 (left to right)
    box_list.sort(key=lambda b: (b['box'][1], b['box'][0]))

    # Collect all crops for each class_id (accept duplicates)
    for item in box_list:
        class_id = item['class_id']
        fields_per_class[class_id].append(item['cropped'])

    # Find which classes were found (non-empty lists)
    found_classes = [i for i, crops in enumerate(fields_per_class) if crops]

    return fields_per_class, found_classes
