import tkinter as tk
from typing import Union
from scr.config.styles import Styles
from tkinter import ttk

class SettingsFrame(tk.Frame):
    
    is_predicting = False

    def __init__(self, screen, 
                 on_predict = lambda:None,
                 on_stop_predict=  lambda:None,
                 on_change_camara= lambda i,text:None,
                 on_change_model= lambda i,text:None,
                 on_change_show_box= lambda i,val:True,
                 on_change_show_segment= lambda i,val:True,
                 on_capture = lambda: None
                 ):
        super().__init__(screen,**Styles.frame_style())
        self.on_change_camara = on_change_camara
        self.on_change_model = on_change_model
        self.on_change_show_segment= on_change_show_segment
        self.on_change_show_box = on_change_show_box
        self.on_predict = on_predict
        self.on_capture = on_capture
        self.on_stop_predict = on_stop_predict
        self.text_rn_selected = tk.StringVar(self)
        self.check_box = tk.IntVar( value=1)
        self.check_segment = tk.IntVar( value=1)
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

        self.check_show_box = tk.Checkbutton(self, text="Mostrar Cuadros", 
            
            variable=self.check_box,
            onvalue=1, offvalue=0,

            **Styles.check_style()
            )
        self.check_show_box.config(command=self.toggle_show_box)
        
        
        
        self.check_show_box.grid(
            row=2,
            pady=10,
            padx=5,
            column=0,
        )

        self.check_show_segment = tk.Checkbutton(self, text="Mostrar Contornos", 
            
            variable=self.check_segment,
            onvalue=1, offvalue=0,

            **Styles.check_style()
            )
        
        self.check_show_segment.config(command=self.toggle_show_segment)
        
        
        self.check_show_segment.grid(
            row=2,
            pady=10,
            padx=5,
            column=1,
        )
        
        self.button_predict = tk.Button(
            self,
            text="COMENZAR PREDICIONES",
            **Styles.button_style()
        )

        self.button_predict.grid(
            row=3,
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
            row=4,
            columnspan=2,
            column=0,
        )
        
        self.button_capturar.config(command=self.capture)

        



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

    def set_model_combobox(self,value:Union[str,None]=None, index:Union[int,None]=None):
        if value != None:
            valor = value.lower()
            for i,model_text in enumerate(self.combobox_rn_models["values"]):
                if model_text.lower() == valor:
                    index = i
        if index != None:
         self.combobox_rn_models.current(index)


   
            
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
        self.on_stop_predict()
        
    def capture(self):
        self.is_predicting = False
        self.button_predict.config(text="COMENZAR PREDICIONES")
        self.on_capture()

    def toggle_show_box(self):
        self.on_change_show_box(self.check_box.get() == 1)

    def toggle_show_segment(self):
        self.on_change_show_segment(self.check_segment.get() == 1)
        


    
    
