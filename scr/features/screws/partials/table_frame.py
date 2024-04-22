from ast import List
import tkinter as tk
from tkinter import ttk

from scr.config.styles import Styles

class TableFrame(tk.Frame):
    
    def __init__(self, screen):
        super().__init__(screen,**Styles.frame_style())
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
    
    def clear_table(self):
        for i in self.table.get_children():
            self.table.delete(i)
            
    def insert_row(self, index, cateory, cant):
        self.table.insert(parent='', index=index, values=(index+1, cateory, cant))
        
    
    def update_prediction(self, predictions = []):
        self.clear_table()
        for index, p in enumerate(predictions):
            self.insert_row(index, p.name, p.cantidad)

        
    