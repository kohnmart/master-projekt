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


def load_images_from_folder(folder):
    images = []
    filenames = []
    for filename in os.listdir(folder):
        if filename.endswith(".png") or filename.endswith(".jpg"):  # Add other extensions if needed
            img = cv2.imread(os.path.join(folder, filename))
            if img is not None:
                images.append(img)
                filenames.append(filename)
    return images, filenames

