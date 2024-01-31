import tkinter as tk
from tkinter import ttk ,scrolledtext

class CustomOptionMenu(ttk.Frame):
    def __init__(self, parent, options, initial_value="Select Option"):
        super().__init__(parent)
        self.option_var = tk.StringVar(value=initial_value)
        self._create_option_menu(options)

    def _create_option_menu(self, options):
        if hasattr(self, 'option_menu'):
            self.option_menu.destroy()  # Destroy the existing OptionMenu widget
        self.option_menu = ttk.OptionMenu(self, self.option_var, self.option_var.get(), *options)
        self.option_menu.pack(expand=True, fill='both')

    def get_value(self):
        return self.option_var.get()

    def update_options(self, options):
        # Update the options in the OptionMenu
        self._create_option_menu(options)
        # Reset the value of the option_var
        if options:
            self.option_var.set(options[0])
        else:
            self.option_var.set("Select Option")


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
    def get_button_text(self):
        return self.button.cget("text")

        

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

class CustomScrolledText(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.text_widget = scrolledtext.ScrolledText(self, **kwargs)
        self.text_widget.pack(expand=True, fill='both')

    def insert_text(self, text, index=tk.END):
        self.text_widget.insert(index, text)
        self.text_widget.see(index)

    def get_text(self, start="1.0", end=tk.END):
        return self.text_widget.get(start, end)

    def clear_text(self):
        self.text_widget.delete("1.0", tk.END)

    def set_state(self, state):
        self.text_widget.config(state=state)