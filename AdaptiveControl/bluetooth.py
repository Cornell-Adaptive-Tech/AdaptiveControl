# *Actually supports any serial input.

from typing import List, Optional
from numbers import Number

from serial.tools.list_ports import comports
from serial import Serial
from enum import Enum
import pyautogui

# Configs
MOUSE_SENSITIVITY = 100
SCROLL_SENSITIVITY = 5
BAUDRATE = 9600
TIMEOUT = None
pyautogui.PAUSE = 0.01


def get_serial_devices() -> List:
    """
    Runs serial.tools.list_ports.comports.
    RETURNS
    --------
    list
        List of device objects.
    """
    return comports()


def def_val(v: Optional[Number], e: Number) -> Number:
    return v if v is not None else e


class Signal(Enum):
    """
    Enumeration that contains all the controls, as well as the actions to take.
    Each enum is defined as by a tuple: (value, action).
    """

    def __new__(cls, value, action):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.action = action
        return obj

    UP = 'U', lambda v: pyautogui.moveRel(0, -v)
    DOWN = 'D', lambda v: pyautogui.moveRel(0, v)
    LEFT = 'L', lambda v: pyautogui.moveRel(-v, 0)
    RIGHT = 'R', lambda v: pyautogui.moveRel(v, 0)
    L_CLICK = '1', lambda v: pyautogui.click(button='left')
    R_CLICK = '2', lambda v: pyautogui.click(button='right')
    SCROLL_UP = '^', lambda v: pyautogui.scroll(v)
    SCROLL_DOWN = 'V', lambda v: pyautogui.scroll(-v)
    RELINQUISH_CONTROL = 'E', lambda _: 'RELINQUISH_CONTROL'
    END_MSG = ';', lambda _: ';'


mouse_signals = [Signal.UP, Signal.DOWN, Signal.LEFT, Signal.RIGHT]
scroll_signals = [Signal.SCROLL_UP, Signal.SCROLL_DOWN]
parameterized_signals = [*mouse_signals, *scroll_signals]

# Inverse maps to allow easier mapping from signal enum to byte value.
# If you need that sort of thing
action_control_map = {signal.name: signal.value for signal in Signal}
control_action_map = {v: k for k, v in action_control_map.items()}


def listen(port, baudrate=BAUDRATE, timeout=TIMEOUT):
    """
    Listens on the port for Signal values. Acts upon them until
    """
    def process_line(line):
        print(f'Processing {line}')
        try:
            line = line[:-1]
            signal = Signal(line[0])
            data = line[1:]
            if signal in parameterized_signals:
                if data:
                    data = float(data)
                else:
                    return None
            return signal.action(data)
        except IndexError:
            return None
    with Serial(port, baudrate=baudrate, timeout=timeout) as device:
        buffer = ''
        while True:
            datum = device.read().decode()
            buffer += datum
            if datum == ';':
                result = process_line(buffer)
                buffer = ''
                if result == 'RELINQUISH_CONTROL':
                    break
