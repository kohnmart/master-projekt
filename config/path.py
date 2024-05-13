import os

def get_project_root():
    """Return the root directory of the project."""
    return os.path.dirname(os.path.dirname(__file__))

def get_models_path():
    """Return the path to the directory containing models."""
    return os.path.join(get_project_root(), 'src/models_export/multi_models/pytorch')

def get_processed_images_path(version=None):
    """Return the path to the directory containing processed images."""
    processed_path = os.path.join(get_project_root(), "dataset/images/evaluate/processed")
    if version:
        processed_path = os.path.join(processed_path, version)
    return processed_path

def get_evaluation_path():
    """Return the path to the evaluation directory."""
    return os.path.join(get_project_root(), 'src/evaluation')

def get_checkpoint_path(name=None):
    """Return the path to the directory containing model checkpoint files."""
    checkpoint_path = os.path.join(get_project_root(), 'src/pipeline/model_weights')
    if name:
        checkpoint_path = os.path.join(checkpoint_path, name)
    return checkpoint_path

def get_training_data_path(data_type=None, file_name=None, class_type=None):
    """Return the path to the directory containing training data."""
    train_path = os.path.join(get_project_root(), f"dataset/{data_type}/train")

    if class_type:
        train_path = os.path.join(train_path, class_type)

    if file_name:
        train_path = os.path.join(train_path, file_name)
    return train_path

def get_stable_input_path():
    """Return the path to the directory containing stable diffusion input images."""
    return os.path.join(get_project_root(), "dataset/generator/input")

def get_stable_output_path():
    """Return the path to the directory containing stable diffusion output images."""
    return os.path.join(get_project_root(), "dataset/generator/output")

def get_all_files_from_folder(folder_path):
    """Return a list of all files in a folder."""
    return os.listdir(folder_path)

class DATASET_PATH_TYPE:
    """Class to define constants for different types of paths."""
    classifier = 'classifier'
    generator = 'generator'
    segmentator = 'segmentator'
