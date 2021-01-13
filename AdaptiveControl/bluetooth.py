# *Actually supports any serial input.

from serial.tools.list_ports import comports
from serial import Serial
from enum import Enum
import pyautogui

pyautogui.PAUSE = 0.01

def get_serial_devices():
    return comports()

# Configs
MOUSE_SENSITIVITY = 100
SCROLL_SENSITIVITY = 5
BAUDRATE = 9600
TIMEOUT = None

class Signal(Enum):
    '''
    Enumeration that contains all the controls, as well as the actions to take.
    Each enum is defined as by a tuple: (value, action).
    '''
    def __new__(cls, value, action):
        obj = object.__new__(cls)
        obj._value_=value
        obj.action = action
        return obj

    UP = rb'U', lambda: pyautogui.moveRel(0, -MOUSE_SENSITIVITY)
    DOWN = rb'D', lambda: pyautogui.moveRel(0, MOUSE_SENSITIVITY)
    LEFT = rb'L', lambda: pyautogui.moveRel(-MOUSE_SENSITIVITY, 0)
    RIGHT = rb'R', lambda: pyautogui.moveRel(MOUSE_SENSITIVITY, 0)
    L_CLICK = rb'1', lambda: pyautogui.click(button='left')
    R_CLICK = rb'2', lambda: pyautogui.click(button='right')
    SCOLL_UP = rb'^', lambda: pyautogui.scroll(SCROLL_SENSITIVITY)
    SCROLL_DOWN = rb'V', lambda: pyautogui.scroll(-SCROLL_SENSITIVITY)
    RELINQUISH_CONTROL = rb'E', lambda: 'RELINQUISH_CONTROL'

# Inverse maps to allow easier mapping from signal enum to byte value.
# If you need that sort of thing
action_control_map = {signal.name: signal.value for signal in Signal}
control_action_map = {v:k for k,v in action_control_map.items()}

def listen(port, baudrate=BAUDRATE, timeout=TIMEOUT, encoding='utf-8'):
    '''
    Listens on the port for Signal values. Acts upon them until
    '''
    with Serial(port, baudrate = baudrate, timeout=timeout) as device:
        while True:
            datum = device.read()
            try:
                print(f'Executing: {datum} of type {type(datum)}')
                sig = Signal(datum)
                print(f'Signal: {sig} Action: {sig.action}')
                result = sig.action()
                print('Action performed.')
            except ValueError as e:
                print(e)
                print(Signal.UP.value)
                result = None
                pass
            if result=='RELINQUISH_CONTROL':
                print('Relinquishing control.')
                break
