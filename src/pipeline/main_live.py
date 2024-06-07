import cv2
import time
from sam import SAM
from helper import get_all_samples
from mongo import MONGO
from clip import ClipClassifier
from yolo import YOLOS
import numpy as np

print('Launching...')

sam_instance = SAM()
clip_instance = ClipClassifier()
yolo_instance = YOLOS(700)
# Path to the video file
video_path = './stream_video/1.mp4'

# Initialize a video capture object
cap = cv2.VideoCapture(video_path)

# Frame rate of the video
frame_rate = cap.get(cv2.CAP_PROP_FPS)
print(frame_rate)
# Distance an object moves per frame (in meters)
distance_per_frame = 1 / frame_rate # 1 meter per second speed, captured each second

# Decide on the physical distance over which you want to capture frames (e.g., every 10 cm)
capture_interval = 0.05  # meters

# Calculate the number of frames to skip to capture the desired spatial interval
frames_to_skip = int(capture_interval / distance_per_frame)

frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    if frame_count % frames_to_skip == 0:
        # Save or process the frame
        # Pipeline Entry for Cloth Detection and Classification
        print(f"Processing frame {frame_count}")

        state = yolo_instance.process(frame)

        if state:
            masks = sam_instance.image_processor(frame=frame)
            cleaned_masks = sam_instance.clean_masks(masks, range=[60000, 160000])

            cloth_objects, cleaned_compared_masks = sam_instance.separate_by_bbox(cleaned_masks, frame, True, False)
            
            for i, cloth in enumerate(cloth_objects):
                cv2.imwrite(f"output/frame_{frame_count}_{i}.jpg", cloth)

        else:
            print("No object in center place")
    
    frame_count += 1

# Release the video capture object
cap.release()
