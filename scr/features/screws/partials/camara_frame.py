import tkinter as tk
from scr.config.styles import Styles
from scr.utils.capture_camaras import CaptureCameras
PADDING_X = 80
PADDING_Y = 20

class CamaraFrame(tk.Frame):

    playing = False

    def __init__(self, screen, captura_cameras = CaptureCameras()):
        super().__init__(screen,
                         **Styles.frame_style())
        self.captura_cameras = captura_cameras
        self.label_camera = tk.Label(self, **Styles.label_title_style())
        self.label_camera.pack(
            fill=tk.BOTH,
            expand=True,
            padx=PADDING_X,
            pady=PADDING_Y
        )
        self.update_image_label()

    def resize_image(self, height = None):
        if height is None:
            height = self.winfo_height()-24
        self.captura_cameras.size = (self.winfo_width() -PADDING_X,height-PADDING_Y)

    def start_video(self):
        if self.playing:
            return
        self.playing = True
        
        self.capture_video()
    
    def capture_video(self):
        with_image = self.update_image_label()
        
        if self.playing and with_image:
            self.after(ms=5, func= self.capture_video)
            
        
    def update_image_label(self):
        with_image, photo_image = self.captura_cameras.capture_frame()
        self.label_camera.photo_image = photo_image
        self.label_camera.configure(image=photo_image)
        return with_image
    
    
    def stop_video(self):
         self.playing = False
         self.after(10, self.captura_cameras.leave_camera)


        

    
