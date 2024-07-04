import sys
import os
# Calculate the relative path to the 'widgets.py'
script_dir = os.path.dirname(__file__)  # Get the directory where the script is running
relative_path = os.path.join(script_dir, '../autocubing/gui')
sys.path.append(relative_path)
from widgets import *
import cv2
import pynput
from pynput import keyboard 
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, Key
import pyautogui
import pygetwindow as gw
import time
import subprocess
import threading

running = False
class WindowCapture:
    def __init__(self, window_title):
        self.window = self.locate_window(window_title)
        self.game_pos = ()
        self.game_wh = ()
    def locate_window(self, window_title):
        windows = gw.getWindowsWithTitle(window_title)
        if windows:
            return windows[0]
        else:
            raise Exception(f"No window with title {window_title} found.")

    def game_screenshot(self):
        x, y, w, h = self.window.left, self.window.top, self.window.width, self.window.height
        self.game_pos = (x, y)
        self.game_wh = (w,h)
        screenshot = pyautogui.screenshot(region=(x, y, w, h))

        base_dir = os.path.dirname(__file__)  # Get the directory of the current script
        assets_dir = os.path.join(base_dir, 'assets')
        if not os.path.exists(assets_dir):
            os.makedirs(assets_dir)  # Create the directory if it does not exist
        file_path = os.path.join(assets_dir, 'maplewindow.png')
        screenshot.save(file_path)
        

    def get_template_coordinates(self, image_path, template_path):
        game_screenshot = cv2.imread(image_path)
        template = cv2.imread(template_path)
        res = cv2.matchTemplate(game_screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.8:  # threshold for matching
            return max_loc,(template.shape[1], template.shape[0])
        else:
            return None

    def get_ask_and_lb_coordinates(self):
        self.game_screenshot()  # Take screenshot and save it
        ask_coord = self.get_template_coordinates('autoasking/assets/maplewindow.png', 'autoasking/assets/ask.png')
        lb_coord = self.get_template_coordinates('autoasking/assets/maplewindow.png', 'autoasking/assets/lightbulb.png')
        return [ask_coord, lb_coord]
    
    def get_windows_coordinates(self):
        return self.game_pos
    
    def get_windows_width_height(self):
        return self.game_wh

    @staticmethod
    def get_ask_and_lb_middle_coordinates(coordinate,image_size):
        
        return ((coordinate[0]+(image_size[0]/2)),(coordinate[1]+(image_size[1]/2)))

class ActionController:
    def __init__(self):
        self.mouse = MouseController()  # Initialize mouse controller
        self.keyboard = KeyboardController()  # Initialize keyboard controller

    def move_and_click(self, position, repetition=1):
        self.mouse.position = position
        for _ in range(repetition):
            self.mouse.click(Button.left)  # Perform a left mouse click

    def press_key(self, key, repetition=1,wait=1):
        for _ in range(repetition):

            self.keyboard.press(key)
            self.keyboard.release(key)
            time.sleep(wait)

def shutdown():
    try:
        
        time_in_hours = int(shutdown_time.get())
    except ValueError:
        print("Please enter a valid number")
        return  

    shutdown_command = f"shutdown /s /t {time_in_hours * 3600}"  
    subprocess.run(shutdown_command.split(), shell=True)
    print(f"Shutdown scheduled in {time_in_hours} hour(s).")

def cancel_shutdown():
    shutdown_command = "shutdown -a"  
    subprocess.run(shutdown_command.split(), shell=True)

def run_autoasking():
    global running
    running = True
    capture = WindowCapture("MapleStory")
    coordinates = capture.get_ask_and_lb_coordinates()
    click_pos_list = []
    game_pos = capture.get_windows_coordinates()
    game_size =  capture.get_windows_width_height()

    for i in coordinates:
        a = capture.get_ask_and_lb_middle_coordinates(i[0],i[1])
        click_pos_list.append(a)
    
    ask_click_pos = click_pos_list[0][0]+game_pos[0],click_pos_list[0][1]+game_pos[1]
    lightbulb_click_pos = click_pos_list[1][0]+game_pos[0],click_pos_list[1][1]+game_pos[1]
    
    action = ActionController()
    while running:
        time.sleep(2)
        action.move_and_click(ask_click_pos, 2)
        time.sleep(1)
        action.press_key("y", 10)
        time.sleep(2)
        action.move_and_click(lightbulb_click_pos, 2)
        print("bulb", lightbulb_click_pos)
        time.sleep(2)
        action.press_key("y", 10)
        time.sleep(10)

def start_autoasking():
    global asking_thread
    asking_thread = threading.Thread(target=run_autoasking)
    asking_thread.start()

def stop_autoasking():
    global running
    running = False  

def main():
    root = tk.Tk()
    root.title("AutoAsking")
    root.geometry("800x600")
    # start button
    start_button = CustomButton(root, "Start Asking", command=start_autoasking)
    start_button.grid(row=0, column=0)
    # stop
    stop_button = CustomButton(root, "Stop Asking", command=stop_autoasking)
    stop_button.grid(row=1, column=0)

    #pc shutdown
    shutdown_lable = CustomLabel(root,"PC Shutdown in (hours):")
    shutdown_lable.grid(row=2, column=0, padx=10, pady=10)
    global shutdown_time
    shutdown_time = tk.Entry(root)
    shutdown_time.grid(row=2, column=1, padx=10, pady=10)
    shutdown_time.insert(0,3)
    pc_shutdown_button = CustomButton(root,"Shutdown PC ",shutdown)
    pc_shutdown_button.grid(row=2, column=2)

    #cancel shutdown
    cancel_shutdown_button = CustomButton(root,"Cancel shutdown ",cancel_shutdown)
    cancel_shutdown_button.grid(row=3, column=0)
    root.mainloop()

if __name__ == "__main__":
    main()




