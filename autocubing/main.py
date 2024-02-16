import threading
import tkinter as tk
from tkinter import ttk, scrolledtext,messagebox
from pynput import keyboard 
from autocubing.main import AutoCubing,create_condition_callable
from utils import DataPreprocessing
from gui.components import SelectCube,SelectItem 
from gui.widgets import CustomButton,CustomScrolledText,CustomLabel



def main():
    global stop_event, autocubing_thread  # Declare that we will use global variables in this function
    desired_stats_list = []
    
    def start_autocubing():
        global stop_event, autocubing_thread
        condition = create_condition_callable(desired_stats_list, select_cube.get())

        stop_event = threading.Event()
        stop_event.clear()
        autocubing_instance = AutoCubing(stop_event, condition)
        autocubing_thread = threading.Thread(target=autocubing_instance.main)  # Removed the parentheses here
        autocubing_thread.start()

    def stop_autocubing():
        global stop_event, autocubing_thread
        if stop_event:
            stop_event.set()
        autocubing_thread.join()

        run_button.configure(text="Start", command=autocubing_toggle)

    def autocubing_toggle():
        if not desired_stats_list:
            messagebox.showwarning("Warning", "Please add at least one stat value before starting.")
        
        elif run_button.cget("text") == "Start" :

            run_button.configure(text="Stop", command=stop_autocubing)
            start_autocubing()
        elif run_button.cget("text") == "Stop":
            run_button.configure(text="Start", command=autocubing_toggle)
            stop_autocubing()
            
    # Keyboard listener setup

    def on_press(key):
        if key == keyboard.Key.f12:
            autocubing_toggle()
            
    def update_stats_dropdown(*args):
        # Get the selected item category
        selected_category = item_cate.get()
        # Get the stats for the selected category
        stats = item_category_Data_process.get_stats_for_category(selected_category)
        # Update the stats dropdown
        desired_stats.update_options(stats)

    
    def clear_stats():
        desired_stats_list.clear()
        item_category_Data_process.clear_dict()
        set_display_windows.clear_text()
        display_windows.clear_text()

    def set_input_stats_value():
        selected_item = item_cate.get()
        selected_stat = desired_stats.get()
        number = desired_number_entry.get()
        
        if selected_item != "Select Option" and selected_stat != "Select Option" and number.isdigit():
            item_category_Data_process.set_item_dict_value(selected_item, selected_stat, int(number))
            display_str = item_category_Data_process.get_item_dict_value(selected_item, selected_stat, int(number))

            set_display_windows.clear_text()
            set_display_windows.insert_text("Your desired stats is: "+"\n"+str(display_str))
        else:
            set_display_windows.clear_text()
            set_display_windows.insert_text("Please make a valid selection and enter a number.\n")
    def add_input_stats_value():
        selected_item = item_cate.get()
        selected_stat = desired_stats.get()
        number = desired_number_entry.get()
        
        if selected_item != "Select Option" and selected_stat != "Select Option" and number.isdigit():
            
            display_str = item_category_Data_process.get_item_dict_value(selected_item, selected_stat, int(number))
            desired_stats_list.append(display_str)
            item_category_Data_process.clear_dict_value(selected_item,selected_stat)
            set_display_windows.clear_text()
            display_windows.insert_text(str(display_str)+"\n")

            
            
        else:
            display_windows.clear_text()
            display_windows.insert_text("Please make a valid selection and enter a number.\n")



    root = tk.Tk()
    root.title("AutoCubing")
    root.geometry("800x600")
    
    # Choose red or black cube
    select_cube = SelectCube(root)
    select_cube.pack(fill='x', padx=10, pady=5)
    
    # Data processing instance
    item_category_Data_process = DataPreprocessing("Autocubing/resources/item_category.txt")

    # Choose the item you want to cubing
    item_name_list = item_category_Data_process.get_item_name_list()
    item_cate = SelectItem(root, "select item", item_name_list)
    item_cate.pack(fill='x', padx=10, pady=5)
    
    # choose the desired stats 
    desired_stats = SelectItem(root, "select desire stats", [])
    desired_stats.pack(fill='x', padx=10, pady=5)

    entry_box_frame = ttk.Frame(root)
    entry_box_frame.pack(fill='x', padx=10, pady=5)

    # Label
    extry_box_label = CustomLabel(entry_box_frame, "Enter your stats value:")
    extry_box_label.pack(side='left', padx=(0, 10))

    # Entry Box
    desired_number_entry = tk.Entry(entry_box_frame)
    desired_number_entry.pack(side='left', padx=(0, 10))


    # Set up the dropdown update trace
    item_cate.options.option_var.trace('w', update_stats_dropdown)

    display_window_frame = ttk.Frame(root)
    display_window_frame.pack(fill='x', padx=10, pady=5)
    #show your disired text
    set_display_windows = CustomScrolledText(display_window_frame,height=10, width=50)
    set_display_windows.pack(side='left', padx=(0, 10))

    display_windows = CustomScrolledText(display_window_frame,height=10, width=50)
    display_windows.pack(side='right', padx=(0, 10))

    # set button
    display_window_button_frame = ttk.Frame(root)
    display_window_button_frame.pack(fill='x', padx=10, pady=5)
    set_button = CustomButton(display_window_button_frame,"Set",set_input_stats_value)
    set_button.pack(side='left', padx=(0, 10))

    # add button
    add_button = CustomButton(display_window_button_frame,"Add",add_input_stats_value)
    add_button.pack(side='right', padx=(0, 10))
    #run button
    run_button = ttk.Button(root, text="Start", command=autocubing_toggle)
    run_button.pack(side='right', padx=(0, 10))

    #clear button
    clear_button = ttk.Button(root, text="Clear", command=clear_stats)
    clear_button.pack(side='left', padx=(0, 10))

    # keyboard listener,bind f12 to run button
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    root.mainloop()

if __name__ == "__main__":
    main()


