from transformers import YolosForObjectDetection, YolosImageProcessor
from ultralytics import YOLO
import torch
import numpy as np
from PIL import Image

class ObjectDetector:

    def __init__(self, model_type='yolos'):
        self.model_type = model_type
        if model_type == 'yolos':
            self.model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
            self.image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")
        elif model_type == 'yolo':
            self.model = YOLO('yolov8l.pt')
        else:
            raise ValueError("Invalid model type. Choose 'yolos' or 'yolo'.")

    def process(self, image):
        found_objects = []
        detected = False
        scores = []
        index = -1

        if self.model_type == 'yolos':
            inputs = self.image_processor(images=image, return_tensors="pt")
            outputs = self.model(**inputs)
            logits = outputs.logits
            bboxes = outputs.pred_boxes

            image_np = np.array(image)  # Convert the image to a NumPy array once
            height, width, _ = image_np.shape
            target_sizes = torch.tensor([[height, width]])  # Note the double square brackets

            results = self.image_processor.post_process_object_detection(outputs, threshold=0.2, target_sizes=target_sizes)[0]
            # Iterate over detected objects and process bounding boxes
            for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
                box = box.detach().numpy()  # Detach tensor and convert to numpy array
                x_min, y_min, x_max, y_max = map(int, box)
                # Ensure bounding box is within image dimensions
                x_min = max(0, x_min)
                y_min = max(0, y_min)
                x_max = min(width, x_max)
                y_max = min(height, y_max)

                cropped_image = image_np[y_min:y_max, x_min:x_max]
                x, y = cropped_image.shape[:2]
                if 50 <= x_min <= 300 and (x * y >= 60000):
                    detected = True
                    found_objects.append(cropped_image)
                    scores.append(score.item())

        elif self.model_type == 'yolo':
            results = self.model(image)
            image_np = np.array(image)
            height, width, _ = image_np.shape
            for box in results[0].boxes:  # Accessing the bounding boxes from results
                x1, y1, x2, y2 = map(int, box.xyxy.tolist()[0])
                x1 = max(0, x1)
                y1 = max(0, y1)
                x2 = min(width, x2)
                y2 = min(height, y2)

                cropped_image = image_np[y1:y2, x1:x2]
                x, y = cropped_image.shape[:2]
                if 0 <= x1 <= 300:
                    detected = True
                    found_objects.append(cropped_image)
                    scores.append(box.conf.item())  # Ensure score is properly defined here

        temp_score = 0
        for i, score in enumerate(scores):
            if score > temp_score:
                temp_score = score
                index = i

        if index != -1:
            found_objects = found_objects[index]

        return detected, found_objects

