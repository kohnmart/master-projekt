from transformers import YolosFeatureExtractor, YolosForObjectDetection, YolosImageProcessor
import torch
import numpy as np
import cv2
class YOLOS:

    def __init__(self):
        self.model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
        self.image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")

    def process(self, image):

        detected = False
        cropped_image = []

        found_objects = []
        scores = []
        index = -1
        inputs = self.image_processor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)

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
            if 100 <= x_min <= 130:
                if (x * y >= 60000):
                    print(f"Detected object with size {x * y} and score: {score.item()}")
                    # Display the cropped image
                    detected = True
                    found_objects.append(cropped_image)
                    scores.append(score.item())
                else: 
                    detected = False
                    cropped_image = []
        
        temp_score = 0
        for i, score in enumerate(scores):
            if score > temp_score:
                temp_score = score
                index = i

        if index != -1:
            found_objects = found_objects[index]
        


        return detected, found_objects
