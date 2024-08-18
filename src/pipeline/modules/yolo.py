from ultralytics import YOLO
from PIL import Image
from abstracts.object_detection import ObjectDetector
import torch


class YOLODetector(ObjectDetector):
    """
    YOLO Detector class.
    - Model options: 'v5small', 'v8nano', 'v8medium', 'v8large'
    - Weights path: src/pipeline/model_weights/yolo
    - Source: https://github.com/ultralytics/ultralytics
    """

    def __init__(self):
        super().__init__(model_type='yolo')
        self.model = YOLO('yolov8l.pt')

    def process(self, image):
        image_np = np.array(image)
        height, width, _ = image_np.shape

        results = self.model(image)
        found_objects, scores = self._extract_detections(results, image_np, width, height)
        return self._get_best_detection(found_objects, scores)

    def _extract_detections(self, results, image_np, width, height):
        """Extracts and processes detections from YOLO results."""
        found_objects, scores = []

        for box in results[0].boxes:
            x1, y1, x2, y2 = self._get_bounding_box_coordinates(box.xyxy.tolist()[0], width, height)
            cropped_image = image_np[y1:y2, x1:x2]

            if self._is_valid_detection(x1):
                found_objects.append(cropped_image)
                scores.append(box.conf.item())

        return found_objects, scores

    def _get_bounding_box_coordinates(self, box, width, height):
        """Calculates bounding box coordinates within image boundaries."""
        x_min, y_min, x_max, y_max = map(int, box)
        x_min, y_min = max(0, x_min), max(0, y_min)
        x_max, y_max = min(width, x_max), min(height, y_max)
        return x_min, y_min, x_max, y_max

    def _is_valid_detection(self, x1):
        """Checks if a YOLO detection is valid based on given criteria."""
        return 0 <= x1 <= 300

