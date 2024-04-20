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

        self.captura_cameras = CaptureCameras(size = (256,256))
        
        #add sections in screen
        self.section_camara = CamaraFrame(self,self.captura_cameras)
        self.section_camara.pack(fill="both", expand=False)

        self.section_settings = SettingsFrame(self,
                                              on_predict=self.section_camara.start_video,
                                              on_change_camara=self.on_change_camara
                                              )
        self.section_settings.pack(fill="both", expand=True)

        self.start_services()
        self.wait_visibility()
        self.bind('<Configure>', self.window_resize)
         
    
    def start_services(self): 
        self.after(100, self.start_camaras_service)
        

    def start_camaras_service(self):
        self.captura_cameras.start()
        camaras = self.captura_cameras.camaras

        values_camaras = [
                          [c  for c in camaras.keys()],
                          [c  for c in camaras.keys()]
                          ]

        self.section_settings.set_values_combobox(
            [ ca for list in values_camaras for ca in list]
        )
    


    def window_resize(self,event):
        self.section_camara.resize_image(height=int((self.winfo_height())/2))

    def on_change_camara(self, _, value):
        camaras = self.captura_cameras.camaras
        self.captura_cameras.set_camera(camara_index=camaras[value])
    

    

        



