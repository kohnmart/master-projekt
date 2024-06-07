# system
import sys
import os
import torch
import cv2
import numpy as np
import supervision as sv
from PIL import Image
from matplotlib import patches
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor

# custom
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../../')))
from config.path import get_training_data_path, DATASET_PATH_TYPE

class SAM:

    def __init__(self):
        CHECKPOINT_PATH = "./model_weights/sam_vit_h_4b8939.pth"
        DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        MODEL_TYPE = "vit_h"

        sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT_PATH).to(device=DEVICE)
        self.mask_generator = SamAutomaticMaskGenerator(
        model=sam,
        points_per_side=5,
        pred_iou_thresh=0.9,
        stability_score_thresh=0.9,
        crop_n_layers=1,
        crop_n_points_downscale_factor=2,
        min_mask_region_area=100,  # Requires open-cv to run post-processing
        )

    def remove_shadow_rgb(self, image):
        # Convert image to RGB if it isn't already
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) if image.shape[-1] == 3 else image
        # Convert to YCrCb color space
        ycrcb = cv2.cvtColor(rgb, cv2.COLOR_RGB2YCrCb)
        # Split into channels
        y, cr, cb = cv2.split(ycrcb)
        # Apply histogram equalization on the brightness channel
        y_eq = cv2.equalizeHist(y)
        # Merge back the channels
        ycrcb_eq = cv2.merge((y_eq, cr, cb))
        # Convert back to RGB
        result = cv2.cvtColor(ycrcb_eq, cv2.COLOR_YCrCb2RGB)
        return result

    def image_processor(self, img_path=None, frame=None):
        #img_path = get_training_data_path(DATASET_PATH_TYPE.generator, file_name)
        image_bgr = None

        if img_path:
            image_bgr = cv2.imread(img_path)

        else: 
            image_bgr = frame

        image_ycrcb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)
        blurred_image = cv2.medianBlur(image_ycrcb, 25)
        #processed_image = self.remove_shadow_rgb(blurred_image) 

        return self.mask_generator.generate(blurred_image)


    def clean_masks(self,masks, range):
        masks_cleaned = []
        for mask in masks: 
            if mask['area'] >= range[0] and mask['area'] <= range[1]:
                masks_cleaned.append(mask)
        return masks_cleaned
        

    def separate_by_bbox(self,masks_cleaned, image, with_segmentation=False, save_single_objects=False):

        separated_images = []
        masks_cleaned_compared = []
        for i, ann in enumerate(masks_cleaned):
        # Extract bounding box coordinates
            x, y, width, height = map(int, ann['bbox'])  # Ensure integer values
                    
            if with_segmentation:
                mask = np.array(ann['segmentation'], dtype=np.uint8)
                si_image = image.copy()
                si_image = cv2.bitwise_and(si_image, si_image, mask=mask)
                
            # Crop the region from the original image
            cropped_image = si_image[y:y+height, x:x+width]
            cropped_image_bgr = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR)

            mean = np.mean(cropped_image[0])
            print(mean)
            if mean < 230:

                separated_images.append(cropped_image_bgr)
                masks_cleaned_compared.append((masks_cleaned[i]))
                to_save_image = Image.fromarray(cropped_image_bgr)

                if save_single_objects:
                    path = f'./output/v4'
                    if not os.path.exists(path):
                        os.makedirs(path)

                    path = path + '/' + 'test' + str(i) + '.png'

                    to_save_image.save(path)
        
        return separated_images, masks_cleaned_compared
    

    def save_sample_with_bboxes(self, masks, image, name, probs):

        for i, mask in enumerate(masks):
            x, y, w, h = mask['bbox']
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255,0), 3)
            cv2.rectangle(image, (x, y), (x + 150, y + -20), (255, 255, 255), -1) 
            cv2.putText(image, probs[i], (x,y-5), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,255,0), 1)
        to_save_image = Image.fromarray(image)

        path = f'./output/v4'
        if not os.path.exists(path):
            os.makedirs(path)

        path = path + '/' + name

        to_save_image.save(path)