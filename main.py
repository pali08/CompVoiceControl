# This is a sample Python script.
import random
import threading
import time

import pyautogui

movement_direction_vertical = 'down'
movement_direction_horizontal = 'left'
movements = {'up': -1, 'down': 1, 'left': -1, 'right': 1, 'stop':0}

screen_w, screen_h = pyautogui.size()
lock = threading.Lock()


def do_movement():
    global movement_direction_vertical
    global movement_direction_horizontal
    while True:
        pyautogui.move(movements[movement_direction_horizontal], movements[movement_direction_vertical])


def set_variable():
    global movement_direction_horizontal
    global movement_direction_vertical
    while True:
        movement_direction_vertical = random.choice(['up', 'down', 'stop'])
        movement_direction_horizontal = random.choice(['left', 'right', 'stop'])
        print(movement_direction_horizontal)
        print(movement_direction_vertical)
        time.sleep(5)


if __name__ == '__main__':
    # Create the threads
    thread1 = threading.Thread(target=set_variable)
    thread2 = threading.Thread(target=do_movement)

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for the threads to finish
    thread1.join()
    thread2.join()

