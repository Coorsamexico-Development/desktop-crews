import os
import tensorflow as tf
import keras_cv


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
        self.backbone = keras_cv.models.YOLOV8Backbone.from_preset(
                "yolo_v8_m_backbone"  # We will use yolov8 small backbone with coco weights
            )
    

    
    def get_models(self):
        path = os.path.join(os.getcwd(), "assets", "models")
        models = []
        #models = [{"name": f"Red Neuronal {directory.name}",
        #           "path": os.path.join(path, directory.name),
        #           "categories": self.__set_categories(directory.name)
        #        } for directory in Path(path).iterdir() if directory.is_dir()]
        archivos = os.listdir(path)

        for archivo in archivos:
            models.append(
                {"name": f"Red {archivo}",
                   "path": os.path.join(path, archivo),
                   "categories": self.__set_categories(archivo)
                } 
            )

        return models
    
    def load_model(self,model):
        model_path = model["path"]
        model_name = model["name"]
        model_loaded = None
        if model_name in self.history_model:
            model_loaded= self.history_model[model_name]
        else:
            model_loaded = tf.keras.models.load_model(model_path,
                                          compile=False, 
                                          safe_mode=False,
                                          custom_objects= {
                                              'YOLOV8Detector': keras_cv.models.YOLOV8Detector(
                                                   num_classes=len(model['categories']),
                                                    bounding_box_format="xywh",
                                                    backbone=self.backbone,
                                                    fpn_depth=3,
                                              ),
                                          }
                                          
                                          )
            self.history_model[model_name] = model_loaded
        
        return model_loaded, model['categories']
    
    def __set_categories(self, rn):
        if self.categories is None:
            return CATEGORY_NAMES
        else:
            if rn in self.categories:
                return self.categories[rn]
            else:
                return CATEGORY_NAMES

        