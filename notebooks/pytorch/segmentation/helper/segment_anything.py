import os
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt

def load_images(relative_path, limit=20):
    file_names = get_all_files_from_folder(relative_path)[:limit]
    return file_names

def process_image(file_path):
    orig_image = Image.open(file_path)
    n_image = np.array(orig_image)
    gray_image = cv2.cvtColor(n_image, cv2.COLOR_BGR2GRAY)
    image_ycrcb = cv2.cvtColor(n_image, cv2.COLOR_BGR2YUV)
    image_ycrcb[:, :, 0] = cv2.equalizeHist(image_ycrcb[:, :, 0])
    blurred_image = cv2.medianBlur(image_ycrcb, 21)
    return n_image, blurred_image

def generate_masks(blurred_image, threshold_area=1000):
    masks = mask_generator.generate(blurred_image)
    cleaned_masks = [mask for mask in masks if mask['area'] > threshold_area]
    return cleaned_masks

def annotate_images(n_image, blurred_image, cleaned_masks):
    mask_annotator = sv.MaskAnnotator(color_lookup=sv.ColorLookup.INDEX, opacity=1.0)
    detections = sv.Detections.from_sam(sam_result=cleaned_masks)
    annotated_image = mask_annotator.annotate(scene=blurred_image.copy(), detections=detections)
    
    bounding_box_annotator = sv.BoundingBoxAnnotator(color_lookup=sv.ColorLookup.INDEX)
    final_annotated_image = bounding_box_annotator.annotate(scene=n_image, detections=detections)
    
    return final_annotated_image

def clean_masks(masks, area_range=(25000, 100000), mean_threshold=0.2):
    masks_cleaned = [mask for mask in masks if np.mean(mask['segmentation'][3]) <= mean_threshold and (area_range[0] <= mask['area'] <= area_range[1])]
    return masks_cleaned

def crop_and_save_mask(cleaned_masks, n_image, file_name):
    x, y, w, h = cleaned_masks[0]['bbox']
    cropped_mask = cleaned_masks[0]['segmentation'][y:y+h, x:x+w]
    cropped_mask = cropped_mask.astype(np.uint8) * 255
    masked_image = cv2.resize(cropped_mask, (256, 256), interpolation=cv2.INTER_NEAREST)
    path = './' + file_name + '_mask.jpg'
    cv2.imwrite(path, masked_image)

def plot_images(images, titles, grid_size):
    fig, axes = plt.subplots(grid_size[0], grid_size[1], figsize=(12, 6))
    for ax, image, title in zip(axes.flatten(), images, titles):
        ax.imshow(image)
        ax.set_title(title)
        ax.axis('off')
    plt.tight_layout()
    plt.show()