# This is a sample Python script.
import queue
import random
import sys
import threading
import time

import pyautogui

from voice_command_loader import get_voice_command

text_to_command_queue_ = queue.Queue()
movement_direction = None
movements = {'up': [-1, 0], 'down': [1, 0], 'left': [0, -1], 'right': [0, 1],
             'up left': [-1, -1], 'up right': [-1, 1], 'down left': [1, -1], 'down right': [1, 1],
             'stop': [0, 0]}
clicks = {'click': [1, 'left'], 'double click': [2, 'left'],
          'right click': [1, 'right'], 'right double click': [2, 'right'],
          'middle click': [1, 'middle']}
click_count = None
click_button = None
screen_w, screen_h = pyautogui.size()
lock = threading.Lock()


def do_movement():
    global movement_direction
    print('doin movement')
    while True:
        if movement_direction is not None:
            pyautogui.move(movement_direction[1], movement_direction[0])


def click():
    global click_count
    global click_button
    print(f'click count is {click_count}')
    print(f'click button is {click_button}')
    while True:
        time.sleep(1)
        if click_count is not None and click_button is not None:
            print('i am doing some clicking')
            pyautogui.click(clicks=click_count, button=click_button)
            click_count = None
            click_button = None


def set_variable(text_to_command_queue):
    global movement_direction
    global click_count
    global click_button
    while True:
        if not text_to_command_queue.empty():
            command = text_to_command_queue.get()
            if command in movements:
                movement_direction = movements[command]
            elif command in clicks:
                print(f'command in clicks is {command}')
                click_count = clicks[command][0]
                click_button = clicks[command][1]
                print(click_count)
                print(click_button)
            else:
                print(command)
        # time.sleep(5)


if __name__ == '__main__':
    # time.sleep(5)
    # pyautogui.click(clicks=1, button='left')
    # Create the threads
    thread_set_var = threading.Thread(target=set_variable, daemon=True, args=[text_to_command_queue_])
    thread_do_movement = threading.Thread(target=do_movement, daemon=True)
    thread_click = threading.Thread(target=click, daemon=True)
    thread_get_voice_command = threading.Thread(target=get_voice_command, daemon=True, args=[text_to_command_queue_])

    # Start the threads
    thread_set_var.start()
    thread_do_movement.start()
    thread_click.start()
    thread_get_voice_command.start()

    # Wait for the threads to finish
    thread_set_var.join()
    thread_do_movement.join()
    thread_click.join()
    thread_get_voice_command.join()
