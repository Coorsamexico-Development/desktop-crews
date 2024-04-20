import os
from pathlib import Path

class KerasRepository:
    def __init__(self):
        pass
    
    def get_models():
        path = os.path.join(os.getcwd(), "assets", "saved_model")

        models = [{"name": f"Red Neuronal {directory.name}",
                   
                "path": os.path.join(path, directory.name)} for directory in Path(path).iterdir() if directory.is_dir()]
        return models

        