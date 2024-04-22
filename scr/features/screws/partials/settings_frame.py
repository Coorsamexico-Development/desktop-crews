import tkinter as tk
from dist.main._internal.PIL.ImageOps import expand
from scr.config.styles import Styles
from tkinter import ttk

class SettingsFrame(tk.Frame):
    
    is_predicting = False

    def __init__(self, screen, 
                 on_predict = lambda:None,
                 stop_predict=  lambda:None,
                 on_change_camara= lambda i,text:None,
                 on_change_model= lambda i,text:None
                 ):
        super().__init__(screen,**Styles.frame_style())
        self.on_change_camara = on_change_camara
        self.on_change_model = on_change_model
        self.on_predict = on_predict
        self.stop_predict = stop_predict
        self.text_rn_selected = tk.StringVar(self)
        self.text_camara_selected = tk.StringVar(self)



        self.label_rn_model = tk.Label(self, text="MODELO:", **Styles.label_normal_style() )
        self.label_rn_model.grid(
            pady=2,
            padx=10,
            row=0,
            column=0
        )
        # widget model
        self.combobox_rn_models = ttk.Combobox(self,
                                values=(),
                                textvariable=self.text_rn_selected,
                                state="readonly", 
                                **Styles.combobox_style())
        self.combobox_rn_models.grid(
            pady=2,
            row=0,
            column=1
        )
        
        self.combobox_rn_models.bind("<<ComboboxSelected>>", self.change_model)

        self.label_camara = tk.Label(self, text="CAMARA:", **Styles.label_normal_style())
        self.label_camara.grid(
            pady=2,
            padx=10,
            row=1,
            column=0,
        )
        
        self.combobox_camara = ttk.Combobox(self,
                               values=(),
                               textvariable=self.text_camara_selected,
                               state="readonly", 
                                **Styles.combobox_style()
                               )

        self.combobox_camara.bind("<<ComboboxSelected>>", self.change_camara)

        self.combobox_camara.grid(
            pady=2,
            row=1,
            column=1,
        )
        
        self.button_predict = tk.Button(
            self,
            text="COMENZAR PREDICIONES",
            **Styles.button_style()
        )

        self.button_predict.grid(
            row=2,
            pady=10,
            padx=5,
            columnspan=2,
            column=0,
        )
        
        self.button_predict.config(command=self.start_or_stop_predict)
        
        self.button_capturar = tk.Button(
            self,
            text="CAPTURAR PREDICION",
            **Styles.button_style()
        )

        self.button_capturar.grid(
            padx=5,
            row=3,
            columnspan=2,
            column=0,
        )
        
        self.button_predict.config(command=self.start_or_stop_predict)

        



    def set_camaras_combobox(self,values= ()):
         self.combobox_camara["values"] = values
         if len(self.combobox_camara["values"]) > 0:
            self.combobox_camara.current(0)


    def change_camara(self,_):
        current_index = self.combobox_camara.current()
        self.on_change_camara(current_index, self.text_camara_selected.get())
         # Elegimos la camara con la que vamos a hacer la deteccion
         
    def start_or_stop_predict(self):
        if self.is_predicting:
            self.stop_predict()
        else:
            self.start_predict()
            
    def set_rn_models_combobox(self,values= ()):
         self.combobox_rn_models["values"] = values
         if len(self.combobox_rn_models["values"]) > 0:
            self.combobox_rn_models.current(0)
            
    def change_model(self,_):
        current_index = self.combobox_rn_models.current()
        self.on_change_model(current_index, self.text_rn_selected.get())
    
    def start_predict(self):
        self.is_predicting = True
        self.button_predict.config(text="DETENER PREDICIONES")
        self.on_predict()
        
    def stop_predict(self):
        self.is_predicting = False
        
        self.button_predict.config(text="COMENZAR PREDICIONES")
        print("detener prediciones")
        self.stop_predict()
        


    
    
