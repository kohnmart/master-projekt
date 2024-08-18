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