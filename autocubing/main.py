import time
import pyautogui
from autocubing.utils import WindowCapture, Cube_image_reco
from autocubing.ItemCategory import For_Stats

class AutoCubing:
    def __init__(self, stop_event=None, condition_callable=None):
        self.found = False
        self.stop_event = stop_event
        self.condition_callable = condition_callable

    def check_condition(self):
        if self.condition_callable is not None:
            self.found = self.condition_callable()

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


def create_condition_callable(desired_stats,cube_type):
    if cube_type == 'red':
        WindowCapture("Windows Powershell").locate_potential_RedCube()
    else:
        WindowCapture("MapleStory").locate_potential_BlackCube()
    def condition():
        
        OCR_result = Cube_image_reco.main()   
        return For_Stats(OCR_result, desired_stats).main()
    return condition



