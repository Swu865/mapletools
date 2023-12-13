import pyautogui
import pygetwindow as gw
import pytesseract
import cv2
import re
import ast

class WindowCapture:
    def __init__(self, window_title):
        self.window = self.locate_window(window_title)
    
    def locate_window(self, window_title):
        try:
            window = gw.getWindowsWithTitle(window_title)[0]
            return window
        except IndexError:
            print(f"Window titled '{window_title}' not found")
            exit()
    
    def take_screenshot(self, x_offset, y_offset, width, height, filename):
        x, y, w, h = self.window.left, self.window.top, self.window.width, self.window.height
        x1 = x + w // 2 - x_offset
        y1 = y + h // 2 + y_offset
        screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
        screenshot.save(filename)
    
    def locate_potential_RedCube(self):
        return self.take_screenshot(84, 57, 163, 43, 'screenshot.png')

    def locate_potential_BlackCube(self):
        return self.take_screenshot(84, 57+49, 163, 43, 'screenshot.png')


class Cube_image_reco:
    def __init__(self):
        pass
    def main():
        image =cv2.imread('screenshot.png')
        scale_factor = 4
        enlarged_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
        gray = cv2.cvtColor(enlarged_image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        text = text.replace(",", "").replace(".", "")
        OCR_result = text.split("\n")
        while "" in OCR_result:
            OCR_result.remove("")
        return OCR_result

class DataPreprocessing:
    def __init__(self, file_path):
        self.file_path = file_path
        self.stats_list = [] 
        self.item_name_list = []
        self.item_dict_list = []

    def parse(self):
        pattern = r"(\w+):(\{'.+?\})"
        with open(self.file_path, 'r') as file:
            for line in file:
                match = re.match(pattern, line.strip())
                if match:
                    category = match.group(1)
                    dict_str = match.group(2)                    
                    dict_obj = ast.literal_eval(dict_str)
                    self.stats_list.append([category, dict_obj])
        for i in range(len(self.stats_list)):
            self.item_name_list.append(self.stats_list[i][0])
            self.item_dict_list.append(self.stats_list[i][1])
    
    def get_item_name_list(self):
        self.parse()
        return self.item_name_list
    
    def get_item_dict_list(self):
        self.parse()
        return self.item_dict_list