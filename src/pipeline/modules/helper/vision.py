from PIL import Image
import cv2
import numpy as np

def rotate_image(image, angle):
    # Get the dimensions of the image
    (height, width) = image.shape[:2]

    # Calculate the center of the image
    center = (height // 2, width // 2)
    # Get the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D((250, 250), -90, 1.0)

    # Perform the rotation
    rotated_image = cv2.warpAffine(image, rotation_matrix, (height, width))
    
    return rotated_image


def rotation_image_proper(keyed_frame, angle):
    # Get the dimensions of the image
    height, width = keyed_frame.shape[:2]

    # Calculate the center of the image
    center = (width / 2, height / 2)

    # Calculate the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)

    # Calculate the new bounding box dimensions
    abs_cos = abs(rotation_matrix[0, 0])
    abs_sin = abs(rotation_matrix[0, 1])
    new_width = int(height * abs_sin + width * abs_cos)
    new_height = int(height * abs_cos + width * abs_sin)

    # Adjust the rotation matrix to take into account the new dimensions
    rotation_matrix[0, 2] += new_width / 2 - center[0]
    rotation_matrix[1, 2] += new_height / 2 - center[1]

    # Apply the rotation to the image with the new dimensions
    rot_frame = cv2.warpAffine(keyed_frame, rotation_matrix, (new_width, new_height))

    # Convert the image from BGR (OpenCV default) to RGB (Matplotlib expects RGB)
    rot_frame_rgb = cv2.cvtColor(rot_frame, cv2.COLOR_BGR2RGB)
    return rot_frame_rgb



def mask_area(image):
    (height, width) = image.shape[:2]
    return height * width


def keying(orig_image):
# Calculate the average color
    n_image = orig_image.copy()
    n_image = cv2.medianBlur(n_image, 31)

    # n_cropped = n_image[0:5, 10:15]
    # average_color = n_cropped.mean(axis=0).mean(axis=0)
    # print(average_color)

    average_color = np.array([104.12, 171.12, 13.32])

    # Define a threshold range around the average color
    threshold = 60  # Adjust this value as needed
    lower_bound = np.clip(average_color - threshold, 0, 255)
    upper_bound = np.clip(average_color + threshold, 0, 255)

    mask = cv2.inRange(n_image, lower_bound, upper_bound)

    # Invert the mask to create a binary mask
    binary_mask = cv2.bitwise_not(mask)


    result_image = cv2.bitwise_and(orig_image, orig_image, mask=binary_mask)

    return result_image
