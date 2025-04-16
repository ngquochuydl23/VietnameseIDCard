import yaml
import numpy as np
from PIL import Image

from modules.corner_detector.corner_detector import CornerDetector
from modules.fields_recognition.detector import FieldDetector
from modules.ocr_idcard import IdCardTranslator


class IdCardService:
    def __init__(self):
        #using yaml to load

        self.corner_detector = CornerDetector()
        self.field_detector = FieldDetector()
        pass

    async def idcard_extract_info(self, id_card, is_front = True):
        bytes = await id_card.read()
        image = np.array(Image.open(io.BytesIO(bytes)).convert("RGB"))

        #preprocessing
        self.corner_detector.predict(image, verbose=True)


        
