import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../../')))
sys_path = sys.path[-1]

import cv2
import numpy as np
import pandas as pd

from src.pipeline.modules.clip import ClipFast
from src.pipeline.modules.cloth_categories import ClothingCategories

from src.pipeline.modules.helper.choices import make_choices

from src.pipeline.modules.helper.loader import load_images_from_folder
from src.pipeline.modules.helper.plotting import plot_images, generate_and_plot_conf
from src.pipeline.modules.helper.calc import calculate_averages


###### CHOICES CONFIGURATION ######
dataset_production_dir = "dataset/production/setup-v2"
data_path = os.path.join(sys_path, dataset_production_dir)
choices = make_choices(data_path, True)


###### SETUP ######

print('Launching...')

clip_instance = ClipFast(model_name=choices['clip'])

folder_name = choices['file']
fullpath = os.path.join(data_path, folder_name)
print(fullpath)
images, filenames = load_images_from_folder(fullpath)


export_path = os.path.join(sys_path, "src/pipeline/output")
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
    final_score = {}
    pred_item = []

    if choices['decision_tree'] == True:
        child_data, parent_score = clip_instance.clip_decision_tree(keyed_frame, choices['rotation'])
        pred_item = child_data['final_item']
        final_score = child_data['score_tree']

    else:
        final_score = clip_instance.clip_decision_plain(keyed_frame, choices['rotation'])



    predicted_labels.append(pred_item)
    cv2.imwrite(f"{full_path}/{filename}_{pred_item}_.jpg", keyed_frame)

    if choices['decision_tree'] == True:
        # Convert original data to DataFrame
        df_parent = pd.DataFrame([parent_score], index=['parent-tree-avg'])

        df_stages = []
        for score_stage in final_score:
            # Convert averages to DataFrame
            df = pd.DataFrame([score_stage], index=['stage-tree-avg'])
            df_stages.append(df)

        df_combined = [df_parent] + df_stages
        
        # Concatenate the two DataFrames
        df_total = pd.concat(df_combined)

    else:
        # Convert averages to DataFrame
        df_total = pd.DataFrame([final_score], index=['plain-avg'])

    # Save the combined DataFrame to CSV
    csv_file = f"{full_path}/{filename}_{pred_item}_.csv"
    df_total.to_csv(csv_file)


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