import tkinter as tk
from scr.config.styles import Styles
from scr.utils.capture_camaras import CaptureCameras


class CamaraFrame(tk.Frame):

    playing = False
    camara = 0

    def __init__(self, screen, captura_cameras = CaptureCameras()):
        super().__init__(screen,
                         **Styles.frame_style())
        self.captura_cameras = captura_cameras
        self.label_camera = tk.Label(self, **Styles.label_style())
        self.label_camera.pack(
            fill=tk.BOTH,
            expand=True,
            padx=80,
            pady=20
        )
        self.capture_frame()

    def resize_image(self, height = None):
        if height is None:
            height = self.winfo_height()-24
        self.captura_cameras.size = (self.winfo_width() -80,height-20)

    def start_video(self):
        if self.playing:
            return
        self.playing = True
        self.captura_cameras.start()
        self.capture_video()
    
    def capture_video(self):
        with_image = self.capture_frame()
        
        if self.playing and with_image:
            self.after(ms=5, func= self.capture_video)
            
        
    def capture_frame(self):
        with_image, photo_image = self.captura_cameras.capture_frame()
        self.label_camera.photo_image = photo_image
        self.label_camera.configure(image=photo_image)
        return with_image
    
    
    def stop_video(self):
         self.playing = False
         self.after(10, self.captura_cameras.cap.release)


        

    
