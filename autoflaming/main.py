import threading
import tkinter as tk
from tkinter import ttk
import sys
import os
import pygetwindow as gw
import json

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
        
        desired_stat_dict = {"main":main_stat.get_selected_option(),"sub":sub_stats.get_checked_items(),"attack":att_matt.get_selected_option(),"all":"All Stats","HP":"MaxHP","MP":"MaxMP"}
        condition = create_condition_callable(
            float(desired_flame_entry.get()),
            desired_stat_dict,
            float(desired_sub_entry.get()),
            float(desired_att_entry.get()),
            float(desired_alls_entry.get()),
            float(desired_HP_entry.get()),
            float(desired_MP_entry.get()),
            str(rdp_window.get()),
            stop_on_combat=combat_stop.get()
        )
        
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

    # find rdp windows list 
    def filter_windows():
        all_windows = gw.getAllTitles()
        filtered_windows = [title for title in all_windows if any(keyword in title for keyword in ["Remote Desktop Connection", "远程"])]
        return filtered_windows



    root = tk.Tk()
    root.title("Autoflaming")
    root.geometry("800x600")

    rdp_windows = filter_windows()
    rdp_window = SelectItem(root, "select RDP window",rdp_windows)
    rdp_window.pack(fill='x', padx=10, pady=5)

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
    desired_sub_label = CustomLabel(entry_box_frame, "Enter your Secondary Stat weight:")
    desired_sub_label.pack(side='left', padx=(0, 10))
    desired_sub_entry = tk.Entry(entry_box_frame)
    desired_sub_entry.insert(0,0.1)
    desired_sub_entry.pack(side='left', padx=(0, 10))

    entry_box_frame1 = ttk.Frame(root)
    entry_box_frame1.pack(fill='x', padx=10, pady=6)
    #desired att
    desired_att_label = CustomLabel(entry_box_frame1, "Enter your att/matt weight:")
    desired_att_label.pack(side='left', padx=(0, 10))
    desired_att_entry = tk.Entry(entry_box_frame1)
    desired_att_entry.insert(0,2.4)
    desired_att_entry.pack(side='left', padx=(0, 10))

    #desired alls
    desired_alls_label = CustomLabel(entry_box_frame1, "Enter your all stats weight:")
    desired_alls_label.pack(side='left', padx=(0, 10))
    desired_alls_entry = tk.Entry(entry_box_frame1)
    desired_alls_entry.insert(0,13)
    desired_alls_entry.pack(side='left', padx=(0, 10))

    #desired HP
    desired_HP_label = CustomLabel(entry_box_frame1, "Enter your HP weight:")
    desired_HP_label.pack(side='left', padx=(0, 10))
    desired_HP_entry = tk.Entry(entry_box_frame1)
    desired_HP_entry.insert(0,28000)
    desired_HP_entry.pack(side='left', padx=(0, 10))

    #desired MP
    desired_MP_label = CustomLabel(entry_box_frame1, "Enter your MP weight:")
    desired_MP_label.pack(side='left', padx=(2, 10))
    desired_MP_entry = tk.Entry(entry_box_frame1)
    desired_MP_entry.insert(0,28000)
    desired_MP_entry.pack(side='left', padx=(2, 10))       


    combat_stop = tk.BooleanVar(value=True)
    ttk.Checkbutton(
        root,
        text="Stop if Combat Power increases",
        variable=combat_stop
    ).pack(anchor="w", padx=10, pady=5)

    #button start
    run_button = ttk.Button(root,text="Start",command=autoflaming_toggle)
    
    run_button.pack(fill='x',  pady=7)

    f12_pressed = False

    def on_press(key):
        nonlocal f12_pressed
        if key == keyboard.Key.f12 and not f12_pressed:
            f12_pressed = True
            root.after(0, run_button.invoke)

    def on_release(key):
        nonlocal f12_pressed
        if key == keyboard.Key.f12:
            f12_pressed = False

    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    )
    listener.start()
    
    settings_path = os.path.join(script_dir, "settings.json")

    # 单选、复选框和窗口选择
    saved_vars = {
        "main": main_stat.radio_var,
        "attack": att_matt.radio_var,
        "combat_stop": combat_stop,
        "window": rdp_window.options.option_var,
    }
    saved_vars.update({
        f"sub_{name}": var
        for name, var in sub_stats.check_vars.items()
    })

    # 输入框绑定变量，方便保存和恢复
    entries = {
        "score": desired_flame_entry,
        "sub_weight": desired_sub_entry,
        "attack_weight": desired_att_entry,
        "all_weight": desired_alls_entry,
        "hp_weight": desired_HP_entry,
        "mp_weight": desired_MP_entry,
    }

    for name, entry in entries.items():
        var = tk.StringVar(master=root, value=entry.get())
        entry.configure(textvariable=var)
        saved_vars[name] = var

    # 启动时恢复
    try:
        with open(settings_path, "r", encoding="utf-8") as file:
            settings = json.load(file)
    except (OSError, ValueError):
        settings = {}

    if isinstance(settings, dict):
        for name, var in saved_vars.items():
            if name not in settings:
                continue

            # 上次选择的远程窗口不存在，就保留当前默认值
            if name == "window" and settings[name] not in rdp_windows:
                continue

            try:
                var.set(settings[name])
            except (tk.TclError, TypeError, ValueError):
                pass

    # 修改后自动保存
    def save_settings(*_):
        try:
            settings = {
                name: var.get()
                for name, var in saved_vars.items()
            }
            with open(settings_path, "w", encoding="utf-8") as file:
                json.dump(settings, file, ensure_ascii=False, indent=2)
        except (OSError, tk.TclError, ValueError) as error:
            print("保存设置失败:", error)

    for var in saved_vars.values():
        var.trace_add("write", save_settings)
    
    root.mainloop()
    listener.stop()

if __name__ == "__main__":
    main()

