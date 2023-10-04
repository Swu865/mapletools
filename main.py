import tkinter as tk
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

# press F12 to start auto cubing
def on_press_f12(event):
    autocubing_toggle()

root = tk.Tk()
root.title("MapleTools")
root.geometry("1000x800")

# label
label = tk.Label(root, text="Auto Cubing")
label.grid(row=0, column=0)

# select drop down
potential_var = tk.StringVar(value="Select potential")
potential_options = ["STR", "DEX", "INT", "LUK","ATT","MATT","Item Drop Rate","Mesos Obtained"]
option_menu = tk.OptionMenu(root, potential_var, *potential_options)
option_menu.grid(row=1, column=0)

# number input box
desire_line_number = tk.Entry()
desire_line_number.grid(row=1,column=1)

# check box

Check_True3 = tk.Checkbutton(root, text='True 3 ', onvalue=True, offvalue=False)
Check_True3.grid(row=1,column=2)
# submit button
autocubing_button = tk.Button(root, text="Start", command=autocubing_toggle)
autocubing_button.grid(row=1, column=3)

root.bind("<F12>", on_press_f12)
root.mainloop()
