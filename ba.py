import pygetwindow as gw
import time
import hashlib
from PIL import ImageGrab

def get_mumu_window_bbox(window_title):
    """查找MuMu模拟器窗口并获取其坐标"""
    try:
        window = gw.getWindowsWithTitle(window_title)[0]  # 假设窗口标题中包含'MuMu'

    except IndexError:
        print("未能找到模拟器窗口，请确保模拟器正在运行并且窗口标题正确。")
        return None



def get_screen_area_hash(bbox):
    """捕获屏幕指定区域的图像，并计算哈希值"""
    screen_image = ImageGrab.grab(bbox)
    hash_md5 = hashlib.md5(screen_image.tobytes())
    return hash_md5.hexdigest()

def monitor_screen_area(bbox, interval=1):
    """监控指定屏幕区域的变化"""
    print("开始监控指定屏幕区域的变化...")
    last_hash = None
    while True:
        current_hash = get_screen_area_hash(bbox)
        if last_hash is not None and current_hash != last_hash:
            print("警报：屏幕区域内容发生变化！")
            # 在这里添加任何警报动作，比如发出声音等
        last_hash = current_hash
        time.sleep(interval)

# 使用示例
# 将下面的字符串替换成你的MuMu模拟器窗口标题
mumu_window_title = "MuMu模拟器"
# 你需要根据红色方框在模拟器窗口中的相对位置进行调整
offset_left = 100  # 红色方框左边距离模拟器窗口左边界的距离
offset_top = 100   # 红色方框顶部距离模拟器窗口顶部界的距离
offset_right = 100 # 模拟器窗口右边界到红色方框右边的距离
offset_bottom = 100 # 模拟器窗口底部到红色方框底部的距离

bbox = get_mumu_window_bbox(mumu_window_title)
if bbox:
    monitor_screen_area(bbox, interval=1)