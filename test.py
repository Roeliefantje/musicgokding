import threading
from time import sleep
import time
from io import StringIO
import sys
from pyautogui import press, typewrite, hotkey


noInput = True

def startcounter():
    while noInput:
        if time.time() > timeout:
            typewrite('Carlson')
            press('enter')
            break

if __name__ == '__main__':
    timeout = time.time() + 5
    p = threading.Thread(target=startcounter)
    p.start()
    name = input("What is your name?")
    print(name)

