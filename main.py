import tkinter as tk
from subprocess import Popen
import sys
import os



def run_autocubing():

    script_path = os.path.join(os.path.dirname(__file__), 'Autocubing', 'main.py')
    Popen([sys.executable, script_path])

def run_autoflaming():
    
    script_path = os.path.join(os.path.dirname(__file__), 'autoflaming', 'main.py')
    Popen([sys.executable, script_path])



root = tk.Tk()
root.title('MapleTools')
root.geometry('800x600')


autocubing_button = tk.Button(root, text='Cubing', command=run_autocubing)
autocubing_button.pack(fill='x', padx=20, pady=5)

autoflaming_button = tk.Button(root, text='Flaming', command=run_autoflaming)
autoflaming_button.pack(fill='x', padx=20, pady=7)



root.mainloop()