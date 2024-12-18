from time import time
import cv2
import os

from window import WindowCapture
from methods import MobHunter

script_dir = os.path.abspath(__file__)

img_dir = os.path.join(os.path.dirname(script_dir), "img")
take_img = cv2.imread(os.path.join(img_dir, "mino", "hand.jpg"))
reconnect_img = cv2.imread(os.path.join(img_dir, "disconnect", "reconnect.jpg"))


def get_take_img():
    return take_img

def get_reconnect_img():
    return reconnect_img

wincap = WindowCapture('NoxPlayer')
# WindowCapture.list_window_names()
# exit()

needle_paths = ['img/mino/mhalfhead.jpg','img/mino/mhalfleft.jpg', 'img/mino/mhalfright.jpg', 'img/mino/mhalfback.jpg',
                'img/mino/mhalfleft_low.jpg']
loop_time = time()

try:
    print('Script is turned on!')
    while(True):
        screenshot = wincap.get_screenshot()
        hunter = MobHunter(needle_paths)

        cv2.imshow('Computer vision', screenshot)
        
        hunter.hunt()



        print(f'FPS {1 / (time() - loop_time)}')
        loop_time = time()

        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break

except KeyboardInterrupt:
        print('Script is turned off!')
