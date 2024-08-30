import os 
import cv2
import numpy as np
import pandas as pd

from modules.clip import ClipFast
from modules.cloth_categories import ClothingCategories

from modules.helper.choices import make_choices

from modules.helper.loader import load_images_from_folder
from modules.helper.plotting import plot_images, generate_and_plot_conf
from modules.helper.calc import calculate_averages


"""
This script performs image classification and analysis using the ClipFast model and a predefined set of choices by user.

The script loads images from a specified folder, processes them through the ClipFast model using either a decision tree 
or plain classification method, saves the classification results, and generates a plot of the images with their predicted 
labels. Additionally, it generates and saves a confusion matrix to evaluate the model's performance.

Modules and Functions:
- `ClipFast`: A custom module for processing images with the CLIP model.
- `get_all_classes`: Retrieves all possible class labels for the classification task.
- `make_choices`: Generates configuration choices such as model selection, file paths, and processing options.
- `load_images_from_folder`: Loads images and their filenames from a specified folder.
- `plot_images`: Generates and saves a plot of the images with their predicted labels.
- `calculate_averages`: Used to compute average scores during the decision tree process.

Process:
1. **CHOICES CONFIGURATION**: Loads configuration choices from a specified path.
2. **SETUP**: Initializes the CLIP model based on the selected choices and prepares the folder structure for outputs.
3. **CAPTURE RUN**: 
   - Iterates over the images, classifies each image, and saves the result as an image and CSV file.
   - If a decision tree method is used, additional average calculations are performed and saved.
4. **SAVE OUT PLOT**: Generates and saves a plot of all processed images with their predicted labels.
5. **CONFUSION MATRIX**: Computes and saves a confusion matrix to evaluate the classification performance against true labels.

Outputs:
- Processed images with their predicted labels saved in the specified "./output/x" folder.
- CSV files containing detection scores and if applicable, parent tree averages to trace back on errors.
- A plot of processed images with labels.
- A confusion matrix plot to evaluate classification accuracy.

Usage:
Run this script in a Python environment after configuring the required paths and choices. Ensure that the input images are 
located in the specified folder and that the necessary modules are available.

"""



###### CHOICES CONFIGURATION ######
path = './stream_extracted'
choices = make_choices(path)


###### SETUP ######

print('Launching...')

clip_instance = ClipFast(model_name=choices['clip'])

folder_name = choices['file']
fullpath = os.path.join(path, folder_name)
print(fullpath)
images, filenames = load_images_from_folder(fullpath)

full_path = os.path.join('output', choices['concat_name'])
if not os.path.exists(full_path):
    os.mkdir(full_path)


# Example true labels and predicted labels
true_labels = []
predicted_labels = []


###### CAPTURE RUN ######

for i, keyed_frame in enumerate(images):

    filename = filenames[i].split('.')[0]
    label = filename.split('_')[1]
    true_labels.append(label)
    detection_score = {}

    keyed_frame = np.rot90(keyed_frame, k=-1)

    if choices['decision_tree'] == True:
        detection_score, parent_averages = clip_instance.clip_decision_tree(keyed_frame, choices['rotation'])

    else:
        detection_score = clip_instance.clip_decision_plain(keyed_frame, choices['rotation'])

    
    max_item = max(detection_score, key=detection_score.get) 
    predicted_labels.append(max_item)
    cv2.imwrite(f"{full_path}/{filename}_{max_item}_.jpg", keyed_frame)

    if choices['decision_tree'] == True:
        # Convert original data to DataFrame
        df_data = pd.DataFrame([parent_averages], index=['parent-tree-avg'])

        # Convert averages to DataFrame
        df_averages = pd.DataFrame([detection_score], index=['sub-tree-avg'])

        # Concatenate the two DataFrames
        df_combined = pd.concat([df_data, df_averages])

    else:
        # Convert averages to DataFrame
        df_combined = pd.DataFrame([detection_score], index=['plain-avg'])

    # Save the combined DataFrame to CSV
    csv_file = f"{full_path}/{filename}_{max_item}__.csv"
    df_combined.to_csv(csv_file)


###### SAVE OUT PLOT ######

print("Creating plot...")
export_path = full_path
images, filenames = load_images_from_folder(export_path)

plot_images(images, filenames, full_path)
print("Plot saved...")

###### Confusion Matrix ######
print("Creating conf matrix...")

classes = ClothingCategories.get_all_classes()

generate_and_plot_conf(true_labels, predicted_labels, classes, full_path)

print("Conf matrix saved...")

print("Finished...")