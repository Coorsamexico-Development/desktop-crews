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
                "attributes": ('-alpha', 0.8),
                'background': BACKGROUND_COLOR
             }

        @staticmethod
        def frame_style(bg = "black"):
             return {
                "bg": bg,
                "bd":1,
                "relief": tk.SOLID
             }
        
        @staticmethod
        def label_title_style(bg_color=BACKGROUND_COLOR, fg_color=FG_COLOR, font=("Arial", 16)):
               return {
                      "bg": bg_color,
                      "fg": fg_color,
                      "font": font,
               }
        
        @staticmethod
        def label_normal_style(bg_color=BACKGROUND_COLOR, fg_color=FG_COLOR, font=("Arial", 8)):
               return {
                      "bg": bg_color,
                      "fg": fg_color,
                      "font": font,
               }
        @staticmethod
        def combobox_style(bg_color=BACKGROUND_COLOR, fg_color="black", font=("Arial", 12)):
               return {
                      "background": bg_color,
                      "foreground": fg_color,
                      "font": font,
               }
        
        @staticmethod
        def button_style(bg_color=BACKGROUND_COLOR, fg_color=FG_COLOR, font=("Arial", 14),justify='center'):
               return {
                      "bg": bg_color,
                      "fg": fg_color,
                      "font": font,
                      "justify": justify
               }
        
        @staticmethod
        def check_style(bg_color=BACKGROUND_COLOR, fg_color="blue", font=("Arial", 14),justify='center'):
               return {
                      "bg": bg_color,
                      "fg": fg_color,
                      "font": font,
                      "justify": justify
               }