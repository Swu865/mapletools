import pyautogui
import pygetwindow as gw
import pytesseract
import cv2
import re
import ast

class WindowCapture:
    def __init__(self, window_title):

        self.window = self.locate_window(window_title)
        self.cursor_coor = ()
    def locate_window(self, window_title):
        try:
            window = gw.getWindowsWithTitle(window_title)[0]
            return window
        except IndexError:
            print(f"Window titled '{window_title}' not found")
            exit()


    def locate_potential_RedCube(self):
        x, y, w, h = self.window.left, self.window.top, self.window.width, self.window.height
        screenshot = pyautogui.screenshot(region=(x, y, w, h))
        screenshot.save("autocubing/assets/maplewindow.png") 
        
        game_screenshot = cv2.imread('autocubing/assets/maplewindow.png')
        template_tl = cv2.imread('autocubing/assets/red_tl.png', 0)  
        template_br = cv2.imread('autocubing/assets/cube_br.png', 0)  
        game_gray = cv2.cvtColor(game_screenshot, cv2.COLOR_BGR2GRAY)
        while True:
            #template match
            res_tl = cv2.matchTemplate(game_gray, template_tl, cv2.TM_CCOEFF_NORMED)
            res_br = cv2.matchTemplate(game_gray, template_br, cv2.TM_CCOEFF_NORMED)

            
            min_val_tl, max_val_tl, min_loc_tl, max_loc_tl = cv2.minMaxLoc(res_tl)
            min_val_br, max_val_br, min_loc_br, max_loc_br = cv2.minMaxLoc(res_br)
            top_left = max_loc_tl
            bottom_right = (max_loc_br[0] + template_br.shape[1], max_loc_br[1] + template_br.shape[0])

            
            top_left1 = (top_left[0],top_left[1]+36)
            bottom_right1 = (bottom_right[0],bottom_right[1]-20)

            #calculate one more try coordinate
            cursor_x = (top_left[0]+bottom_right[0])//2
            cursor_y = (bottom_right[1]+20)
            one_more_try_coor = (cursor_x+x,cursor_y+y)
            print(one_more_try_coor)
            #update 
            self.update_cursor_coor(one_more_try_coor)


            # take screenshot
            matched_region = game_screenshot[top_left1[1]:bottom_right1[1], top_left1[0]:bottom_right1[0]]
            if len(matched_region) !=0:
                break
        cv2.imwrite('autocubing/assets/screenshot.png', matched_region)

        

    def locate_potential_BlackCube(self):
        x, y, w, h = self.window.left, self.window.top, self.window.width, self.window.height
        screenshot = pyautogui.screenshot(region=(x, y, w, h))
        screenshot.save("autocubing/assets/maplewindow.png") 

        game_screenshot = cv2.imread('autocubing/assets/maplewindow.png')
        template_tl = cv2.imread(   'autocubing/assets/black_tl.png', 0)
        template_br = cv2.imread('autocubing/assets/cube_br.png', 0)
        game_gray = cv2.cvtColor(game_screenshot, cv2.COLOR_BGR2GRAY)

        #template match
        while True:
            res_tl = cv2.matchTemplate(game_gray, template_tl, cv2.TM_CCOEFF_NORMED)
            min_val_tl, max_val_tl, min_loc_tl, max_loc_tl = cv2.minMaxLoc(res_tl)
            top_left = max_loc_tl

            res_br = cv2.matchTemplate(game_gray[top_left[1]:, :], template_br, cv2.TM_CCOEFF_NORMED)
            min_val_br, max_val_br, min_loc_br, max_loc_br = cv2.minMaxLoc(res_br)
            bottom_right = (
                max_loc_br[0] + template_br.shape[1],
                max_loc_br[1] + template_br.shape[0] + top_left[1]
            )

            # add x,y offets to approach the stats rect
            top_left1 = (top_left[0], top_left[1]+36)
            bottom_right1 = (bottom_right[0], bottom_right[1] - 20)

            #calculate one more try coordinate
            cursor_x = (top_left[0]+bottom_right[0])//2
            cursor_y = (bottom_right[1]+20)
            one_more_try_coor = (cursor_x+x,cursor_y+y)
            #update 
            self.update_cursor_coor(one_more_try_coor)
            
            # take screenshot
            matched_region = game_screenshot[top_left1[1]:bottom_right1[1], top_left1[0]:bottom_right1[0]]
            if len(matched_region) != 0:
                break


        cv2.imwrite('autocubing/assets/screenshot.png', matched_region)
    
    def update_cursor_coor(self, new_value):

        self.cursor_coor = new_value


    def get_cursor_coor(self):

        return self.cursor_coor
        



class Cube_image_reco:
    def __init__(self):
        pass
    def main():
        image =cv2.imread('autocubing/assets/screenshot.png')
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


