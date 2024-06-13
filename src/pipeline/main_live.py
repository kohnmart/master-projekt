import cv2
from modules.yolo import YOLOS
from modules.helper import rotate_image
from modules.clip import ClipClassifier, ClipClassifierUpdate
from modules.keying import keying


print('Launching...')

clip_instance = ClipClassifierUpdate()
yolo_instance = YOLOS()
# Path to the video file

video_path = './stream_video/' + '3.mp4'

print('Running...')

# Initialize a video capture object
cap = cv2.VideoCapture(video_path)
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

frame_rate = cap.get(cv2.CAP_PROP_FPS)
distance_per_frame = 1 / frame_rate # 1 meter per second speed, captured each second
capture_interval = 0.05  # meters
frames_to_skip = int(capture_interval / distance_per_frame)

frame_count = 0
wait_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    #print(frame_count)
    #frame = rotate_image(frame, -90)
    is_detected_state, cropped_image = yolo_instance.process(frame)

    if is_detected_state:
        keyed_frame = keying(cropped_image)
        clip_instance.image = keyed_frame
        res = clip_instance.process(keyed_frame)
        cv2.imwrite(f"output/v15/frame_{frame_count}_{res[0]}__.jpg", keyed_frame)

    frame_count += 1

# Release the video capture object
cap.release()

print('Finished...')

