import pyautogui
import pygetwindow as gw
import pytesseract
import cv2
import re

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

class For_Stats():
    def __init__(self, OCR_stats: list[str], DESIRED_stats: list[dict[str, int]]):
        self.OCR_stats = OCR_stats
        self.DESIRED_stats = DESIRED_stats  # Now a list of dictionaries

    def parse_OCR_result(self) -> dict[str, int]:
        Stats_dict = {}
        str_pattern = r"([a-zA-Z\s]+): \+(\d+)%"
        for stat in self.OCR_stats:
            match = re.match(str_pattern, stat)
            if match:
                stat_name = match.group(1).strip()  # Strip to remove any leading/trailing spaces
                stat_value = int(match.group(2))
                Stats_dict[stat_name] = Stats_dict.get(stat_name, 0) + stat_value

        return Stats_dict

    def check_stat(self, OCR_stats: dict[str, int]) -> bool:
        for desired_stats in self.DESIRED_stats:  # Iterate through each DESIRED_stats dict
            if all(OCR_stats.get(stat_name, 0) >= stat_threshold for stat_name, stat_threshold in desired_stats.items()):
                return True  # Return True if any DESIRED_stats is fully met
        return False  # Return False if none of the DESIRED_stats are met

    def main(self) -> bool:
        OCR_dict = self.parse_OCR_result()
        match_desired_stats = self.check_stat(OCR_dict)
        return match_desired_stats