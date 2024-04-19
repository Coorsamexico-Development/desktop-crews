import tkinter as tk
from scr.config.styles import Styles
from scr.utils.capture_camaras import CaptureCameras

class SettingsFrame(tk.Frame):
    

    def __init__(self, screen, captura_cameras = CaptureCameras()):
        super().__init__(screen,**Styles.frame_style())

        self.captura_cameras = captura_cameras
        self.label_camera = tk.Label(self,text="Settings frame", **Styles.label_style())
        self.label_camera.pack(
            side="top",
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )
    
