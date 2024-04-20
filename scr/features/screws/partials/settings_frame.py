import tkinter as tk
from scr.config.styles import Styles
from tkinter import ttk

class SettingsFrame(tk.Frame):
    
    camaras = []

    def __init__(self, screen, on_predict = lambda:None, on_change_camara= lambda i,text:None):
        super().__init__(screen,**Styles.frame_style())
        self.on_change_camara = on_change_camara
        self.text_selected = tk.StringVar(self)

        self.text_camara_selected = tk.StringVar(self)



        self.label_model = tk.Label(self, text="MODELO:", **Styles.label_normal_style() )
        self.label_model.grid(
            pady=2,
            padx=10,
            row=0,
            column=0
        )
        # widget model
        self.models_combobox = ttk.Combobox(self,
                                values=(),
                                textvariable=self.text_selected,
                                state="readonly", 
                                **Styles.combobox_style())
        self.models_combobox.grid(
            pady=2,
            row=0,
            column=1
        )

        self.label_model = tk.Label(self, text="CAMARA:", **Styles.label_normal_style())
        self.label_model.grid(
            pady=2,
            padx=10,
            row=1,
            column=0,
        )
        self.button_predict = tk.Button(
            self,
            text="COMENZAR PREDICIONES",
            **Styles.button_style()
        )

        self.button_predict.grid(
            pady=5,
            row=2,
            column=1,
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

        self.button_predict.config(command=on_predict)


    def set_values_combobox(self,values= ()):
         self.combobox_camara["values"] = values
         if len(self.combobox_camara["values"]) > 0:
            self.combobox_camara.current(0)


    def change_camara(self,_):
        current_index = self.combobox_camara.current()
        self.on_change_camara(current_index, self.text_camara_selected.get())
         # Elegimos la camara con la que vamos a hacer la deteccion


    
    
