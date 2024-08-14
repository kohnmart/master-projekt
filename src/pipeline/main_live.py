import cv2
import numpy as np
from modules.yolo import YOLOS
from modules.helper import rotate_image
from modules.clip import ClipClassifier, ClipFast
from modules.keying import keying

print('Launching...')

clip_instance = ClipFast(model_name='ViT-B/16')
yolo_instance = YOLOS()
# Path to the video file

video_path = './stream_video/' + 'recording_2024-08-14.avi'

print('Running...')

# Initialize a video capture object
cap = cv2.VideoCapture(video_path)
cap.set(cv2.CAP_PROP_POS_FRAMES, 180)

frame_rate = cap.get(cv2.CAP_PROP_FPS)
distance_per_frame = 1 / frame_rate # 1 meter per second speed, captured each second
capture_interval = 0.05  # meters
frames_to_skip = int(capture_interval / distance_per_frame)

block_paired = []

res_last_detection = [-10, -10]
res = [0, 0]
frame_count = 0
last_keyed_frame = []
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    print(frame_count)
    #frame = np.rot90(frame)
    #cv2.imwrite(f"output/stream6/frame_{frame_count}__.jpg", frame)
    is_detected_state, cropped_image = yolo_instance.process(frame)

    if is_detected_state:
        #keyed_frame = keying(cropped_image)
        keyed_frame = cropped_image
        clip_instance.image = keyed_frame
        res = clip_instance.process(keyed_frame)
        if (frame_count - 3 <= res_last_detection[1]):  
            print("Detected same object")
            block_paired.append(res)
            last_keyed_frame = keyed_frame


        else:
            res_last_detection = [res[0], frame_count]
            block_paired.append(res)

    
    else: 
        if len(last_keyed_frame) != 0:
            sorted_paired = sorted(block_paired, key=lambda x: x[1], reverse=True)
            #cv2.imwrite(f"output/stream8/frame_{frame_count}_{res[0]}__.jpg", last_keyed_frame)
            last_keyed_frame = []
            block_paired = []

    frame_count += 1

# Release the video capture object
cap.release()

print('Finished...')

