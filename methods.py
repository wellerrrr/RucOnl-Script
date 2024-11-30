import PIL.Image
import pyautogui
import cv2
import numpy
import time
import win32con
import win32api

from run import get_take_img, get_reconnect_img

class MobHunter:
    def __init__(self, needle_paths, click_delay=int(input('Enter seconds delay: ')), threshold=0.7):
        self.needle_paths = needle_paths
        self.click_delay = click_delay
        self.threshold = threshold
        self.last_click_time = 0

        self.screen_width, self.screen_height = pyautogui.size()
        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height // 2

    def find_closest_mob(self, haystack_img):
        found_any = False
        closest_mob_distance = float('inf')
        closest_mob_center_x = 0
        closest_mob_center_y = 0
        mob_count = 0

        for needle_path in self.needle_paths:
            needle_img = cv2.imread(needle_path, cv2.TM_CCOEFF_NORMED)

            needle_w = needle_img.shape[1]
            needle_h = needle_img.shape[0]

            result = cv2.matchTemplate(haystack_img, needle_img, cv2.TM_CCOEFF_NORMED)
            location = numpy.where(result >= self.threshold)
            location = list(zip(*location[::-1]))

            rectangles = []
            for loc in location:
                rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
                rectangles.append(rect)
            rectangles, weigths = cv2.groupRectangles(rectangles, 1, 0.5)

            if len(rectangles):
                found_any = True
                mob_count += len(rectangles)
                marker_color = (0, 0, 255)

                for (x, y, w, h) in rectangles:
                    center_x_mob = x + int(w/2)
                    center_y_mob = y + int(h/2)
                    cv2.rectangle(haystack_img, (x, y), (x + w, y + h), marker_color, 2)
                    distance = ((self.center_x - center_x_mob)**2 + (self.center_y - center_y_mob)**2)**0.5

                    if distance < closest_mob_distance:
                        closest_mob_distance = distance
                        closest_mob_center_x = center_x_mob
                        closest_mob_center_y = center_y_mob

        return found_any, closest_mob_center_x, closest_mob_center_y
    
    
    def take_item(self):

        screenshot = pyautogui.screenshot()
        haystack_img = cv2.cvtColor(numpy.array(screenshot), cv2.COLOR_RGB2BGR)
        take_btn = cv2.matchTemplate(haystack_img, take_img, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(take_btn)

        hand_w = take_img.shape[1]
        hand_h = take_img.shape[0]
        top_left = max_loc
        bottom_right = (top_left[0] + hand_w, top_left[1] + hand_h)
        cv2.rectangle(haystack_img, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_4)

        if max_val >= self.threshold:
            pyautogui.press('space')

            cv2.imwrite('result.jpg', haystack_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


    def hunt(self):
        check = CheckDisconect()

        while True:
            screenshot = pyautogui.screenshot()
            haystack_img = cv2.cvtColor(numpy.array(screenshot), cv2.COLOR_RGB2BGR)
            found_any, closest_mob_center_x, closest_mob_center_y = self.find_closest_mob(haystack_img)

            if check.find_reconnect_btn():
                print('Need to reconnect!')
                time.sleep(1)
                continue

            if self.take_item():
                print('btn founded')

            if found_any and time.time() - self.last_click_time >= self.click_delay:
                pyautogui.moveTo(closest_mob_center_x, closest_mob_center_y, duration=0.1)
                pyautogui.click(button='left')
                self.last_click_time = time.time()

            cv2.imwrite('result.jpg', haystack_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        

class CheckDisconect:
    def __init__(self, threshold=0.7):
        self.threshold = threshold
        self.reconnect = reconnect

    def find_reconnect_btn(self):
        screenshot = pyautogui.screenshot()
        disconnect = cv2.cvtColor(numpy.array(screenshot), cv2.COLOR_RGB2BGR)
        result = cv2.matchTemplate(disconnect, self.reconnect, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        btn_w = self.reconnect.shape[1]
        btn_h = self.reconnect.shape[0]
        top_left = max_loc
        bottom_right = (top_left[0] + btn_w, top_left[1] + btn_h - 50)
        cv2.rectangle(disconnect, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_4)

        if max_val >= self.threshold:
            win32api.SetCursorPos((bottom_right))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

            cv2.imwrite('result.jpg', disconnect)

            cv2.destroyAllWindows()
            return True
        return False

take_img = get_take_img()
reconnect = get_reconnect_img()