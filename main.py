# This is a sample Python script.
import queue
import random
import threading
import time

import pyautogui

from voice_command_loader import get_voice_command

text_to_command_queue_ = queue.Queue()
movement_direction = None
movements = {'up': [-1, 0], 'down': [1, 0], 'left': [0, -1], 'right': [0, 1],
             'up left': [-1, -1], 'up right': [-1, 1], 'down left': [1, -1], 'down right': [1, 1],
             'stop': [0, 0]}

screen_w, screen_h = pyautogui.size()
lock = threading.Lock()


def do_movement():
    global movement_direction
    while True:
        if movement_direction is not None:
            pyautogui.move(movement_direction[1], movement_direction[0])


def set_variable(text_to_command_queue):
    global movement_direction
    while True:
        if not text_to_command_queue.empty():
            try:
                movement_direction = movements[text_to_command_queue.get()]
            except KeyError:
                print('unknown command')
        # time.sleep(5)


if __name__ == '__main__':
    # Create the threads
    thread1 = threading.Thread(target=set_variable, args=[text_to_command_queue_])
    thread2 = threading.Thread(target=do_movement)
    thread3 = threading.Thread(target=get_voice_command, args=[text_to_command_queue_])

    # Start the threads
    thread1.start()
    thread2.start()
    thread3.start()

    # Wait for the threads to finish
    thread1.join()
    thread2.join()
    thread3.join()
