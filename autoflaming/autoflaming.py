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
            template_tl = cv2.imread('autoflaming/assets/flame_after.png', 0)  



            game_gray = cv2.cvtColor(game_screenshot, cv2.COLOR_BGR2GRAY)
           
            #template match


            res_tl = cv2.matchTemplate(game_gray, template_tl, cv2.TM_CCOEFF_NORMED)
            # find frame position
            min_val_tl, max_val_tl, min_loc_tl, max_loc_tl = cv2.minMaxLoc(res_tl)

            top_left = max_loc_tl

            # add x,y offets to approach the stats rect
            top_left1 = (top_left[0]+15,top_left[1]+195)
            bottom_right = (top_left[0] + 208, top_left[1] + 324)
            
            # combat power region
            top_left2 = (top_left[0]+15,top_left[1]+334)
            bottom_right2 = (top_left[0] + 208, top_left[1] + 390)



            matched_region = game_screenshot[top_left1[1]:bottom_right[1], top_left1[0]:bottom_right[0]]

            combat_power_region = game_screenshot[top_left2[1]:bottom_right2[1], top_left2[0]:bottom_right2[0]]

            cv2.imwrite('autoflaming/assets/flame.png', matched_region)
            cv2.imwrite('autoflaming/assets/combat.png', combat_power_region)
            break

class Image_Reco:
    @staticmethod
    def main(text_filename):
        image = cv2.imread(text_filename)
        enlarged = cv2.resize(
            image, None, fx=3, fy=3,
            interpolation=cv2.INTER_CUBIC
        )
        gray = cv2.cvtColor(enlarged, cv2.COLOR_BGR2GRAY)
        ocr_image = cv2.bitwise_not(gray)

        text = pytesseract.image_to_string(
            ocr_image, config="--psm 6"
        )
        print("OCR 原始结果:", repr(text))

        OCR_result = [
            line.strip().upper()
            for line in text.replace(",", "").replace(".", "").splitlines()
            if line.strip()
        ]

        for index, line in enumerate(OCR_result):
            if not line.startswith("ALL STATS"):
                continue
            if re.fullmatch(r"ALL\s+STATS\s*\+\s*\d+\s*%", line):
                continue

            # 获取文字坐标，找到 All Stats 所在行
            data = pytesseract.image_to_data(
                ocr_image,
                config="--psm 6",
                output_type=pytesseract.Output.DICT
            )
            rows = {}
            for i, word in enumerate(data["text"]):
                if word.strip():
                    row_id = (
                        data["block_num"][i],
                        data["par_num"][i],
                        data["line_num"][i]
                    )
                    rows.setdefault(row_id, []).append(i)

            for ids in rows.values():
                words = [data["text"][i].upper() for i in ids]
                if "ALL" not in words or "STATS" not in words:
                    continue

                # 只取 STATS 右边的数值，排除属性文字
                value_ids = ids[words.index("STATS") + 1:]
                if not value_ids:
                    continue

                x1 = min(data["left"][i] for i in value_ids)
                y1 = min(data["top"][i] for i in value_ids)
                x2 = max(data["left"][i] + data["width"][i]
                         for i in value_ids)
                y2 = max(data["top"][i] + data["height"][i]
                         for i in value_ids)

                crop = ocr_image[
                    max(0, y1 - 3):y2 + 3,
                    max(0, x1 - 3):x2 + 3
                ]
                crop = cv2.copyMakeBorder(
                    crop, 15, 15, 15, 15,
                    cv2.BORDER_CONSTANT, value=255
                )

                retry = pytesseract.image_to_string(
                    crop,
                    config="--psm 7 -c tessedit_char_whitelist=0123456789+%"
                )
                retry = re.sub(r"\s+", "", retry)
                print("All Stats 单独识别:", repr(retry))

                match = re.fullmatch(r"\+?(\d+)%", retry)
                if match:
                    OCR_result[index] = f"ALL STATS +{match.group(1)}%"
                break

        print(OCR_result)
        return OCR_result
        
class CombatPowerCheck:
    @staticmethod
    def main(text_filename):
        image = cv2.imread(text_filename, 0)
        arrow = cv2.imread('autoflaming/assets/combat_arrow.png', 0)

        if image is None or arrow is None:
            print("战力截图或箭头模板读取失败")
            return False

        if image.shape[0] < arrow.shape[0] or image.shape[1] < arrow.shape[1]:
            return False

        result = cv2.matchTemplate(
            image, arrow, cv2.TM_CCOEFF_NORMED
        )
        score = cv2.minMaxLoc(result)[1]
        print("箭头匹配度:", round(score, 3))

        return score >= 0.85

class DataPreprocessing:
    def __init__(self):
        self.stats_dict = {"STR": 0, "DEX": 0, "INT": 0, "LUK": 0, "All Stats": 0,"Attack Power":0,"Magic Attack":0,"MaxHP":0,"MaxMP":0}

    def update_OCR_stats(self, item_list):

        fuzzy_keys = {key: key.replace(" ", "") for key in self.stats_dict.keys()}
        
        for item in item_list:


            match = re.search(r"([a-zA-Z\s]+)\s*\+\s*(\d+)%?", item)
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

def check_score(desired_score,desired_stats:dict,sub_coeffi:float,att_coeffi:float,all_coeffi:float,hp_coeffi:float,mp_coeffi:float,window_name:str,stop_on_combat=False):
    WindowCapture(window_name).game_screenshot()
    WindowCapture(window_name).red_flame_window()
    OCR_list = Image_Reco.main('autoflaming/assets/flame.png')
    combat_change = CombatPowerCheck.main('autoflaming/assets/combat.png')
    print("combat power increase?",combat_change)
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
    return rounded_total >= desired_score or (stop_on_combat and combat_change)    
def create_condition_callable(
    desired_score, desired_dict, sub, att, alls,
    hp, mp, window_name, stop_on_combat=False
):
    def condition():
        return check_score(
            desired_score, desired_dict, sub, att, alls,
            hp, mp, window_name, stop_on_combat=stop_on_combat
        )
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

            time.sleep(2.3)  

