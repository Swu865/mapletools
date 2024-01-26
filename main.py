import threading
import tkinter as tk
from tkinter import ttk,scrolledtext
from autocubing.main import AutoCubing,create_condition_callable
from utils import DataPreprocessing
from gui.components import SelectCube,SelectItem 
from gui.widgets import CustomButton,CustomScrolledText,CustomLabel

def main():

    stop_event = threading.Event()
    test = []
    # Function to handle F12 press or stop button click
    def handle_stop():
        stop_event.set()  # Signal the event to stop the AutoCubing process
        print("Stopping...")  # Update this as needed, e.g., update a label in the GUI

    def run_autocubing():
        # Toggle running state
        
        


        condition = create_condition_callable(test, select_cube.get())
        autocubing_instance = AutoCubing(stop_event=stop_event, condition_callable=condition)  # Create an instance
        if not stop_event.is_set():
            # Start the AutoCubing process in a separate thread
            autocubing_thread = threading.Thread(target=autocubing_instance.main)  # Pass the instance's main method
            autocubing_thread.start()
            run_button.config(text="Stop", command=handle_stop)
        else:
            handle_stop()
            run_button.config(text="Run", command=run_autocubing)

    def update_stats_dropdown(*args):
        # Get the selected item category
        selected_category = item_cate.get()
        # Get the stats for the selected category
        stats = item_category_Data_process.get_stats_for_category(selected_category)
        # Update the stats dropdown
        desired_stats.update_options(stats)


    root = tk.Tk()
    root.title("AutoCubing")
    root.geometry("800x600")
    
    # Choose red or black cube
    select_cube = SelectCube(root)
    select_cube.pack(fill='x', padx=10, pady=5)
    
    # Data processing instance
    item_category_Data_process = DataPreprocessing("resources/item_category.txt")

    # Choose the item you want to cubing
    item_name_list = item_category_Data_process.get_item_name_list()
    item_cate = SelectItem(root, "select item", item_name_list)
    item_cate.pack(fill='x', padx=10, pady=5)
    
    # choose the desired stats 
    desired_stats = SelectItem(root, "select desire stats", [])
    desired_stats.pack(fill='x', padx=10, pady=5)

    #entry box
    extry_box_label = CustomLabel(root,"Enter your desired stats")
    extry_box_label.pack(fill='x', padx=10, pady=5)
    desired_number_entry = tk.Entry(root)
    desired_number_entry.pack(fill='x', padx=10, pady=5)

    def add_input_stats_value():
        selected_item = item_cate.get()
        selected_stat = desired_stats.get()
        number = desired_number_entry.get()
        
        if selected_item != "Select Option" and selected_stat != "Select Option" and number.isdigit():
            item_category_Data_process.set_item_dict_value(selected_item, selected_stat, int(number))
            display_str = item_category_Data_process.get_item_dict_value(selected_item, selected_stat, int(number))
            test.append(display_str)
            display_windows.clear_text()
            display_windows.insert_text(str(display_str))
        else:
            display_windows.clear_text()
            display_windows.insert_text("Please make a valid selection and enter a number.\n")

    
    add_button = CustomButton(root,"Add",add_input_stats_value)
    add_button.pack()
    
    # Set up the dropdown update trace
    item_cate.options.option_var.trace('w', update_stats_dropdown)

    #show your disired text
    display_windows = CustomScrolledText(root,height=10, width=50)
    display_windows.pack(fill='x', padx=10, pady=5)





    #run button
    
    run_button = CustomButton(root, "Run", run_autocubing)
    run_button.pack()

    # Bind the F12 key to the handle_stop function
    root.bind('<F12>', lambda event: handle_stop())

    root.mainloop()

if __name__ == "__main__":
    main()
