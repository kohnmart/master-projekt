import cv2
import numpy as np
import os 
from modules.yolo import YOLOS
from modules.helper import rotate_image
from modules.clip import ClipClassifier, ClipFast
from modules.keying import keying
from modules.helper import load_images_from_folder, plot_images
print('Launching...')

clip_instance = ClipFast(model_name='ViT-B/16')
yolo_instance = YOLOS()
# Path to the video file

file_name = 'stream3.mp4'


video_path = './stream_video/' + file_name

file_name = file_name.split('.')[0]
full_path = os.path.join('output', file_name)

if not os.path.exists(full_path):
    os.mkdir(full_path)
print('Running...')

# Initialize a video capture object
cap = cv2.VideoCapture(video_path)
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

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

    is_detected_state, cropped_image = yolo_instance.process(frame)

    if is_detected_state:
        #keyed_frame = keying(cropped_image)
        keyed_frame = cropped_image
        clip_instance.image = keyed_frame
        clip_instance.classes = ['dress', 'skirt', 'jacket', 'shirt', 'tshirt', 'pant', 'short']
        res = clip_instance.rotate_wise(keyed_frame)
        print("FIRST RES")
        print(res)

        if res == 'pant':
            clip_instance.classes = ['pant', 'skirt', 'short']
            res = clip_instance.rotate_wise(keyed_frame)

        if res == 'shirt':
            clip_instance.classes = ['sweat-shirt', 'polo-shirt']
            res = clip_instance.rotate_wise(keyed_frame)


        if (frame_count - 3 <= res_last_detection[1]):  
            print("Detected same object")
            block_paired.append(res)
            last_keyed_frame = keyed_frame


        else:
            res_last_detection = [res, frame_count]
            block_paired.append(res)

    
    else: 
        if len(last_keyed_frame) != 0:
            sorted_paired = sorted(block_paired, key=lambda x: x[1], reverse=True)
            cv2.imwrite(f"{full_path}/frame_{frame_count}_{res}__.jpg", last_keyed_frame)
            last_keyed_frame = []
            block_paired = []

    frame_count += 1

# Release the video capture object
cap.release()

print('Finished...')

print("Creating plot...")
 # Replace with your folder path
images, filenames = load_images_from_folder(full_path)
plot_images(images, filenames, full_path)

