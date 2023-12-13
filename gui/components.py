import tkinter as tk
from tkinter import ttk  

from .widgets import CustomRadioButtons ,CustomCheckBoxes,CustomLabel,CustomOptionMenu,CustomButton



class SelectCube(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.label = CustomLabel(self, "Select Cube Type")
        self.radio_buttons = CustomRadioButtons(self,["Red","Black"])

        self.label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))  
        self.radio_buttons.grid(row=0, column=1)

    def get_selected_cube(self):
        return self.radio_buttons.get_value()

    

class SelectItem(ttk.Frame):
    def __init__(self,parent,text:str,options:list):
        super().__init__(parent)
        self.label = CustomLabel(self, text=text)
        self.options = CustomOptionMenu(self, options=options)

        self.label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))  
        self.options.grid(row=0, column=1)

    def get_selected_value(self):
        return self.options.get_value()
    
