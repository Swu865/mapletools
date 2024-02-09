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

    def get(self):
        
        index = self.radio_buttons.get_value()
        
        if index == 1:
            return "Red"
        elif index == 2:
            return "Black"


class SelectItem(ttk.Frame):
    def __init__(self, parent, text: str, options: list):
        super().__init__(parent)
        # Assuming CustomLabel is a class you've defined elsewhere that creates a label
        self.label = ttk.Label(self, text=text)  
        self.options = CustomOptionMenu(self, options)

        self.label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))  
        self.options.grid(row=0, column=1, sticky="ew")

        # This makes the option menu expand to fill the cell in the grid
        self.grid_columnconfigure(1, weight=1)

    def get(self):
        return self.options.get_value()

    def update_options(self, new_options):
        self.options.update_options(new_options)
