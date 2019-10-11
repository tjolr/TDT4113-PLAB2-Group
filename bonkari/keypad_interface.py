# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 11:05:24 2019
@author:
"""
from time import sleep
from RPi import GPIO



class Keypad:
    """Class for interfacing with adafruit 3x4 keypad"""

    keyLookup = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9'],
        ['*', '0', '#'],
    ]

    def __init__(self, row_pins, col_pins, do_setup=False):
        self.row_pins = row_pins
        self.col_pins = col_pins
        if do_setup:
            self.setup()

    def setup(self):
        """
         Also, use GPIO functions to set the row pins as
         outputs and the column pins as inputs.
        """
        for pin in self.row_pins:
            GPIO.setup(pin, GPIO.OUT)
        for pin in self.col_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def do_polling(self):
        """
        Determine the key currently
        being pressed on the keypad.
        """
        for row in self.row_pins:
            GPIO.output(row, 1)
            row_num = self.row_pins.index(row)
            for col in self.col_pins:
                col_num = self.col_pins.index(col)
                is_on = True
                i = 0
                while is_on and i < 10:
                    is_on = (GPIO.input(col) == GPIO.HIGH)
                    i += 1
                    if not is_on:
                        break
                    sleep(0.01)
                if is_on:
                    return Keypad.keyLookup[row_num][col_num]
            GPIO.output(row, 0)
            sleep(0.01)
        return None

    def get_next_signal(self):
        """
        This is the main interface between the agent and the
        keypad. It should initiate repeated calls to do polling
        until a key press is detected.
        """
        output = None
        while output is None:
            output = self.do_polling()
            sleep(0.1)
        return output


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    ROW_PINS = [18, 23, 24, 25]
    COL_PINS = [17, 27, 22]
    k = Keypad(ROW_PINS, COL_PINS, do_setup=True)
    k.setup()
    try:
        while True:
            print(k.get_next_signal())
            sleep(1)
    finally:
        GPIO.cleanup()
