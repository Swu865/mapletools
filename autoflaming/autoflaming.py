import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import pytesseract
import re
import ast
from Levenshtein import ratio
import time



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


    def game_screenshot(self):
        x, y, w, h = self.window.left, self.window.top, self.window.width, self.window.height
        screenshot = pyautogui.screenshot(region=(x, y, w, h))
        screenshot.save("autoflaming/assets/maplewindow.png") 
    
    def red_flame_window(self):
        while True:
            game_screenshot = cv2.imread('autoflaming/assets/maplewindow.png')
            template_tl = cv2.imread('autoflaming/assets/flame_tl.png', 0)  
            template_br = cv2.imread('autoflaming/assets/flame_br.png', 0)  
            game_gray = cv2.cvtColor(game_screenshot, cv2.COLOR_BGR2GRAY)
           
            #template match
            res_tl = cv2.matchTemplate(game_gray, template_tl, cv2.TM_CCOEFF_NORMED)
            res_br = cv2.matchTemplate(game_gray, template_br, cv2.TM_CCOEFF_NORMED)

            # find frame position
            min_val_tl, max_val_tl, min_loc_tl, max_loc_tl = cv2.minMaxLoc(res_tl)
            min_val_br, max_val_br, min_loc_br, max_loc_br = cv2.minMaxLoc(res_br)
            top_left = max_loc_tl
            bottom_right = (max_loc_br[0] + template_br.shape[1], max_loc_br[1] + template_br.shape[0])

            # add x,y offets to approach the stats rect
            top_left1 = (top_left[0],top_left[1]+20)
            bottom_right1 = (bottom_right[0],bottom_right[1]-20)

            # take screenshot
            matched_region = game_screenshot[top_left1[1]:bottom_right1[1], top_left1[0]:bottom_right1[0]]
            cv2.imwrite('autoflaming/assets/red_flame_region.png', matched_region)
            break

class Image_Reco:
    def __init__(self):
        pass
    def main(filename):
        image =cv2.imread(filename)
        scale_factor = 2
        enlarged_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

        gray = cv2.cvtColor(enlarged_image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('autoflaming/assets/red_flame_region.png', gray)
        text = pytesseract.image_to_string(gray)
        text = text.replace(",", "").replace(".", "")
        OCR_result = text.split("\n")
        while "" in OCR_result:
            OCR_result.remove("")
        return OCR_result

class DataPreprocessing:
    def __init__(self):
        self.stats_dict = {"STR": 0, "DEX": 0, "INT": 0, "LUK": 0, "All Stats": 0,"Attack Power":0,"Magic Attack":0,"MaxHP":0,"MaxMP":0}

    def update_OCR_stats(self, item_list):

        fuzzy_keys = {key: key.replace(" ", "") for key in self.stats_dict.keys()}
        

        for item in item_list:




            match = re.search(r"([a-zA-Z\s]+)\s*:? \+(\d+)%?", item)
            if not match:
                continue

            key = match.group(1).strip().replace(" ", "")
            value = int(match.group(2))
            

            best_match = None
            best_score = 0
            for dict_key, fuzzy_key in fuzzy_keys.items():
                score = ratio(fuzzy_key.lower(), key.lower())
                if score > best_score and score > 0.8:  
                    best_match = dict_key
                    best_score = score

 
            if best_match:
                self.stats_dict[best_match] += value
        
    def get_OCR_stats_dict(self):
        return self.stats_dict

def check_score(desired_score,desired_stats:dict,sub_coeffi:float,att_coeffi:float,all_coeffi:float,hp_coeffi:float,mp_coeffi:float,window_name:str):
    WindowCapture(window_name).game_screenshot()
    WindowCapture(window_name).red_flame_window()
    OCR_list = Image_Reco.main('autoflaming/assets/red_flame_region.png')
    data_process = DataPreprocessing()
    data_process.update_OCR_stats(OCR_list)
    OCR_dict = data_process.get_OCR_stats_dict()
    filtered_stats = {}
    desired_keys = []
    
    for key, value in desired_stats.items():
        if isinstance(value, list):
            desired_keys.extend(value)
        else:
            desired_keys.append(value)
    
    for key in desired_keys:
        if key in OCR_dict and isinstance(OCR_dict[key], (int, float)) and OCR_dict[key] != '':
            filtered_stats[key] = OCR_dict[key]
    
    for category, keys in desired_stats.items():
        if isinstance(keys, list):
            for key in keys:
                
                if key in filtered_stats:
                    # sub的值乘以0.1
                    filtered_stats[key] *= sub_coeffi
        else:
            if keys in filtered_stats:
                if category == 'main':
                    # main的值乘以1
                    filtered_stats[keys] *= 1
                elif category == 'attack':
                    # attack的值乘以3
                    filtered_stats[keys] *= att_coeffi
                elif category == 'all':
                    # all的值乘以10
                    filtered_stats[keys] *= all_coeffi
                
                elif category == 'HP':
                    filtered_stats[keys] *= (1/hp_coeffi)
                elif category == 'MP':
                    filtered_stats[keys] *= (1/mp_coeffi)                    

    
    total_value = sum(filtered_stats.values())
    rounded_total = round(total_value)
    print("----------------")
    print(desired_stats)
    print("ocr dict",OCR_dict)
    
    print("flame score",rounded_total)
    print("desired score",desired_score)
    return desired_score<rounded_total
    
def create_condition_callable(desired_score,desired_dict,sub,att,alls,hp,mp,window_name):

    def condition():
        return check_score(desired_score,desired_dict,sub,att,alls,hp,mp,window_name)
    return condition


class Autoflaming:
    def __init__(self, stop_event=None, condition_callable=None):
        self.found = False
        self.stop_event = stop_event
        self.condition_callable = condition_callable

    def check_condition(self):
        if self.condition_callable is not None:

            self.found = self.condition_callable()
            
    def main(self):
        while not self.stop_event.is_set():
            
            self.check_condition()
            if not self.found:
                pyautogui.click()
                time.sleep(0.10)
                pyautogui.press('enter')
                time.sleep(0.10)
                pyautogui.press('enter')
                time.sleep(0.10)
                pyautogui.press('enter')
                time.sleep(0.10)
            else:
                print("found",self.found )
                break

            time.sleep(3)  




# condition = create_condition_callable(115,{"main":"STR","sub":["DEX","LUK"],"attack":"Attack Power","all":"All Stats"},0.1,3,10)


# autoflaming = Autoflaming(condition)
# autoflaming.main()




















