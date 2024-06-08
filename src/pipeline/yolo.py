from transformers import YolosFeatureExtractor, YolosForObjectDetection, YolosImageProcessor
import torch
import numpy as np
import cv2

class YOLOS:

    def __init__(self, stream_width):
        self.model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
        self.image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")
        self.stream_width = stream_width


    def process(self, image):
        inputs = self.image_processor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)

        logits = outputs.logits
        bboxes = outputs.pred_boxes

        height, width, _ = image.shape
        target_sizes = torch.tensor([[height, width]])  # Note the double square brackets

        results = self.image_processor.post_process_object_detection(outputs, threshold=0.5, target_sizes=target_sizes)[0]

        detections = []

        img_array = np.array(image)  # Convert the image to a NumPy array once

        for box, score, label in zip(results['boxes'], results['scores'], results['labels']):
            box = box.detach().numpy()  # Detach tensor and convert to numpy array
            x_min, y_min, x_max, y_max = box
            box_width = x_max - x_min
            box_height = y_max - y_min

            # Calculate the midpoint of the box
            m_x = (x_min + x_max) / 2
            # Object in Camera Center
            if 90 <= x_min <= 100:
                print(
                    f"Detected Cloth Object with confidence "
                    f"{round(score.item(), 3)} at location {box}"
                )

                # Ensure the coordinates are within the image dimensions
                x_min, y_min, x_max, y_max = map(int, [x_min, y_min, x_max, y_max])
                detected_cropped_image = img_array[y_min:y_max, x_min:x_max]
                detections.append((score.item(), detected_cropped_image))

        if detections:
            # Find the detection with the highest score using np.argmax
            scores = [d[0] for d in detections]  # Extract scores
            max_index = np.argmax(scores)  # Find index of max score
            detected_cropped_image = detections[max_index][1]  # Get the image corresponding to max score
            detected = True
            print(f"Highest score index: {max_index}")
        else:
            detected = False
            detected_cropped_image = image

        return detected, detected_cropped_image
