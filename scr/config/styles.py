import tkinter as tk

#defaul Colors
BACKGROUND_COLOR = "black"
FG_COLOR ="white"


class Styles:
        
        @staticmethod
        def screen_style():
             return {
                "geometry": "1000x600",
                "minsize":(800, 600),
                "attributes": ('-alpha', 0.8)
             }

        @staticmethod
        def frame_style(bg = "black"):
             return {
                "bg": bg,
                "bd":1,
                "relief": tk.SOLID
             }
        
        @staticmethod
        def label_style(bg_color=BACKGROUND_COLOR, fg_color=FG_COLOR, font=("Arial", 16)):
               return {
                      "bg": bg_color,
                      "fg": fg_color,
                      "font": font,
               }
        