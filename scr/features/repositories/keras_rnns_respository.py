import os
from pathlib import Path
import tensorflow as tf

CATEGORY_NAMES = {
                    0: 'tornillo tirafondo largo',
                    1: 'lag tornillo para madera',
                    2: 'tornillo para madera', 
                    3: 'tornillo corto para madera',
                    4: 'tornillo brillante',
                    5: 'tornillo de óxido negro', 
                    6: 'tuerca pequeña',  
                    7: 'perno',
                    8: 'tuerca grande',
                    9: 'tuerca mediana-pequeña',
                    10: 'tuerca mediana',
                    11: 'machine screw', 
                    12: 'short machine screw'
                }

class KerasRnnsRepository:
    history_model = {} 

    def __init__(self,categories = None):
        self.categories = categories
    

    
    def get_models(self):
        path = os.path.join(os.getcwd(), "assets", "models")

        models = [{"name": f"Red Neuronal {directory.name}",
                   "path": os.path.join(path, directory.name),
                   "categories": self.__set_categories(directory.name)
                } for directory in Path(path).iterdir() if directory.is_dir()]
        return models
    
    def load_model(self,model):
        model_path = model["path"]
        model_name = model["name"]
        model_loaded = None
        if model_name in self.history_model:
            model_loaded= self.history_model[model_name]
        else:  
            model_loaded = tf.keras.models.load_model(model_path, compile=False, safe_mode=False)
            self.history_model[model_name] = model_loaded
        
        return model_loaded, model['categories']
    
    def __set_categories(self, rn):
        if self.categories is None:
            return CATEGORY_NAMES
        else:
            return self.categories[rn]

        