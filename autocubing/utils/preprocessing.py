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
        self.list_of_keys = []
    def parse(self):
        if not self.stats_list:  # Check if it's already been parsed
            pattern = r"(\w+):(\{'.+?\})"
            with open(self.file_path, 'r') as file:
                for line in file:
                    match = re.match(pattern, line.strip())
                    if match:
                        category = match.group(1)
                        dict_str = match.group(2)                    
                        dict_obj = ast.literal_eval(dict_str)
                        self.stats_list.append([category, dict_obj])

            # Only populate these lists if they're empty
            if not self.item_name_list and not self.item_dict_list:
                for category, stats in self.stats_list:
                    self.item_name_list.append(category)
                    self.item_dict_list.append(stats)

    def get_item_name_list(self):
        self.parse()
        return self.item_name_list
    
    def get_item_dict_list(self):
        self.parse()
        return self.item_dict_list

    def get_stats_for_category(self, category):
        
        for name, stats in self.stats_list:
            if name == category:
                return list(stats.keys())
    
    def set_item_dict_value(self, item_cate: str, key: str, value: int):
        self.parse()  # Make sure the data is parsed and lists are populated
        if item_cate in self.item_name_list:
            i = self.item_name_list.index(item_cate)
            self.item_dict_list[i][key] = value
            self.list_of_keys.append(key)
        else:
            print(item_cate)
            print(f"The item category '{item_cate}' is not a valid selection.")

    ## might be use in future
    def get_item_dict_value(self, item_cate: str, key: str, value: int):
          # Make sure the data is parsed and lists are populated
        self.parse()  # Make sure the data is parsed and lists are populated
        if item_cate in self.item_name_list:
            i = self.item_name_list.index(item_cate)
            return dict(self.item_dict_list[i] )
        else:
            print(item_cate)
            print(f"The item category '{item_cate}' is not a valid selection.")
    
    def display_desired_stat_value(self, item_cate: str, key: str, value: int):
        self.parse()  
        result = ""
        if item_cate in self.item_name_list:
            i = self.item_name_list.index(item_cate)
            stat_dict = dict(self.item_dict_list[i] )
            for key,value in stat_dict.items():
                if value != 0:
                    result += str(key)+": "+str(value)+" "
        return result


    def clear_dict_value(self,item_cate: str,key: str):
        if item_cate in self.item_name_list:
            i = self.item_name_list.index(item_cate)
            for j in self.list_of_keys:
                self.item_dict_list[i][j] = 0
        self.list_of_keys.clear()
        
    
    def clear_dict(self):
        self.item_dict_list.clear()
        self.stats_list.clear()
        self.item_name_list.clear()

        self.list_of_keys.clear()


