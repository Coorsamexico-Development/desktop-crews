import tkinter as tk
import asyncio

from scr.config.styles import Styles
from scr.features.screws.partials.camara_frame import CamaraFrame
from scr.features.screws.partials.settings_frame import SettingsFrame

from scr.utils.capture_camaras import CaptureCameras


class ScrewsScreen(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Conteo de Tornillos")
        self.bind('<Escape>', lambda e: self.quit())
        # Dimesiones Anchura x Altura
        screen_style = Styles.screen_style()
        self.geometry(screen_style["geometry"])
        self.minsize(*screen_style["minsize"])
        self.attributes(*screen_style["attributes"])

        captura_cameras = CaptureCameras(size = (256,256))
        
        #add sections in screen
        self.section_camara = CamaraFrame(self,captura_cameras)
        self.section_camara.pack(fill="both", expand=False)

        self.section_settings = SettingsFrame(self,captura_cameras)
        self.section_settings.pack(fill="both", expand=True)

        self.start_services()
        self.wait_visibility()
        self.bind('<Configure>', self.window_resize)
         
    
    def start_services(self): 
        self.after(100, self.start_service_video)
        

    def start_service_video(self):
        self.section_camara.start_video()
        self.after(ms=50000, func= self.section_camara.stop_video)

    def window_resize(self,event):
        self.section_camara.resize_image(height=int((self.winfo_height())/2))

    

        



