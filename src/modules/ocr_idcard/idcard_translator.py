import cv2
import pytesseract
import numpy as np
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from PIL import Image
import torch

class IdCardTranslator():
    def __init__(self,
                lang='vie',
                tesseract_config=r'--oem 3 --psm 6',
                vietocr_config='vgg_transformer',
                engine='vietocr'):

        self.lang = lang
        self.tesseract_config = tesseract_config
        self.vietocr_config = vietocr_config
        self.engine = engine
        self.vietocr_detector = None
        self.setup_engine()

    def setup_engine(self):
        if self.engine == 'vietocr':
            self.vietocr_config = Cfg.load_config_from_name(self.vietocr_config)
            self.vietocr_config['cnn']['pretrained'] = False
            self.vietocr_config['device'] = 'cuda' if torch.cuda.is_available() else 'cpu'
            self.vietocr_detector = Predictor(self.vietocr_config)
        else:
            pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

    def read_field(self, img):
        if self.engine == 'vietocr':
            return self.vietocr_detector.predict(Image.fromarray(img))
        return pytesseract.image_to_string(img, lang=self.lang, config=self.tesseract_config)

    def processing_img(
            self,
            img,
            brighten_factor=1.5,
            scale_factor=2.0,
            blur_kernel_size=(3, 3),
            alpha=0.6,
            beta=0.4):

        if isinstance(img, str):
            img = cv2.imread(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = self.resize_image(img, scale_factor=scale_factor)

        # brightening
        img = np.clip(img * brighten_factor, 0, 255).astype(np.uint8)
        sharpen_kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ])
        sharpened = cv2.filter2D(img, -1, sharpen_kernel)
        blured = cv2.GaussianBlur(img, blur_kernel_size, 0)

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(img)

        _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Morphology reduce outliers
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

        return cleaned

    def read_info(self, crops):
        result = {}
        for idx, crop in enumerate(crops):
            class_name = crop["class_name"]
            if  class_name != "qr_code":
                
                preprocessed_img = self.processing_img(crop["field_img"])
                field_text = self.read_field(preprocessed_img)
                result[class_name] = field_text
                
        # if result.get("place_of_residence") and result.get("extend_place_of_residence"):
        #     result["place_of_residence"] += f' {result["extend_place_of_residence"]}'
        #     result.pop("extend_place_of_residence")
        print(result)
        if ("place_of_residence" in result) and ("extend_place_of_residence" in result):
            result["place_of_residence"] += f' {result["extend_place_of_residence"]}'
            result.pop("extend_place_of_residence")
        return result

    def resize_image(self, image, scale_factor=2.0):
        # Resize the image by scaling
        height, width = image.shape
        new_dim = (int(width * scale_factor), int(height * scale_factor))
        resized_image = cv2.resize(image, new_dim, interpolation=cv2.INTER_CUBIC)
        return resized_image
