import tkinter as tk
from scr.config.styles import Styles
from scr.utils.capture_camaras import CaptureCameras
from scr.utils.predict_rn_yolov8 import PredictRnYolov8
from PIL import  ImageTk



class CamaraFrame(tk.Frame):

    playing = False
    model = None
    categories = None
    yolov8 = PredictRnYolov8()
    size_camara = (256,256)

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
        self.captura_cameras.set_camera(self.captura_cameras.camara_index)
        self.capture_video()
    
    def capture_video(self):
        with_image, frame = self.captura_cameras.capture_frame()
        self.update_image_label(frame)
        
        if self.playing and with_image:
            self.after(ms=20, func= self.capture_video)
            
    
    
    def update_image_label(self, frame):
        photo_image = None
        predictions = []
        if self.categories is None:
            image = frame
        else:
            frame = frame.resize((256,256))
            predictions, image_predict = self.yolov8.predict_rn(self.model, self.categories, frame)
            image = self.yolov8.draw_boxes(image=image_predict,predictions=predictions )
            
        image = image.resize(self.size_camara)
        photo_image = ImageTk.PhotoImage(image)
        
        self.label_camera.photo_image = photo_image
        self.label_camera.configure(image=photo_image)
        return predictions
    
    
    def stop_video(self):
         self.playing = False
         with_image, frame = self.captura_cameras.capture_frame()
         self.after(30, self.captura_cameras.leave_camera)
         return with_image, frame


        

    
