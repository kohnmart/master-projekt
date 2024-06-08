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
yolo_instance = YOLOS(stream_width=700)
# Path to the video file
video_path = './stream_video/2.mp4'

# Initialize a video capture object
cap = cv2.VideoCapture(video_path)

# Frame rate of the video
frame_rate = cap.get(cv2.CAP_PROP_FPS)

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
        is_detected_state, cropped_image = yolo_instance.process(frame)
        if is_detected_state:
            #cv2.imwrite(f"output/v7/frame_{frame_count}test.jpg", cropped_image)
            masks = sam_instance.image_processor(frame=cropped_image)
            cleaned_masks = sam_instance.clean_masks(masks, range=[30000, 160000])

            cloth_objects, cleaned_compared_masks = sam_instance.separate_by_bbox(cleaned_masks, cropped_image, True, False)
            
            for i, cloth in enumerate(cloth_objects):
                clip_instance.image = cloth
                res = clip_instance.classifier()
                cv2.imwrite(f"output/v8/frame_{frame_count}__{res[0]}_{i}.jpg", cloth)

    frame_count += 1

# Release the video capture object
cap.release()
