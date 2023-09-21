import tkinter as tk
import customtkinter as ctk
from tools.autocubing import main as autocubing_main
import threading

def autocubing_toggle():
    if "Start" in autocubing_button.cget("text"):
        start_autocubing()
        autocubing_button.configure(text="Stop", command=stop_autocubing)
    else: 
        stop_autocubing()
        
def start_autocubing():
    global autocubing_thread
    global stop_event
    selected_potential = potential_var.get()
    stop_event = threading.Event()
    stop_event.clear()
    autocubing_thread = threading.Thread(target=autocubing_main, args=(selected_potential, stop_event))
    autocubing_thread.start()

def stop_autocubing():
    global stop_event
    if stop_event:
        stop_event.set()
    autocubing_thread.join()  
    autocubing_button.configure(text="Start", command=autocubing_toggle)


root = ctk.CTk()
root.title("MapleTools")
root.geometry("1000x800")

label = ctk.CTkLabel(root, text="Auto Cubing")
label.pack(pady=20)

potential_var = ctk.StringVar(value="Select potential")

potential_options = ["STR", "DEX", "INT", "LUK"]
option_menu = tk.OptionMenu(root, potential_var, *potential_options)
option_menu.pack(pady=20)

autocubing_button = ctk.CTkButton(root, text="Start", command=autocubing_toggle)
autocubing_button.pack(pady=20)

root.mainloop()


