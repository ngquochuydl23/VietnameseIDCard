import torch
from ultralytics.utils.ops import non_max_suppression

def apply_non_max_suppression(results):
    boxes_tensor = results[0].boxes.xyxy  # (N, 4)
    scores_tensor = results[0].boxes.conf  # (N,)
    class_ids = results[0].boxes.cls  # (N,)

    detections = torch.cat([
        boxes_tensor,
        scores_tensor.unsqueeze(1),
        class_ids.unsqueeze(1)
    ], dim=1)

    nms_result = non_max_suppression(
        detections.unsqueeze(0),
        conf_thres=0.25,
        iou_thres=0.45
    )[0]

    return nms_result