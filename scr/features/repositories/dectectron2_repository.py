import os
from pathlib import Path

from detectron2.utils.logger import setup_logger
setup_logger()


# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
import matplotlib.pyplot as plt

CATEGORY_NAMES = {
                    0: 'tornillo_chico',
                }

class Dectectron2Repository:
    history_model = {} 

    def __init__(self,categories = None):
        self.categories = categories
        self.cfg = get_cfg()
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")  # Let training initialize from model zoo
        self.cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128   # The "RoIHead batch size". 128 is faster, and good enough for this toy dataset (default: 512)
        self.cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
        self.path = os.path.join(os.getcwd(), "assets", "models-dectectron2")
        if not os.path.exists(self.path):
            os.makedirs(self.path)
    

    
    def get_models(self):
      
        models = []
        #models = [{"name": f"Red Neuronal {directory.name}",
        #           "path": os.path.join(path, directory.name),
        #           "categories": self.__set_categories(directory.name)
        #        } for directory in Path(path).iterdir() if directory.is_dir()]
        dirs = [dir.name for dir in Path(self.path).iterdir() if dir.is_dir() ]

        for dir in dirs:
            models.append(
                {
                   "name": f"Red {dir}",
                   "path": os.path.join(self.path, dir),
                   "categories": self.__set_categories(dir)
                } 
            )

        return models
    
    def load_model(self,model):
        model_path = model["path"]
        model_name = model["name"]
        model_categories = model["categories"]
        model_loaded = None
        if model_name in self.history_model:
            model_loaded= self.history_model[model_name]
        else:
            self.cfg.MODEL.WEIGHTS = os.path.join(model_path, "model_final.pth")  # path to the model we just trained
            self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.74   # set a custom testing threshold
            self.cfg.MODEL.ROI_HEADS.NUM_CLASSES = len(model_categories.keys())
            predictor = DefaultPredictor(self.cfg)
            model_loaded = predictor
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

        