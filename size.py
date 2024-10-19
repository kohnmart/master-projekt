import os

def get_folder_size(folder_path):
    total_size = 0
    # Walk through all subdirectories and files
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            # Add the file size to the total
            total_size += os.path.getsize(file_path)
    
    return total_size

# Specify the folder path
folder_path = './src/output'

# Convert the size to MB
size_in_mb = get_folder_size(folder_path) / (1024 * 1024)

print(f"Folder size: {size_in_mb:.2f} MB")
