import cv2
import numpy as np
import os 
from modules.clip import ClipFast
from modules.helper import load_images_from_folder, plot_images, calculate_averages
from modules.choices import make_choices
import pandas as pd
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score, precision_score, recall_score
import matplotlib.pyplot as plt
###################################

#   This script features the entire production pipeline from taking in the video sequence  
#   extracting objects and classification. Model and Input configurations can 
#   be set prior to start. Sample gets exported with its predicted label category as well as 
#   an individual csv file logging prediction scores to plain or decision-tree. 
#

###################################

###### CHOICES CONFIGURATION ######
path = './output'
choices = make_choices(path)


###### SETUP ######

print('Launching...')

clip_instance = ClipFast(model_name=choices['clip'])

folder_name = choices['file']
fullpath = os.path.join(path, folder_name)
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
plot_images(images, filenames, full_path)
print("Plot saved...")

###### Confusion Matrix ######
print(true_labels)
print(predicted_labels)
print("Creating conf matrix...")

classes =  ['dress', 'skirt', 'sweatshirt', 'shirt', 'short', 'pant', 'jacket', 'poloshirt', 't-shirt']

# Calculate the confusion matrix
cm = confusion_matrix(true_labels, predicted_labels, labels=classes)

# Calculate accuracy, precision, and recall
accuracy = accuracy_score(true_labels, predicted_labels)
# precision = precision_score(true_labels, predicted_labels, average='macro')
# recall = recall_score(true_labels, predicted_labels, average='macro')

# Display the confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classes)
fig, ax = plt.subplots(figsize=(10, 10))
disp.plot(cmap=plt.cm.Blues, xticks_rotation='vertical', ax=ax)

# Add accuracy, precision, and recall to the plot
ax.text(0.5, -0.2, f'Accuracy: {accuracy:.2f}', transform=ax.transAxes, fontsize=12, verticalalignment='top', horizontalalignment='center')

plt.title("Confusion Matrix for Multi-Class Classification")
plt.savefig(f"{full_path}/confusion_matrix.png")

print("Conf matrix saved...")