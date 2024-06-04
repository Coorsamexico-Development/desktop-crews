from email.mime import image
from typing import List
import numpy as np

import tkinter as tk
from scr.config.styles import Styles
from scr.utils.capture_camaras import CaptureCameras
from scr.utils.detectron2_rn import PredicDetectron2, PredictResult
from PIL import  ImageTk,Image


class CamaraFrame(tk.Frame):

    playing = False
    model = None
    categories = None
    predictDetectron = PredicDetectron2()
    size_camara = (256,256)
    predictions = []
    num_frame = 0
    show_boxes = True
    show_segments = True

    def __init__(self, screen, captura_cameras = CaptureCameras()):
        super().__init__(screen,
                         **Styles.frame_style())
        self.captura_cameras = captura_cameras
        self.label_camera = tk.Label(self, **Styles.label_title_style())
        self.label_camera.pack(
            fill=tk.BOTH,
            expand=True,
        )
        _, frame = self.captura_cameras.capture_frame()
        self.update_image_label(frame)

    def resize_image(self, height = None):
        if height is None:
            height = self.winfo_height()-24
        
        self.size_camara = (self.winfo_width(),height)

    def start_video(self):
        if self.playing:
            return
        self.playing = True
        is_open = self.captura_cameras.set_camera(self.captura_cameras.camara_index)
        must_predict = self.categories is not None and is_open
        self.capture_video(must_predict=must_predict)
    
    def capture_video(self, must_predict = False):
        with_image, frame = self.captura_cameras.capture_frame()
        if must_predict: 
            predictions, image_numpy =  self.predictions_frame(frame)
            frame = self.draw_predictions(image_numpy, predictions)
        self.update_image_label(frame)
        
        if self.playing and with_image:
            self.after(ms=20, func= lambda:self.capture_video(must_predict))
            
    def predictions_frame(self, frame:Image, optimize:bool = True):
        
        self.num_frame+1
        if optimize and self.num_frame % 10 != 0:
            image_numpy = np.array(frame)
            predicitions = self.predictions
        else:
            self.num_frame=0
            predicitions, image_numpy = self.predictDetectron.predict_rn(self.model, self.categories, frame)
            self.predictions = predicitions
        
        return predicitions, image_numpy
       
    def draw_predictions(self, image_predict,predictions:List[PredictResult]):
        return self.predictDetectron.draw_boxes(image=image_predict,predictions=predictions,show_boxes=self.show_boxes, show_segments=self.show_segments)
       
            

            
    
    def update_image_label(self, frame):         
        image = frame.resize(self.size_camara)
        photo_image = ImageTk.PhotoImage(image)
        self.label_camera.photo_image = photo_image
        self.label_camera.configure(image=photo_image)
    
    
    def stop_video(self):
         self.playing = False
         with_image, frame = self.captura_cameras.capture_frame()
         self.after(30, self.captura_cameras.leave_camera)
         return with_image, frame


        

    
