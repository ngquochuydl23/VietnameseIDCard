import yaml
import asyncio
import logging
from src.modules.corner_detector.corner_detector import CornerDetector
from src.modules.fields_recognition.detector import FieldDetector
from src.modules.ocr_idcard.idcard_translator import IdCardTranslator
from src.modules.corner_detector.utils.centre_point_box import get_centre_point_boxex
from src.modules.corner_detector.utils.preprocessing import warp_image_with_centres
from src.modules.fields_recognition.utils.postprocessing import extract_field_images
from src.app.utils.bytes_to_nparray import convert_file_to_nparray
from src.app.exceptions.app_exception import AppException

logger = logging.getLogger(__name__)

class IdCardService:
    def __init__(self):
        with open('src/app/configs.yaml', 'r') as file:
            config = yaml.safe_load(file)
        self.ocr_config = config['ocr_config']
        self.field_config = config['field_config']
        self.corner_config = config['corner_config']

        self.corner_detector = CornerDetector(self.corner_config['model'])
        self.field_detector = FieldDetector(self.field_config['model'])
        self.idcard_translator = IdCardTranslator(vietocr_config=self.ocr_config['pretrained_cnn_model'])

    async def idcard_extract_combine(self, front_card, back_card):
        front_img = await convert_file_to_nparray(front_card)
        back_img = await convert_file_to_nparray(back_card)

        front_info, back_info = await asyncio.gather(
            self.idcard_extract_front(front_img),
            self.idcard_extract_back(back_img)
        )
        # preprocessing
        # self.corner_detector.predict(image, verbose=True)

        return {"front": front_info, "back": back_info}

    async def idcard_extract_front(self, front_card):
        front_img = await convert_file_to_nparray(front_card)
        corner_result = self.corner_detector.predict(front_img)

        centre_points = get_centre_point_boxex(corner_result[0].boxes)

        preprocess_img = warp_image_with_centres(front_img, centre_points, output_size=(800, 600))
        crops = extract_field_images(self.field_detector, preprocess_img)

        if not crops:
            raise AppException('Cannot detect any fields in idcard.')
        return self.idcard_translator.read_info(crops)

    async def idcard_extract_back(self, back_card):
        back_img = await convert_file_to_nparray(back_card)
        # corner_result = self.corner_detector.predict(front_img)
        # centre_points = get_centre_point_boxex(corner_result[0].boxes)

        # preprocess_img = warp_image_with_centres(front_img, centre_points, output_size=(800, 600))
        # crops = extract_field_images(self.field_detector, preprocess_img)

        # return self.idcard_translator.read_info(crops)
        return {
            "issue_date": '15/09/2021',
            "issue_place": "CỤC TRƯỞNG CỤC CẢNH SÁT QUẢN LÝ VỀ HÀNH CHÍNH TRẬT TỰ XÃ HỘI",
            "personal_identification": "Nối ruồi C: 1cm dưới miêng trái"
        }
