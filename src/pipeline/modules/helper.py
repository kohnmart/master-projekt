import os
import cv2
import matplotlib.pyplot as plt
from PIL import Image
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

def plot_images(images, filenames, foldername, cols=3):
    n_images = len(images)
    rows = (n_images // cols) + 1
    fig = plt.figure(figsize=(15, 5 * rows))
    
    for i, (img, filename) in enumerate(zip(images, filenames)):
        ax = fig.add_subplot(rows, cols, i + 1)
        ax.imshow(img)
        ax.set_title(filename, fontsize=10)
        ax.axis('off')  # Hide axes
    plt.tight_layout()
    save_file_name = foldername + '/all_plt.png'
    plt.savefig(save_file_name)


def calculate_averages(data):
    # Initialize a dictionary to hold the sums of each item
    sums = {}
    # Initialize a dictionary to hold the counts of each item
    counts = {}

    # Iterate through each dictionary in the list
    for entry in data:
        for key, value in entry.items():
            # Add value to the sum for this key
            if key in sums:
                sums[key] += value
                counts[key] += 1
            else:
                sums[key] = value
                counts[key] = 1

    # Calculate the averages
    averages = {key: sums[key] / counts[key] for key in sums}

            # Find the item with the highest average score
    max_item = max(averages, key=averages.get)
    max_average = averages[max_item]

    return averages, max_item