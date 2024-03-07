import time
import pyautogui
import re
from utils import WindowCapture, Cube_image_reco


class AutoCubing:
    def __init__(self, stop_event=None, condition_callable=None):
        self.found = False
        self.stop_event = stop_event
        self.condition_callable = condition_callable

    def check_condition(self):
        if self.condition_callable is not None:

            self.found = self.condition_callable()
            
    def main(self):
        while not self.stop_event.is_set():
            print("Loop running, stop_event is set:", self.stop_event.is_set())
            self.check_condition()
            if not self.found:
                pyautogui.click()
                time.sleep(0.050)
                pyautogui.press('enter')
                time.sleep(0.050)
                pyautogui.press('enter')
                time.sleep(0.050)
                pyautogui.press('enter')
                time.sleep(0.050)
            else:
                print("found")
                break

            time.sleep(2)  


class For_Stats:
    def __init__(self, OCR_stats: list[str], DESIRED_stats: list[dict[str, int]]):
        self.OCR_stats = OCR_stats
        self.DESIRED_stats = DESIRED_stats


    def parse_OCR_result(self) -> dict[str, int]:
        Stats_dict = {}
        str_pattern = r"([a-zA-Z\s]+?)\s*:?\s*\+?(\d+)%"               # match common stats end with %
        str_pattern_boss = r"([a-zA-Z\s]+): \+(\d+)"           #match boss damage
        str_pattern_cd = r"([a-zA-Z\s]+): \-(\d)"              #match skill cooldown

        print("OCR stats list", self.OCR_stats)

        for stat in self.OCR_stats:
            # Determine which pattern to use
            if "Boss" in stat:
                match = re.match(str_pattern_boss, stat)
            elif "Skill" in stat:
                match = re.match(str_pattern_cd, stat)
            else:
                match = re.match(str_pattern, stat)

            if match:
                stat_name = match.group(1).strip()  # Strip to remove any leading/trailing spaces
                stat_value = int(match.group(2))
                Stats_dict[stat_name] = Stats_dict.get(stat_name, 0) + stat_value

        print("Stats_dict", Stats_dict)
        return Stats_dict
 

    def check_stat(self, OCR_stats: dict[str, int]) -> bool:
        
        applicable_stats = {"STR", "INT", "DEX", "LUK","All Stats"}  # Stats that can benefit from 'All Stats'

        for desired_stats in self.DESIRED_stats:
            print("desired_stats", desired_stats)

            for stat_name, stat_threshold in desired_stats.items():
                total_stat = OCR_stats.get(stat_name, 0)

                # Add 'All Stats' value only if the stat is in the applicable list
                if 'All Stats' in OCR_stats and stat_name in applicable_stats:
                    total_stat += OCR_stats['All Stats']

                if total_stat < stat_threshold:
                    break  # If any desired stat is not met, break and check the next set
            else:
                return True  # Return True if all desired stats are met or exceeded

        return False  # Return False if none of the desired stats are met
    def main(self) -> bool:
        OCR_dict = self.parse_OCR_result()
        match_desired_stats = self.check_stat(OCR_dict)
        return match_desired_stats



def create_condition_callable(desired_stats: dict[str, int], cube_type: str):
    window_capture = WindowCapture("MapleStory")
    
    def condition():
        # Trigger screenshot
        if cube_type == 'Red':
            window_capture.locate_potential_RedCube()
        elif cube_type == 'Black':
            window_capture.locate_potential_BlackCube()
        
        OCR_result = Cube_image_reco.main()
        return For_Stats(OCR_result, desired_stats).main()
    
    return condition