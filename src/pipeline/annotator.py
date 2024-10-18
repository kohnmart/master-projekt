import time
from sam import SAM
from helper import get_all_samples
from mongo import MONGO
from clip import ClipClassifier
import numpy as np


"""
Automated Clothing Sample Processing Pipeline.

This script launches and sets up instances of SAM (Segment Anything Model), ClipClassifier, and MONGO
to process clothing samples for object detection and classification. The script performs the following tasks:
- Loads all sample file names.
- For each sample, generates segmentation masks using SAM, cleans the masks, and extracts individual clothing objects.
- Uses the ClipClassifier to classify each detected clothing object and predict labels with probabilities.
- Inserts the detected object information and labels into a MongoDB database.
- Optionally saves the image with bounding boxes around the detected objects.

Key Workflow:
1. SAM is used to process and segment the input images.
2. Masks are cleaned and bounding boxes are extracted to isolate individual objects.
3. ClipClassifier is applied to classify the cropped objects.
4. The results (labels and masks) are stored in the MongoDB database.

The script tracks and outputs the elapsed time at the end of execution for performance monitoring.
"""

print('Launching...')

sam_instance = SAM()
clip_instance = ClipClassifier()
mongo_instance = MONGO()

print ('Connected succesfully to database...')

print('Instances are setup...')

start_time = time.time()
file_names = get_all_samples()

for sample in file_names:

    print(f"Processing: {sample}")

    masks, image = sam_instance.image_processor(sample[1])
    cleaned_masks = sam_instance.clean_masks(masks, range=[10000, 200000])

    cloth_objects, cleaned_compared_masks = sam_instance.separate_by_bbox(cleaned_masks, image, True, True)
    
    probs_strings = []
    labels = []
    for cloth in cloth_objects:
        clip_instance.image = cloth

        res = clip_instance.classifier()
        labels.append(res[0])
        probs_strings.append(f'{res[0]}: {res[1]}')

    for i, mask in enumerate(cleaned_compared_masks):
        mongo_instance.mongo_insert(sample[0], labels[i], mask)

    # sam_instance.save_sample_with_bboxes(cleaned_compared_masks, image, sample, probs)


end_time = time.time()

elapsed_time = end_time - start_time
formatted_elapsed_time = "{:.2f}".format(elapsed_time)

print("Elapsed time:", formatted_elapsed_time, "seconds")