import time
import pyautogui
import re
import random
from utils import WindowCapture, Cube_image_reco

mouse_cursor = ()

class AutoCubing:
    def __init__(self, stop_event=None, condition_callable=None):
        self.found = False
        self.stop_event = stop_event
        self.condition_callable = condition_callable

    def check_condition(self):
        if self.condition_callable is not None:

            self.found = self.condition_callable()
            
    def main(self):
        global mouse_cursor
        while not self.stop_event.is_set():
            print("Loop running, stop_event is set:", self.stop_event.is_set())
            self.check_condition()
            if not self.found:

                pyautogui.moveTo(mouse_cursor)
                pyautogui.click()
                time.sleep(0.10)
                pyautogui.press('enter')
                time.sleep(0.07)
                pyautogui.press('enter')
                time.sleep(0.10)
                pyautogui.press('enter')
                time.sleep(0.05)
                pyautogui.press('enter')
                time.sleep(0.10)
            else:
                print("found")
                break

            time.sleep(random.randint(3, 4))  


class For_Stats:
    def __init__(self, OCR_stats: list[str], DESIRED_stats: list[dict[str, int]]):
        self.OCR_stats = OCR_stats
        self.DESIRED_stats = DESIRED_stats

    def normalize_text(self, text: str) -> str:
        """ Normalize text to lower case and strip extra spaces. """
        return text.strip().lower()

    def parse_OCR_result(self) -> dict[str, int]:
        Stats_dict = {}
        str_pattern = r"([a-zA-Z\s]+?)\s*:?\s*\+?(\d+)%"               # match common stats end with %
        str_pattern_boss = r"([a-zA-Z\s]+): \+(\d+)"           #match boss damage
        str_pattern_cd = r"([a-zA-Z\s]+): \-(\d)"              #match skill cooldown

        print("OCR stats list", self.OCR_stats)

        for stat in self.OCR_stats:
            normalized_stat = self.normalize_text(stat)

            # Determine which pattern to use
            if "boss" in normalized_stat:
                match = re.match(str_pattern_boss, normalized_stat)
            elif "skill" in normalized_stat:
                match = re.match(str_pattern_cd, normalized_stat)
            else:
                match = re.match(str_pattern, normalized_stat)

            if match:
                stat_name = self.normalize_text(match.group(1))
                stat_value = int(match.group(2))
                Stats_dict[stat_name] = Stats_dict.get(stat_name, 0) + stat_value

        print("Stats_dict", Stats_dict)
        return Stats_dict

    def check_stat(self, OCR_stats: dict[str, int]) -> bool:
        
        applicable_stats = {"str", "int", "dex", "luk"}  # Stats that can benefit from 'All Stats'

        for desired_stats in self.DESIRED_stats:
            print("desired_stats", desired_stats)

            for stat_name, stat_threshold in desired_stats.items():
                normalized_stat_name = self.normalize_text(stat_name)
                total_stat = OCR_stats.get(normalized_stat_name, 0)

                # Add 'All Stats' value only if the stat is in the applicable list
                if 'all stats' in OCR_stats and normalized_stat_name in applicable_stats:
                    total_stat += OCR_stats['all stats']

                if total_stat < stat_threshold:
                    break  # If any desired stat is not met, break and check the next set
            else:
                return True  # Return True if all desired stats are met or exceeded

        return False  # Return False if none of the desired stats are met

    def main(self) -> bool:
        OCR_dict = self.parse_OCR_result()
        match_desired_stats = self.check_stat(OCR_dict)
        return match_desired_stats



def create_condition_callable(desired_stats: dict[str, int], cube_type: str,window_name:str):
    global mouse_cursor
    window_capture = WindowCapture(window_name)
    
    def condition():
        global mouse_cursor
        # Trigger screenshot
        if cube_type == 'Red':
            window_capture.locate_potential_RedCube()
            mouse_cursor = window_capture.get_cursor_coor()

        elif cube_type == 'Black':
            window_capture.locate_potential_BlackCube()
            mouse_cursor = window_capture.get_cursor_coor()
 
        OCR_result = Cube_image_reco.main()
        return For_Stats(OCR_result, desired_stats).main()
    
    return condition