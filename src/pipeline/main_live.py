import cv2
import time
from sam import SAM
from mongo import MONGO
from yolo import YOLOS
from helper import get_all_samples
from clip import ClipClassifier
import numpy as np
from keying import keying


def rotate_image(image, angle):
    # Get the dimensions of the image
    (height, width) = image.shape[:2]
    
    # Calculate the center of the image
    center = (width // 2, height // 2)
    
    # Get the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Perform the rotation
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))
    
    return rotated_image

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
wait_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    if wait_count == 0:
        frame = rotate_image(frame, -90)
        is_detected_state, cropped_image = yolo_instance.process(frame)
        #cv2.imwrite(f"output/v10/frame_{frame_count}_.jpg", frame)
        if is_detected_state:
            keyed_frame = keying(cropped_image)
            wait_count = 1
            #cv2.imwrite(f"output/v7/frame_{frame_count}test.jpg", cropped_image)
            #masks = sam_instance.image_processor(frame=cropped_image)
            #cleaned_masks = sam_instance.clean_masks(masks, range=[30000, 160000])

            clip_instance.image = keyed_frame
            res = clip_instance.classifier()
            cv2.imwrite(f"output/v10/frame_{frame_count}_{res[0]}_.jpg", keyed_frame)


            #cloth_objects, cleaned_compared_masks = sam_instance.separate_by_bbox(cleaned_masks, cropped_image, True, False)
            
            # for i, cloth in enumerate(cloth_objects):
            #     clip_instance.image = cloth
            #     res = clip_instance.classifier()
            #     cv2.imwrite(f"output/v8/frame_{frame_count}__{res[0]}_{i}.jpg", cloth)

    else:
        wait_count -= 1

    frame_count += 1

# Release the video capture object
cap.release()


