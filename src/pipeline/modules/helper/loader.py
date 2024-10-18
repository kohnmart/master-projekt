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


def load_images_from_folder_with_filter(folder, filter_by):
    all_images = []
    all_file_names = []

    for file_name in os.listdir(folder):
        if filter_by in file_name:
            read_image(file_name, all_file_names, all_images, folder)

    return all_images, all_file_names


def load_images_from_folder(folder, load_only_false_samples=False):
    all_images = []
    all_file_names = []

    
    for file_name in os.listdir(folder):
        if load_only_false_samples:
            filename_parts = file_name.split("_")
            ground_truth = filename_parts[1]
            prediction = filename_parts[2]

            if ground_truth != prediction:
                read_image(file_name, all_file_names, all_images, folder)

        else:
            read_image(file_name, all_file_names, all_images, folder)

    return all_images, all_file_names


def read_image(file_name, all_file_names, all_images, folder):
    # Add other extensions if needed
    if file_name.endswith(".png") or file_name.endswith(".jpg"):
        img = cv2.imread(os.path.join(folder, file_name))
        if img is not None:
            all_images.append(img)
            all_file_names.append(file_name)

