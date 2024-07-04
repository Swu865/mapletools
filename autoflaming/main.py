import threading
import tkinter as tk
from tkinter import ttk
import sys
import os
# Calculate the relative path to the 'widgets.py'
script_dir = os.path.dirname(__file__)  # Get the directory where the script is running
relative_path = os.path.join(script_dir, '../autocubing/gui')
sys.path.append(relative_path)
from widgets import *
from pynput import keyboard 
from autoflaming import create_condition_callable,Autoflaming



# need  radia button group to select main stats.
# check box group to select sub stats
# need a radia button group to select att or matt
# need a entry box to input aim score , [sub,att,alls coeffi]
# need a start button
# main_stat_value 是主属 一个string，sub_stats_value 是副属性 一个list with string，att_matt_value 是选att或者matt，一个string


def main():
    global stop_event, autoflaming_thread  # Declare that we will use global variables in this function
    desired_stats_list = []
    desired_stat_dict = {}
    def start_autoflaming():
        global stop_event, autoflaming_thread
        
        desired_stat_dict = {"main":main_stat.get_selected_option(),"sub":sub_stats.get_checked_items(),"attack":att_matt.get_selected_option(),"all":"All Stats"}
        condition = create_condition_callable(float(desired_flame_entry.get()),desired_stat_dict,float(desired_sub_entry.get()),float(desired_att_entry.get()),float(desired_alls_entry.get()))

        stop_event = threading.Event()
        stop_event.clear()
        autoflaming_instance = Autoflaming(stop_event, condition)
        autoflaming_thread = threading.Thread(target=autoflaming_instance.main)  # Removed the parentheses here
        autoflaming_thread.start()

    def stop_autoflaming():
        global stop_event, autoflaming_thread
        if stop_event:
            stop_event.set()
        autoflaming_thread.join()

        run_button.configure(text="Start", command=autoflaming_toggle)

    def autoflaming_toggle():
        

        if run_button.cget("text") == "Start" :

            run_button.configure(text="Stop", command=stop_autoflaming)
            start_autoflaming()
        elif run_button.cget("text") == "Stop":
            run_button.configure(text="Start", command=autoflaming_toggle)
            stop_autoflaming()


    root = tk.Tk()
    root.title("Autoflaming")
    root.geometry("800x600")

    # select main stats
    main_stat_label = CustomLabel(root, "Select main stats:")
    main_stat_label.pack()
    main_stat = CustomRadioButtons(root,["STR","DEX","INT","LUK"])
    
    main_stat.pack()

     # select sub stats
    sub_stats_label = CustomLabel(root, "Select secondary stats:")
    sub_stats_label.pack()
    sub_stats = CustomCheckBoxes(root,["STR","DEX","INT","LUK"])
    
    sub_stats.pack()

    sub_stats_label = CustomLabel(root, "Select att/matt:")
    sub_stats_label.pack()
    att_matt = CustomRadioButtons(root,["Attack Power","Magic Attack"])
    
    att_matt.pack()

    entry_box_frame = ttk.Frame(root)
    entry_box_frame.pack(fill='x', padx=10, pady=5)

    # desired flame score
    desired_flame_label = CustomLabel(entry_box_frame, "Enter your desired flame score:")
    desired_flame_label.pack(side='left', padx=(0, 10))
    desired_flame_entry = tk.Entry(entry_box_frame)
    
    desired_flame_entry.pack(side='left', padx=(0, 10))

    #desired sub
    desired_sub_label = CustomLabel(entry_box_frame, "Enter your Secondary Stat coefficient:")
    desired_sub_label.pack(side='left', padx=(0, 10))
    desired_sub_entry = tk.Entry(entry_box_frame)
    desired_sub_entry.insert(0,0.1)
    desired_sub_entry.pack(side='left', padx=(0, 10))

    entry_box_frame1 = ttk.Frame(root)
    entry_box_frame1.pack(fill='x', padx=10, pady=6)
    #desired att
    desired_att_label = CustomLabel(entry_box_frame1, "Enter your att/matt coefficient:")
    desired_att_label.pack(side='left', padx=(0, 10))
    desired_att_entry = tk.Entry(entry_box_frame1)
    desired_att_entry.insert(0,3)
    desired_att_entry.pack(side='left', padx=(0, 10))

    #desired alls
    desired_alls_label = CustomLabel(entry_box_frame1, "Enter your all stats coefficient:")
    desired_alls_label.pack(side='left', padx=(0, 10))
    desired_alls_entry = tk.Entry(entry_box_frame1)
    desired_alls_entry.insert(0,10)
    desired_alls_entry.pack(side='left', padx=(0, 10))

    #button start
    run_button = ttk.Button(root,text="Start",command=autoflaming_toggle)
    
    run_button.pack(fill='x',  pady=7)

    root.mainloop()

if __name__ == "__main__":
    main()

