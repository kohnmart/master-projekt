import cv2
import numpy as np
import os 
import pandas as pd

from modules.yolos import YOLOSDetector
from modules.clip import ClipFast
from modules.helper.choices import make_choices

from modules.helper.loader import load_images_from_folder
from modules.helper.plotting import plot_images
from modules.helper.calc import calculate_averages


"""
EXTRACTOR AND CLASSIFIER Script

This script handles video sample extraction and classification. 
It processes a video to detect objects using YOLO, classifies detected objects using CLIP, 
and saves the classified frames. It then generates and saves a plot of the classified images.

Usage: 
1. Configure settings by following the prompts.
2. Run the script using `python video_seq_to_classifier.py`.
3. The results will be saved in the specified output directory.
"""

###### CHOICES CONFIGURATION ######
choices = make_choices(path='./stream_video')




###### SETUP ######
print('Launching...')

clip_instance = ClipFast(model_name=choices['clip'])
yolo_instance = YOLOSDetector()

file_name = choices['file']
video_path = os.path.join('./stream_video', file_name)

output_dir = os.path.join('output', choices['concat_name'])
os.makedirs(output_dir, exist_ok=True)




###### VIDEO CONFIGURATION ######
cap = cv2.VideoCapture(video_path)
cap.set(cv2.CAP_PROP_POS_FRAMES, int(choices['time_start']))

frame_rate = cap.get(cv2.CAP_PROP_FPS)
distance_per_frame = 1 / frame_rate  # Assuming 1 meter per second speed
capture_interval = 0.05  # Meters
frames_to_skip = int(capture_interval / distance_per_frame)

# Get the total number of frames in the video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

###### HELPER VARIABLES ######
current_detection_list = []
last_detection = [-10, -10]
frame_count = 0
last_keyed_frame = []




is_last_keyed_frame = False
###### CAPTURE RUN ######
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    print(f'Frame: {frame_count} / {total_frames}', end='\r', flush=True)

    frame = np.rot90(frame)
    # Object Detection
    is_detected, cropped_image = yolo_instance.process(frame)
    detection_score = {}
    # If an object is detected, run the CLIP classifier
    if is_detected:
        keyed_frame = cropped_image
        if choices['decision_tree']:
            detection_score, parent_averages = clip_instance.clip_decision_tree(keyed_frame, choices['rotation'])
        else:
            detection_score = clip_instance.clip_decision_plain(keyed_frame, choices['rotation'])

        # Check if the same object is detected within the range
        if frame_count - 3 <= last_detection[1]:
            current_detection_list.append(detection_score)
            last_keyed_frame = keyed_frame
            is_last_keyed_frame = True
        else:
            last_detection = [detection_score, frame_count]
            current_detection_list.append(detection_score)
            is_last_keyed_frame = False

    # If no object is detected, save the last detection
    elif is_detected == False and is_last_keyed_frame == True:
        avg_total, max_item = calculate_averages(current_detection_list)
        cv2.imwrite(os.path.join(output_dir, f"frame{frame_count}_{max_item}.jpg"), last_keyed_frame)
        last_keyed_frame = []
        is_last_keyed_frame = False
        current_detection_list = []

    frame_count += 1



###### RELEASE CAPTURE ######
cap.release()
print('Sequence completed...')



###### SAVE PLOT ######
print("Creating plot...")
images, filenames = load_images_from_folder(output_dir)
plot_images(images, filenames, output_dir)
print("Plot saved...")
