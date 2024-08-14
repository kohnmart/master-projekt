from PIL import Image
import os

def rotate_images_in_folder(folder_path, rotation_angle):
    # Ensure the folder exists
    if not os.path.isdir(folder_path):
        raise NotADirectoryError(f"The path {folder_path} is not a directory.")
    
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        # Construct the full file path
        file_path = os.path.join(folder_path, filename)
        
        # Check if the file is an image (you can add more extensions if needed)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # Open the image file
            with Image.open(file_path) as img:
                # Rotate the image
                rotated_img = img.rotate(rotation_angle, expand=True)
                
                # Save the rotated image back to the same path
                rotated_img.save(file_path)
                #print(f"Rotated and saved: {filename}")
