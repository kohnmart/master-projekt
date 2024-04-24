# system
import sys
import os
import torch
import cv2
import numpy as np
import supervision as sv
from PIL import Image
from matplotlib import patches
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../../')))
print(os.path.abspath(os.path.join(os.getcwd(), '../../')))
from config.path import get_checkpoint_path, get_training_data_path, PATH_TYPE
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor

class SAM:

    def __init__(self):
        CHECKPOINT_PATH = "./model_weights/sam_vit_h_4b8939.pth"
        DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        MODEL_TYPE = "vit_h"

        sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT_PATH).to(device=DEVICE)
        self.mask_generator = SamAutomaticMaskGenerator(
            model=sam,
            points_per_side=10,
            pred_iou_thresh=0.96,
            stability_score_thresh=0.96,
            crop_n_layers=1,
            crop_n_points_downscale_factor=2,
            min_mask_region_area=100,  # Requires open-cv to run post-processing
        )


    def image_processor(self, file_name):
        
        
        img_path = get_training_data_path(PATH_TYPE.segmentator, file_name)
        image_bgr = cv2.imread(img_path)


        blurred_image = cv2.GaussianBlur(image_bgr, (11, 11), 0)
        
        
        #blurred_image = remove_shadow_rgb(blurred_image)


        return self.mask_generator.generate(blurred_image), image_bgr

        # mask_annotator = sv.MaskAnnotator(color_lookup=sv.ColorLookup.INDEX, opacity=1.0)

        # detections = sv.Detections.from_sam(sam_result=masks)

        # annotated_image = mask_annotator.annotate(scene=blurred_image.copy(), detections=detections)

        # # sv.plot_images_grid(
        # #     images=[blurred_image, annotated_image],
        # #     grid_size=(1, 2),
        # #     titles=['source image', 'segmented image']
        # # )

        # bounding_box_annotator = sv.BoundingBoxAnnotator(color_lookup=sv.ColorLookup.INDEX)
        # annotated_image = bounding_box_annotator.annotate(
        #     scene=blurred_image, detections=detections)
        # cv2.cvtColor.imshow(annotated_image)



    def clean_masks(self,masks):
        masks_cleaned = []
        for mask in masks: 
            if np.mean(mask['segmentation'][3]) <= 0.2 and (mask['area'] >= 10000 and mask['area'] <= 50000):
                masks_cleaned.append(mask)

        return masks_cleaned
        

    def separate_by_bbox(self,masks_cleaned, image):

        separated_images = []

        for i, ann in enumerate(masks_cleaned):
        # Extract bounding box coordinates
            x, y, width, height = map(int, ann['bbox'])  # Ensure integer values
            
            # Define rectangular region
            rect = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor='r', facecolor='none')
            
            #mask = np.array(ann['segmentation'], dtype=np.uint8)
            #masked_image = cv2.bitwise_and(image_rgb, image_rgb, mask=mask)
                
            # Crop the region from the original image
            cropped_image = image[y:y+height, x:x+width]
            cropped_image_bgr = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR)
            separated_images.append(cropped_image_bgr)
        
        return separated_images
    

    def show_sample_with_bboxes(self, masks, image, name, probs):

        for i, mask in enumerate(masks):
            x, y, w, h = mask['bbox']
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255,0), 3)
            cv2.putText(image, probs[i], (x,y-5), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,255,0), 1)
        to_save_image = Image.fromarray(image)

        path = './output/' + name

        to_save_image.save(path)