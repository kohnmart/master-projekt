import cv2
import numpy as np
import os 
from modules.yolo import YOLOS
from modules.clip import ClipFast
from modules.helper import load_images_from_folder, plot_images, calculate_averages
from modules.choices import make_choices
import pandas as pd

###### CHOICES CONFIGURATION ######

choices = make_choices()


###### SETUP ######

print('Launching...')

clip_instance = ClipFast(model_name=choices['clip'])
yolo_instance = YOLOS()


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
    print(frame_count)

    # PERFORMING YOLO TO RETRIEVE OBJECTS
    is_detected_state, cropped_image = yolo_instance.process(frame)

    # IF OBJECT IS DETECTED THEN RUN CLIP CLASSIFIER
    if is_detected_state:
        keyed_frame = cropped_image
        detection_score = clip_instance.clip_tree(keyed_frame, choices['rotation'])

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
        #sorted_paired = sorted(current_detection_list, key=lambda x: x[1], reverse=True)
        print(current_detection_list)
        avg_total, max_item = calculate_averages(current_detection_list)
        print("DETECTION LIST")
        print(avg_total)
        cv2.imwrite(f"{full_path}/frame_{frame_count}_{max_item}__.jpg", last_keyed_frame)

        # Convert original data to DataFrame
        #df_data = pd.DataFrame(current_detection_list)

        # Convert averages to DataFrame
        df_averages = pd.DataFrame([avg_total], index=['average'])

        # Concatenate the two DataFrames
        #df_combined = pd.concat([df_data, df_averages])

        # Save the combined DataFrame to CSV
        csv_file = f"{full_path}/frame_{frame_count}_{max_item}__.csv"
        df_averages.to_csv(csv_file)


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