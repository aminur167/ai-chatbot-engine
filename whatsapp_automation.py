import time

import pyautogui
import pyperclip

from chatbot_config import point


def copy_visible_chat(config):
    pyautogui.moveTo(*point(config, "chat_select_start"))
    pyautogui.dragTo(*point(config, "chat_select_end"), duration=2.0, button="left")
    pyautogui.hotkey("ctrl", "c")
    time.sleep(2)
    pyautogui.click(*point(config, "app_click"))
    return pyperclip.paste()


def focus_chat_window(config):
    pyautogui.click(*point(config, "app_click"))
    time.sleep(1)


def send_reply(config, reply):
    pyperclip.copy(reply)
    pyautogui.click(*point(config, "input_click"))
    time.sleep(1)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    pyautogui.press("enter")
