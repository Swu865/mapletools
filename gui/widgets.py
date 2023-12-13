import tkinter as tk
from tkinter import ttk  

class CustomOptionMenu(ttk.Frame):
    def __init__(self, parent, options, initial_value="Select Option"):
        super().__init__(parent)
        self.option_var = tk.StringVar(value=initial_value)
        self.option_menu = ttk.OptionMenu(self, self.option_var, *options)
        self.option_menu.pack(expand=True, fill='both')

    def get_value(self):
        return self.option_var.get()


class CustomRadioButtons(ttk.Frame):
    def __init__(self, parent, options, update_callback=None):
        super().__init__(parent)
        self.radio_var = tk.IntVar()

        if update_callback:
            self.radio_var.trace_add("write", update_callback)

        for i, option in enumerate(options, start=1):
            R = ttk.Radiobutton(self, text=str(option), variable=self.radio_var, value=i)
            R.grid(row=1, column=i, padx=5)

    def get_value(self):
        return self.radio_var.get()

class CustomCheckBoxes(ttk.Frame):
    def __init__(self, parent, options):
        super().__init__(parent)
        self.check_vars = {option: tk.BooleanVar() for option in options}

        for i, (text, var) in enumerate(self.check_vars.items(), start=1):
            C = ttk.Checkbutton(self, text=text, variable=var, onvalue=True, offvalue=False)
            C.grid(row=i, column=2, padx=(20, 5))
 
    def get_checked_values(self):
        return {text: var.get() for text, var in self.check_vars.items()}


class CustomButton(ttk.Frame):
    def __init__(self, parent, text, command):
        super().__init__(parent)
        self.button = ttk.Button(self, text=text, command=command)
        self.button.grid(row=0, column=0, pady=10, padx=(100, 0))

class CustomLabel(ttk.Frame):
    def __init__(self, parent, text="", **kwargs):
        super().__init__(parent)
        self.text_var = tk.StringVar(value=text)
        self.label = ttk.Label(self, textvariable=self.text_var, **kwargs)
        self.label.pack(expand=True, fill='both')
        
    def set_text(self, text):
        self.text_var.set(text)
    def get_text(self):
        return self.text_var.get()