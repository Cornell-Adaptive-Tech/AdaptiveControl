import tkinter as tk
from typing import Iterable

import bluetooth as BT


class GUI(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # My stubbornness for list comprehensions has led to messy code.
        # Woe is me
        device_options: list = [
            tk.Button(self, text=device.name, command=self.choose(device))
            for device in BT.get_serial_devices()
        ]
        device_options.insert(0, tk.Label(self, text=''))
        for i, option in enumerate(device_options):
            option.grid(row=i, column=0)

    # Somewhat janky way to get button callback to work
    def choose(self, device):
        def _choose():
            self.device = device
            # self.root.withdraw()
            BT.listen(device.name)
            # self.root.deiconify()

        return _choose

    def screen_size(self):
        return self.root.winfo_screenwidth(), self.root.winfo_screenheight()
