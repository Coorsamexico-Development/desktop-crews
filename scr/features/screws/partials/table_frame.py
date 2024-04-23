from typing import List
import tkinter as tk
from tkinter import ttk

from scr.config.styles import Styles
from scr.utils.predict_rn_yolov8 import PredictResult

class TableFrame(tk.Frame):
    
    predictions: List[PredictResult] = []
    
    def __init__(self, screen, on_select: lambda r,p:None):
        super().__init__(screen,**Styles.frame_style())
        self.on_select = on_select
        self.table = ttk.Treeview(self, 
                           columns=('num', 'category', 'cant'),
                            show='headings', )
        self.table.heading('num', text="Num.", )
        self.table.heading('category', text="Tornillos", )
        self.table.heading('cant', text="Cantidad")
        
        self.table.pack(
            side="left",
            fill=tk.BOTH,
            expand=True,
        )
        
        self.table.bind("<<TreeviewSelect>>", self.select_table)
    
    def clear_table(self):
        for i in self.table.get_children():
            self.table.delete(i)
            
    def insert_row(self, index, cateory, cant):
        self.table.insert(parent='', index=index, values=(index+1, cateory, cant))
        
    
    def update_prediction(self, predictions: List[PredictResult] = []):
    
        self.clear_table()
        
        for index, p in enumerate(predictions):
            self.insert_row(index, p.name, p.total)
            
        self.predictions= predictions
            
    def select_table(self, _):
        rows_selections = self.table.selection()
        predictions_selected: List[PredictResult] =[]
        for item in rows_selections:
                index = self.table.item(item)['values'][0] - 1
                predictions_selected.append(self.predictions[index])
        
        
        self.on_select(rows_selections, predictions_selected)
        

        
    