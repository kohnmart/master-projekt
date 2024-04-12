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

def get_training_data_path(file_name=None):
    """Return the path to the directory containing training data."""
    train_path = os.path.join(get_project_root(), "dataset/train")

    folder_name = file_name.split("_")[0]

    if file_name:
        train_path = os.path.join(train_path, folder_name, file_name)
    return train_path

def get_stable_input_path():
    """Return the path to the directory containing stable diffusion input images."""
    return os.path.join(get_project_root(), "dataset/images/stable-diffusion/input")

