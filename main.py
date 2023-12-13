import tkinter as tk
from tkinter import ttk  

from utils import DataPreprocessing
from gui.components import SelectCube




def main():
    root = tk.Tk()
    root.title("AutoCubing")
    root.geometry("800x600")


    select_cube = SelectCube(root)


    select_cube.pack(fill='x', padx=10, pady=5)


    def handle_button_click():
        selected_cube = select_cube.get_selected_cube()
        print(f"The selected cube is: {selected_cube}")

    test_button = ttk.Button(root, text="Test Selection", command=handle_button_click)
    test_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()