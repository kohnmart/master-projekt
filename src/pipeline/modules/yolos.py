from transformers import YolosForObjectDetection, YolosImageProcessor
from PIL import Image
import numpy as np
from modules.abstracts.object_detection import ObjectDetector
import torch

class YOLOSDetector(ObjectDetector):
    """
    YOLOS Detector class.
    - Model: 'tiny'
    - Source: https://huggingface.co/hustvl/yolos-tiny
    """

    def __init__(self):
        super().__init__(model_type='yolos')
        self.model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
        self.image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")

    def process(self, image):
        image_np = np.array(image)
        height, width, _ = image_np.shape

        inputs = self.image_processor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)

        target_sizes = torch.tensor([[height, width]])
        results = self.image_processor.post_process_object_detection(outputs, threshold=0.2, target_sizes=target_sizes)[0]

        found_objects, scores = self._extract_detections(results, image_np, width, height)
        return self._get_best_detection(found_objects, scores)

    def _extract_detections(self, results, image_np, width, height):
        """Extracts and processes detections from YOLOS results."""
        found_objects = []
        scores = []

        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            x_min, y_min, x_max, y_max = self._get_bounding_box_coordinates(box, width, height)
            cropped_image = image_np[y_min:y_max, x_min:x_max]

            if self._is_valid_detection(x_min, cropped_image):
                found_objects.append(cropped_image)
                scores.append(score.item())

        return found_objects, scores

    def _get_bounding_box_coordinates(self, box, width, height):
        """Calculates bounding box coordinates within image boundaries."""
        x_min, y_min, x_max, y_max = map(int, box.detach().numpy())
        x_min, y_min = max(0, x_min), max(0, y_min)
        x_max, y_max = min(width, x_max), min(height, y_max)
        return x_min, y_min, x_max, y_max

    def _is_valid_detection(self, x_min, cropped_image):
        """Checks if a YOLOS detection is valid based on given criteria."""
        return 50 <= x_min <= 300 and cropped_image.size >= 60000