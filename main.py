# This is a sample Python script.
import queue
import random
import sys
import threading
import time
import tkinter
from tkinter.messagebox import showinfo

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

type_text = None

click_count = None
click_button = None
screen_w, screen_h = pyautogui.size()
lock = threading.Lock()


def do_movement():
    global movement_direction
    while True:
        if movement_direction is not None:
            pyautogui.move(movement_direction[1], movement_direction[0])


def check_stop_typing():
    """
    :return:
    """
    root = tkinter.Tk()
    root.withdraw()
    showinfo(title='confirmation',
             message='Are you sure that you want to stop typing? Say Yes or No')
    return root
    # root.destroy()


def click():
    global click_count
    global click_button
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
                print(f'Moving cursor:\n{command}')
                movement_direction = movements[command]
            elif command in clicks:
                click_count = clicks[command][0]
                click_button = clicks[command][1]
                print(f'Click:\n{command}')
                click()
            elif command == 'type':
                print('Typing')
                while True:
                    if not text_to_command_queue.empty():
                        typed_text = text_to_command_queue.get()
                        if typed_text == 'stop typing':
                            break
                        pyautogui.typewrite(text_to_command_queue.get() + ' ')
            else:
                print(f'Unknown command: {command}')
        # time.sleep(5)


if __name__ == '__main__':
    # Create the threads
    thread_set_var = threading.Thread(target=set_variable, daemon=True, args=[text_to_command_queue_])
    thread_do_movement = threading.Thread(target=do_movement, daemon=True)
    # thread_click = threading.Thread(target=click, daemon=True)
    thread_get_voice_command = threading.Thread(target=get_voice_command, daemon=True, args=[text_to_command_queue_])

    # Start the threads
    thread_set_var.start()
    thread_do_movement.start()
    thread_get_voice_command.start()

    # Wait for the threads to finish
    thread_set_var.join()
    thread_do_movement.join()
    thread_get_voice_command.join()
