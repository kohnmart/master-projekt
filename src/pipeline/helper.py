import os


def get_all_samples():
    
    file_names = []

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

    relative_path = 'dataset/classifier/train/dress'

    folder_path = os.path.join(project_root, relative_path)

    # Walk through all files and directories recursively
    for root, dirs, files in os.walk(folder_path):
        # Iterate over files in the current directory
        for filename in files:
            fullpath = os.path.join(folder_path, filename)
            file_names.append([filename, fullpath])
    
    return file_names


