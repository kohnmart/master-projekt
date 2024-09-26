from abc import ABC, abstractmethod
import numpy as np


class ObjectDetector(ABC):
    """
    Abstract base class for object detection.
    """

    def __init__(self, model_type):
        self.model_type = model_type

    @abstractmethod
    def process(self, image):
        pass

    def _get_best_detection(self, found_objects, scores):
        """Returns the best detection based on the highest score."""
        if not scores:
            return False, []

        best_index = int(np.argmax(scores))
        return True, found_objects[best_index] if found_objects else []


    def _get_largest_cropped_image(self, found_objects):
        """Returns the detection with the largest cropped image area."""
        if not found_objects or len(found_objects) == 0:
            return False, []

        # Calculate the area for each cropped image (height * width)
        areas = [img.shape[0] * img.shape[1] for img in found_objects]  # shape[0] is height, shape[1] is width
        largest_index = int(np.argmax(areas))

        return True, found_objects[largest_index]
