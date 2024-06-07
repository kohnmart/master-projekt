from transformers import YolosFeatureExtractor, YolosForObjectDetection, YolosImageProcessor
import torch
import numpy as np
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
        target_sizes = torch.tensor([[width, height]])  # Note the double square brackets

        results = self.image_processor.post_process_object_detection(outputs, threshold=0.5, target_sizes=target_sizes)[0]

        # Print detected objects and confidence scores
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.detach().numpy().tolist()]  # Detach tensor and convert to numpy array

        for box, score, label in zip(results['boxes'], results['scores'], results['labels']):
            box = box.detach().numpy()  # Detach tensor and convert to numpy array
            x_min, y_min, x_max, y_max = box
            box_width = x_max - x_min
            box_height = y_max - y_min

            m_x = (x_min + box_width) / 2
            print(x_min)
            # Object in Camera Center
            if x_min >= 90 and x_min <= 100:
                print(
                f"Detected Cloth Object with confidence "
                f"{round(score.item(), 3)} at location {box}"
                )

                return True
            else:
                return False
