# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 11:05:24 2019
@author:
"""
from RPi import GPIO
from time import sleep


class Keypad:
    """Class for interfacing with adafruit 3x4 keypad"""

    keyLookup = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9'],
        ['*', '0', '#'],
    ]

    def __init__(self, rowPins, colPins, doSetup=False):
        self.rowPins = rowPins
        self.colPins = colPins
        if doSetup:
            self.setup()

    def setup(self):
        """
         Also, use GPIO functions to set the row pins as
         outputs and the column pins as inputs.
        """
        for pin in self.rowPins:
            GPIO.setup(pin, GPIO.OUT)
        for pin in self.colPins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def do_polling(self):
        """
        Determine the key currently
        being pressed on the keypad.
        """
        for r in self.rowPins:
            GPIO.output(r, 1)
            rowNum = self.rowPins.index(r)
            for c in self.colPins:
                colNum = self.colPins.index(c)
                isOn = True
                i = 0
                while isOn and i < 10:
                    isOn = (GPIO.input(c) == GPIO.HIGH)
                    i += 1
                    if not isOn:
                        break
                    sleep(0.01)
                if isOn:
                    return Keypad.keyLookup[rowNum][colNum]
            GPIO.output(r, 0)
            sleep(0.01)
        return None

    def get_next_signal(self):
        """
        This is the main interface between the agent and the
        keypad. It should initiate repeated calls to do polling
        until a key press is detected.
        """
        output = None
        while output == None:
            output = self.do_polling()
            sleep(0.1)
        return output


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    '''
    rowPins = [26, 19, 13, 6]
    colPins = [21, 20, 16]
    '''
    rowPins = [18, 23, 24, 25]
    colPins = [17, 27, 22]
    k = Keypad(rowPins, colPins, doSetup=True)
    k.setup()
    try:
        while True:
            print(k.get_next_signal())
            sleep(1)
    finally:
        GPIO.cleanup()
