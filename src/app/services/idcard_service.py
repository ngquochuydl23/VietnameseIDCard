import yaml
import asyncio
import logging
from src.app.constants.http_msg_constants import NO_CORNER_DETECTED
from src.modules.corner_detector.corner_detector import CornerDetector
from src.modules.fields_recognition.back_detector import BackFieldDetector
from src.modules.fields_recognition.detector import FieldDetector
from src.modules.ocr_idcard.idcard_translator import IdCardTranslator
from src.modules.corner_detector.utils.centre_point_box import get_centre_point_boxes
from src.modules.corner_detector.utils.preprocessing import warp_image_with_centres
from src.modules.fields_recognition.utils.postprocessing import extract_field_images, extract_back_field_images
from src.app.utils.bytes_to_nparray import convert_file_to_nparray
from src.app.exceptions.app_exception import AppException


from src.modules.shared.utils.nms import apply_non_max_suppression

logger = logging.getLogger(__name__)

class IdCardService:
    def __init__(self, config_file='src/app/configs.yaml'):
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        self.ocr_config = config['ocr_config']
        self.front_field_config = config['front_field_config']
        self.corner_config = config['corner_config']
        self.back_field_config = config['back_field_config']

        self.corner_detector = CornerDetector(self.corner_config['model'])
        self.front_field_detector = FieldDetector(self.front_field_config['model'])
        self.back_field_detector = BackFieldDetector(self.back_field_config['model'])
        self.idcard_translator = IdCardTranslator(vietocr_config=self.ocr_config['pretrained_cnn_model'])

    async def idcard_extract_combine(self, front_card, back_card):
        front_info, back_info = await asyncio.gather(
            self.idcard_extract_front(front_card),
            self.idcard_extract_back(back_card)
        )
        return {"front": front_info, "back": back_info}

    async def idcard_extract_front(self, front_card):
        front_img = await convert_file_to_nparray(front_card)
        corner_result = self.corner_detector.predict(front_img)
        classes = self.corner_detector.get_classes()

        nms_result = apply_non_max_suppression(corner_result)
        if nms_result is None or len(nms_result) == 0:
            raise AppException(NO_CORNER_DETECTED)

        centre_points = get_centre_point_boxes(nms_result, classes)
        preprocess_img = warp_image_with_centres(front_img, centre_points, output_size=(800, 600))
        crops = extract_field_images(self.front_field_detector, preprocess_img)
        if not crops:
            #raise AppException(NO_FRONT_FIELDS_DETECTED)
            return None
        return self.idcard_translator.read_front_info(crops)

    async def idcard_extract_back(self, back_card):
        back_img = await convert_file_to_nparray(back_card)
        corner_result = self.corner_detector.predict(back_img)
        classes = self.corner_detector.get_classes()

        nms_result = apply_non_max_suppression(corner_result)
        if nms_result is None or len(nms_result) == 0:
            raise AppException(NO_CORNER_DETECTED)

        centre_points = get_centre_point_boxes(nms_result, classes)
        preprocess_img = warp_image_with_centres(back_img, centre_points, output_size=(800, 600))

        crops = extract_back_field_images(self.back_field_detector, preprocess_img)
        if not crops:
            #raise AppException(NO_BACK_FIELDS_DETECTED)
            return None
        return self.idcard_translator.read_back_info(crops)
