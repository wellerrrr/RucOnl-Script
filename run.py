import os
import cv2


script_dir = os.path.abspath(__file__)
print(script_dir)

img_dir = os.path.join(os.path.dirname(script_dir), "img")
take_img = cv2.imread(os.path.join(img_dir, "mino", "hand.jpg"))
reconnect_img = cv2.imread(os.path.join(img_dir, "disconnect", "reconnect.jpg"))


def get_take_img():
    return take_img

def get_reconnect_img():
    return reconnect_img

if __name__ == "__main__":
    needle_paths = ['img/mino/mhalfhead.jpg','img/mino/mhalfleft.jpg', 'img/mino/mhalfright.jpg', 'img/mino/mhalfback.jpg']
    
    from methods import MobHunter

    try:
        print('Script is turned on!')
        hunter = MobHunter(needle_paths)
        hunter.hunt()


    except KeyboardInterrupt:
        print('Script is turned off!')