from transformers import YolosFeatureExtractor, YolosForObjectDetection, YolosImageProcessor
import torch
import numpy as np
import cv2
# Assuming you have these functions available
# from your_module import get_training_data_path, remove_shadow_rgb

# Load the pre-trained model and feature extractor



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

        # Print detected objects and confidence scores
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.detach().numpy().tolist()]  # Detach tensor and convert to numpy array

        detected = False
        detected_cropped_image = None

        img_array = np.array(image)  # Convert the image to a NumPy array once

        detections = []

        for box, score, label in zip(results['boxes'], results['scores'], results['labels']):
            box = box.detach().numpy()  # Detach tensor and convert to numpy array
            x_min, y_min, x_max, y_max = box
            box_width = x_max - x_min
            box_height = y_max - y_min

            # Convert image to numpy array

            m_x = (x_min + box_width) / 2
            # Object in Camera Center
            if x_min >= 90 and x_min <= 100:
                print(
                f"Detected Cloth Object with confidence "
                f"{round(score.item(), 3)} at location {box}"
                )

                # Ensure the coordinates are within the image dimensions
                img_array = np.array(image)
                x_min, y_min, x_max, y_max = map(int, [x_min, y_min, x_max, y_max])
                detected_cropped_image = img_array[y_min:y_max, x_min:x_max]
                detected = True
                detections.append([score.item(), detected_cropped_image])

        if len(detections) != 0:
                # Find the detection with the highest score using np.argmax
                scores = [d[0] for d in detections]  # Extract scores
                max_index = np.argmax(scores)  # Find index of max score
                detected_cropped_image = detections[max_index][1]  # Get the image corresponding to max score
                print("Index")
                print(max_index)
    
        else:
            detected = False
            detected_cropped_image = image

        return detected, detected_cropped_image
