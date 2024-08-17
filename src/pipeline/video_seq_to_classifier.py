import cv2
import numpy as np
import os 
from modules.yolo import ObjectDetector
from modules.clip import ClipFast
from modules.helper import load_images_from_folder, plot_images, calculate_averages
from modules.choices import make_choices
import pandas as pd


#   EXTRACTOR AND PRE-CLASSIFIER Script
#   This script features video sample extraction as well as pre-classification

#   Image saving: filename _ predicted  _ class
#   run - python video_seq_to_classifier.py 
#   follow choices


###### CHOICES CONFIGURATION ######

choices = make_choices(path='./stream_video')


###### SETUP ######

print('Launching...')

clip_instance = ClipFast(model_name=choices['clip'])
yolo_instance = ObjectDetector(model_type='yolos')


file_name = choices['file']
video_path = './stream_video/' + file_name

full_path = os.path.join('output', choices['concat_name'])
if not os.path.exists(full_path):
    os.mkdir(full_path)


###### VIDEO CONFIG ######

cap = cv2.VideoCapture(video_path)
cap.set(cv2.CAP_PROP_POS_FRAMES, int(choices['time_start']))

frame_rate = cap.get(cv2.CAP_PROP_FPS)
distance_per_frame = 1 / frame_rate # 1 meter per second speed, captured each second
capture_interval = 0.05  # meters
frames_to_skip = int(capture_interval / distance_per_frame)



###### PRESET HELPER VARIABLES  ######

current_detection_list = []
res_of_last_detection = [-10, -10]
detection_score = [0, 0]
frame_count = 0
last_keyed_frame = []


###### CAPTURE RUN ######

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    print(f'\rFrame Count: {frame_count}', end='', flush=True)
    frame = np.rot90(frame)
    # PERFORMING YOLO TO RETRIEVE OBJECTS
    is_detected_state, cropped_image = yolo_instance.process(frame)

    detection_score = {}

    # IF OBJECT IS DETECTED THEN RUN CLIP CLASSIFIER
    if is_detected_state:
        keyed_frame = cropped_image
        if choices['decision_tree'] == True:
            detection_score, parent_averages = clip_instance.clip_decision_tree(keyed_frame, choices['rotation'])

        else:
            detection_score = clip_instance.clip_decision_plain(keyed_frame, choices['rotation'])
        # CHECK IF SAME OBJECT IS DETECTED MULTIPLE TIMES WITHIN RANGE
        if (frame_count - 3 <= res_of_last_detection[1]):  
            current_detection_list.append(detection_score)
            last_keyed_frame = keyed_frame

        # ELSE FIRST DETECTION
        else:
            res_of_last_detection = [detection_score, frame_count]
            current_detection_list.append(detection_score)

    # REALEASE OBJECT
    elif not is_detected_state and len(last_keyed_frame) != 0: 
        avg_total, max_item = calculate_averages(current_detection_list)
        cv2.imwrite(f"{full_path}/frame{frame_count}_{max_item}.jpg", last_keyed_frame)
        last_keyed_frame = []
        current_detection_list = []

    frame_count += 1


###### CAPTURE RELEASE ######

cap.release()

print('Sequence completed...')


###### SAVE OUT PLOT ######


print("Creating plot...")
 # Replace with your folder path
images, filenames = load_images_from_folder(full_path)
plot_images(images, filenames, full_path)

print("Plot saved...")