import os


class PathHelper:

    """Helper class for path operations."""
    
    def __init__(self):
        pass
    
    @staticmethod
    def list_files(directory, extension='*'):
        """List files in a directory with a specific extension."""
        return directory.files(extension)
    
    @staticmethod
    def join_paths(*paths):
        """Join multiple paths together."""
        return os.path.join(*paths)
    
    @staticmethod 
    def get_full_cloth_type_path(sample_name):
        type = sample_name.split("_")[0]
        root = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(root, './dataset/train/', type, sample_name)
        
        

