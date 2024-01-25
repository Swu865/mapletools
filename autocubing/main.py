import time
import pyautogui
from utils import WindowCapture, Cube_image_reco


class AutoCubing:
    def __init__(self, stop_event=None, condition_callable=None):
        self.found = False
        self.stop_event = stop_event
        self.condition_callable = condition_callable

    def check_condition(self):
        if self.condition_callable is not None:
            self.found = self.condition_callable()
    def stop(self):
        if self.stop_event is not None:
            self.stop_event.set()

    def main(self):
        while True:
            if self.stop_event and self.stop_event.is_set():
                break
            self.check_condition()
            if not self.found:
                pyautogui.click()
                time.sleep(0.050)
                pyautogui.press('enter')
                time.sleep(0.050)
                pyautogui.press('enter')
                time.sleep(0.050)
            else:
                break

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


def create_condition_callable(desired_stats,cube_type):
    if cube_type == 'red':
        print("red")
        WindowCapture("Windows Powershell").locate_potential_RedCube()
    elif cube_type == 'black':
        print("re2d")
        WindowCapture("MapleStory").locate_potential_BlackCube()
    def condition():
        
        OCR_result = Cube_image_reco.main() 
        print("re2d")
        return For_Stats(OCR_result, desired_stats).main()
    return condition


a = create_condition_callable("ATT","red")
b = AutoCubing(None,a)
b.main()