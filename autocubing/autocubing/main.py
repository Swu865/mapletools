import time
import pyautogui
import re
from utils import WindowCapture, Cube_image_reco
from rapidfuzz import process, fuzz


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
                time.sleep(0.1)
                pyautogui.press('enter')
                time.sleep(0.1)
                pyautogui.press('enter')
                time.sleep(0.1)
                pyautogui.press('enter')
                time.sleep(0.1)
                pyautogui.press('enter')
                time.sleep(0.1)
            else:
                print("found")
                break

            time.sleep(3)  

VALID_KEYS = ["Skill Cooldown: -2","Skill Cooldown: -1",'Magic ATT: +12%', 'Magic ATT: +9%', 'Magic ATT: +10%', 'Magic ATT: +13%', 'Attack Power: +9%', 'Attack Power: +10%', 'Attack Power: +12%', 'Attack Power: +13%', 'Boss Damage: +35%', 'Boss Damage: +30%', 'Boss Damage: +40%', 'Ignore Defense: +40%', 'Ignore Defense: +30%', 'Ignore Defense: +35%', 'STR: +9%', 'STR: +10%', 'STR: +12%', 'STR: +13%', 'DEX: +9%', 'DEX: +10%', 'DEX: +12%', 'DEX: +13%', 'INT: +9%', 'INT: +10%', 'INT: +12%', 'INT: +13%', 'LUK: +9%', 'LUK: +10%', 'LUK: +12%', 'LUK: +13%', 'All Stats: +9%', 'All Stats: +10%', 'All Stats: +6%', 'All Stats: +7%', 'Item Drop Rate: +20%', 'Mesos Obtained: +20%', 'Critical Damage: +8%']


def match_valid_key(input_str: str, threshold=80) -> str | None:
    # ignore the strings without %      
    if not (re.search(r'[+-]\d+%$', input_str) or "Skill Cooldown" in input_str):
        return "pass"

    match, score, _ = process.extractOne(input_str, VALID_KEYS, scorer=fuzz.ratio)
    return match if score >= threshold else "pass"

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
        str_pattern_cd = r"([a-zA-Z\s]+): \-(\d)"              #match skill cooldown

        print("OCR stats list", self.OCR_stats)

        for stat in self.OCR_stats:
            a = match_valid_key(stat)
            normalized_stat = self.normalize_text(a)
            print(normalized_stat)
            # Determine which pattern to use

            if "skill" in normalized_stat:
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
    window_capture = WindowCapture(window_name)
    
    def condition():
        # Trigger screenshot
        if cube_type == 'Red':
            window_capture.locate_potential_RedCube()
        elif cube_type == 'Black':
            window_capture.locate_potential_BlackCube()
        
        OCR_result = Cube_image_reco.main()
        return For_Stats(OCR_result, desired_stats).main()
    
    return condition