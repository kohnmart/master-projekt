import numpy as np
import cv2

def keying(orig_image):
# Calculate the average color
    n_image = orig_image.copy()
    n_image = cv2.medianBlur(n_image, 31)

    n_cropped = n_image[0:5, 10:15]
    average_color = n_cropped.mean(axis=0).mean(axis=0)

    # Define a threshold range around the average color
    threshold = 60  # Adjust this value as needed
    lower_bound = np.clip(average_color - threshold, 0, 255)
    upper_bound = np.clip(average_color + threshold, 0, 255)

    # Apply the threshold to create a mask
    # Apply the threshold to create a mask
    mask = cv2.inRange(n_image, lower_bound, upper_bound)

    # Invert the mask to create a binary mask
    binary_mask = cv2.bitwise_not(mask)


    result_image = cv2.bitwise_and(orig_image, orig_image, mask=binary_mask)


    return result_image
