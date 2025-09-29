import cv2
import pyautogui
import pygetwindow as gw
import pytesseract
import re
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
            template_tl = cv2.imread('autoflaming/assets/test.png', 0)  



            game_gray = cv2.cvtColor(game_screenshot, cv2.COLOR_BGR2GRAY)
           
            #template match
            res_tl = cv2.matchTemplate(game_gray, template_tl, cv2.TM_CCOEFF_NORMED)


            # find frame position
            min_val_tl, max_val_tl, min_loc_tl, max_loc_tl = cv2.minMaxLoc(res_tl)

            top_left = max_loc_tl


            # add x,y offets to approach the stats rect
            top_left1 = (top_left[0]+79, top_left[1] + 295)       
            bottom_right = (top_left[0] + 216, top_left1[1] + 120)

            top_left_n = (bottom_right[0],top_left1[1])
            bottom_right_n = (bottom_right[0]+40,bottom_right[1])
            # take screenshot
            matched_text_region = game_screenshot[top_left1[1]:bottom_right[1], top_left1[0]:bottom_right[0]]
            matched_number_region = game_screenshot[top_left_n[1]:bottom_right_n[1], top_left_n[0]:bottom_right_n[0]]
            cv2.imwrite('autoflaming/assets/red_flame_text_region.png', matched_text_region)
            cv2.imwrite('autoflaming/assets/red_flame_number_region.png', matched_number_region)
            break

class Image_Reco:
    def __init__(self):
        pass

    def main(text_filename, number_filename):
        scale_factor = 2

        # 处理文本图
        image_t = cv2.imread(text_filename)
        enlarged_image_t = cv2.resize(image_t, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
        gray_t = cv2.cvtColor(enlarged_image_t, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('autoflaming/assets/red_flame_region_text.png', gray_t)
        text_t = pytesseract.image_to_string(gray_t)
        OCR_result_t = [line.strip() for line in text_t.split("\n") if line.strip()]

        # 处理数值图
        image_n = cv2.imread(number_filename)
        enlarged_image_n = cv2.resize(image_n, None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST)
        gray_n = cv2.cvtColor(enlarged_image_n, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray_n, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        cv2.imwrite('autoflaming/assets/red_flame_region_num.png', thresh)
        text_n = pytesseract.image_to_string(thresh)
        OCR_result_n = [line.strip() for line in text_n.split("\n") if line.strip()]

        print(OCR_result_t, "← text")
        print(OCR_result_n, "← number")

        # 合并
        merged = []
        min_len = min(len(OCR_result_t), len(OCR_result_n))
        for i in range(min_len):
            merged.append(OCR_result_t[i] + " " + OCR_result_n[i])

        return merged

class DataPreprocessing:
    def __init__(self):
        self.stats_dict = {"STR": 0, "DEX": 0, "INT": 0, "LUK": 0, "All Stats": 0,"Attack Power":0,"Magic Attack":0,"MaxHP":0,"MaxMP":0}

    def update_OCR_stats(self, item_list):
        print(item_list,"data prep")
        fuzzy_keys = {key: key.replace(" ", "") for key in self.stats_dict.keys()}
        

        for item in item_list:


            match = re.search(r"([a-zA-Z\s]+)\s*\+(\d+)%?", item)  
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
    OCR_list = Image_Reco.main('autoflaming/assets/red_flame_text_region.png','autoflaming/assets/red_flame_number_region.png')
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
                    # sub*0.1
                    filtered_stats[key] *= sub_coeffi
        else:
            if keys in filtered_stats:
                if category == 'main':
                    # main*1
                    filtered_stats[keys] *= 1
                elif category == 'attack':
                    # attack*3
                    filtered_stats[keys] *= att_coeffi
                elif category == 'all':
                    # all*10
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
                time.sleep(0.2)
                pyautogui.click()
                time.sleep(0.2)
                pyautogui.press('enter')
                time.sleep(0.20)
                pyautogui.press('enter')
                time.sleep(0.20)
                pyautogui.press('enter')
                time.sleep(0.20)
                pyautogui.press('enter')
                time.sleep(0.20)
            else:
                print("found",self.found )
                break

            time.sleep(4)  























