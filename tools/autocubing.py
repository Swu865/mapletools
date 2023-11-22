import cv2
import pytesseract
import time
import pygetwindow as gw
import pyautogui
import threading


# find the coordinate of the window of maplestory 
# screen shot the rectangle part we need


def locate_potentail_redcube_red():
    try:
        window = gw.getWindowsWithTitle('MapleStory')[0]
    except IndexError:
        print("MapleStory not found")
        exit()

    x,y,width,height =window.left,window.top,window.width,window.height
    x1 = x + width//2 - 84
    y1 = y + height//2 + 57
    rect_width = 168
    rect_height = 43
    screenshot = pyautogui.screenshot(region=(x1, y1,rect_width, rect_height))
    screenshot.save('screenshot.png')


#TODO, locate the black cube windows position
def locate_potentail_redcube_black():
    try:
        window = gw.getWindowsWithTitle('MapleStory')[0]
    except IndexError:
        print("MapleStory not found")
        exit()

    x,y,width,height =window.left,window.top,window.width,window.height
    x1 = x + width//2 - 84
    y1 = y + height//2 + 57
    rect_width = 168
    rect_height = 43
    screenshot = pyautogui.screenshot(region=(x1, y1,rect_width, rect_height))
    screenshot.save('screenshot.png')

def image_processing():
    image =cv2.imread('screenshot.png')
# Enlarge the image by a factor of 4 (for example)
    scale_factor = 4
    enlarged_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
    
# Convert the enlarged image to grayscale
    gray = cv2.cvtColor(enlarged_image, cv2.COLOR_BGR2GRAY)
    
# Perform OCR on the image
    text = pytesseract.image_to_string(gray)
    text = text.replace(",", "").replace(".", "")
# Print the OCR 
    OCR_result = text.split("\n")
    while "" in OCR_result:
        OCR_result.remove("")
    

    return OCR_result

def has_expected_potential_lines(OCR_result, potential, lines: int, True3: bool, above_160: bool):
    count = 0
    temp_sum = 0

    for potential_line in OCR_result:
        if potential in ["STR", "DEX", "INT", "LUK"] and (potential in potential_line or "All Stats" in potential_line):
            if True3:
                value = int(''.join(filter(str.isdigit, potential_line)))
                if above_160 and value in [13, 10, 7] or not above_160 and value in [12, 9, 6]:
                    temp_sum += value
            else:
                count += 1
        elif potential == "ATT" and potential in potential_line and not potential_line.startswith("Magic ATT:") and not potential_line.startswith("ATT: +32"):
            count += 1
        
        elif potential == "Magic ATT:" and potential in potential_line and not potential_line.startswith("Magic ATT: +32"):
            count += 1
        #for meso, drop rate etc...
        elif potential not in ["STR", "DEX", "INT", "LUK", "ATT", "Magic ATT:"] and potential in potential_line:
            count += 1

    if True3:
        return temp_sum >= (33 if above_160 else 30)
    else:
        return count >= lines




def main(cube_type: str,potential, lines: int, True3: bool,above_160: bool, stop_event=None):
    output_lines = ''
    line_count = 0
    found = False
    
    
    while True:
        if stop_event and stop_event.is_set():
            break
        
        time.sleep(1)
        if 'Red' in cube_type:
            locate_potentail_redcube_red()
        else:
            locate_potentail_redcube_black()
        OCR_result = image_processing()
        found = has_expected_potential_lines(OCR_result, potential,lines,True3,above_160)
    
        if not found:
            pyautogui.click()
            time.sleep(0.050)
            pyautogui.press('enter')
            time.sleep(0.050)
            pyautogui.press('enter')
            time.sleep(0.050)
            pyautogui.press('enter')
            time.sleep(0.050)
        else:   
            break
        
        time.sleep(3)
