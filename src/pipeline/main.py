# system
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../../..')))

from config.path import get_training_data_path, get_checkpoint_path, PATH_TYPE
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import torch
from transformers import CLIPProcessor, CLIPModel
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor

import cv2
import supervision as sv
from matplotlib import patches


def sam_setup():
    CHECKPOINT_PATH = get_checkpoint_path("sam_vit_h_4b8939.pth")
    DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    MODEL_TYPE = "vit_h"

    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


    sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT_PATH).to(device=DEVICE)
    mask_generator = SamAutomaticMaskGenerator(
        model=sam,
        points_per_side=10,
        pred_iou_thresh=0.96,
        stability_score_thresh=0.96,
        crop_n_layers=1,
        crop_n_points_downscale_factor=2,
        min_mask_region_area=100,  # Requires open-cv to run post-processing
    )


def image_processing(mask_generator, file_name):
    img_path = get_training_data_path(PATH_TYPE.segmentator, file_name)
    image_bgr = cv2.imread(img_path)

    blurred_image = cv2.GaussianBlur(image_bgr, (11, 11), 0)

    masks = mask_generator.generate(blurred_image)

    mask_annotator = sv.MaskAnnotator(color_lookup=sv.ColorLookup.INDEX, opacity=1.0)

    detections = sv.Detections.from_sam(sam_result=masks)

    annotated_image = mask_annotator.annotate(scene=blurred_image.copy(), detections=detections)

    masks_cleaned = []
    for mask in masks: 
        if np.mean(mask['segmentation'][3]) <= 0.2 and (mask['area'] >= 10000 and mask['area'] <= 50000):
            masks_cleaned.append(mask)


    for i, ann in enumerate(masks_cleaned):
        # Extract bounding box coordinates
        x, y, width, height = map(int, ann['bbox'])  # Ensure integer values
        
        # Define rectangular region
        rect = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor='r', facecolor='none')
        
        #mask = np.array(ann['segmentation'], dtype=np.uint8)
        #masked_image = cv2.bitwise_and(image_rgb, image_rgb, mask=mask)
            
        # Crop the region from the original image
        cropped_image = image_bgr[y:y+height, x:x+width]
        cropped_image_bgr = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR)


def predictor(text_prompt, image):
    inputs = processor(text=text_prompt, images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image # this is the image-text similarity score
    return logits_per_image.softmax(dim=1) # we can take the softmax to get the label probabilities
   


def classifier(image):
    probs = predictor(['a photo a upper body cloth', 'a photo of a lower body cloth'])

    if probs[0][0] < probs[0][1]:
        probs = predictor(['a photo of a short pants', 'a photo of a long pants'])
        res = f"Short: {probs[0][0]:.2f}% ___ Pant: {probs[0][1]:.2f}%"

    else: 
        print("Detected: Upper Body Cloth Type")
        probs = predictor(['a photo of a short sleeve top', 'a photo of a long-sleeve top'])
        res = f"Short Sleeve: {probs[0][0]:.2f}% ___ Long Sleeve: {probs[0][1]:.2f}%"

        if probs[0][0] > probs[0][1]:
            probs = predictor(['a photo of a t-shirt', 'a photo of a polo shirt'])
            res = f"T-Shirt: {probs[0][0]:.2f}% ___ Polo Shirt: {probs[0][1]:.2f}%"

        else:
            probs = predictor(['a photo of a sweatshirt', 'a photo of a jacket'])
            res = f"Shirt: {probs[0][0]:.2f}% ___ Jacket: {probs[0][1]:.2f}%"


