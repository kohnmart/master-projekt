import os
import cv2

def get_all_samples(cloth_type):
    
    file_names = []

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

    relative_path = f'dataset/classifier/train/{cloth_type}'

    folder_path = os.path.join(project_root, relative_path)

    # Walk through all files and directories recursively
    for root, dirs, files in os.walk(folder_path):
        # Iterate over files in the current directory
        for filename in files:
            fullpath = os.path.join(folder_path, filename)
            file_names.append([filename, fullpath])
    
    return file_names


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



def mask_area(image):
    (height, width) = image.shape[:2]
    return height * width

