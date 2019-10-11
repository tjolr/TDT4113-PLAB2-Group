# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 10:56:59 2019

@author:
"""
from RPi import GPIO
from time import sleep, time

class LED_board:
    """docstring"""

    '''
     1 = HIGH
     0 = LOW
    -1 = INPUT/HIGH IMPEDANCE
    '''
    pin_led_states = [
            [1, 0, -1], # A
            [1, -1, 0], # E til 2
            [-1, 1, 0], # D til 3
            [-1, 0, 1], # B til 4
            [0, -1, 1], # F til 5
            [0, 1, -1], # C til 6
            [0, 0, 0],  # Turns off all leds. Can be easilly called using pin_led_states[-1]
            ]

    def __init__(self, ledPins, doSetup=False):

        self.ledPins = ledPins 
        if doSetup:
            self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        

    def set_pin(self, pin_index, pin_state):
        pins = self.ledPins
        if pin_state == -1:
            GPIO.setup(pins[pin_index], GPIO.IN)
        else:
            GPIO.setup(pins[pin_index], GPIO.OUT)
            GPIO.output(pins[pin_index], pin_state)
    
    def light_led(self, led_number):
        for pin_index, pin_state in enumerate(LED_board.pin_led_states[led_number]):
            self.set_pin(pin_index, pin_state)


    def flash_all_leds(self, duration, blinkTime=0.25):
        """
        Flash all 6 LEDs on and off for k seconds, where k is an argument
        of the method.
        """
        startTime = time()
        while time()-startTime < duration:
            onTimeStart = time()
            while time()-onTimeStart < blinkTime:
                for led in range(6):
                    self.light_led(led)
            self.light_led(-1)
            sleep(blinkTime)

    def twinkle_all_leds(self, duration):
        """
        Turn all LEDs on and off in sequence for k seconds, where k is an
        argument of the method.
        """
        startTime = time()
        while time()-startTime < duration:
            for led in range(6):
                self.light_led(led)
                sleep(0.25)
        self.light_led(-1)

    def timed_light(self, led_id, led_dur):
        """turn on specified led for specified duration"""
        self.light_led(led_id)
        sleep(led_dur)
        self.light_led(-1)


    def power_up(self):
        for led in range(3):
            self.light_led(led)
            sleep(0.25)
        self.light_led(-1)

    def power_down(self):
        for led in range(5,2,-1):
            self.light_led(led)
            sleep(0.25)
        self.light_led(-1)

    def deny(self):
        for _ in range(3):
            onTimeStart = time()
            while time()-onTimeStart < 0.25:
                for led in range(3, 6):
                    self.light_led(led)
                    sleep(0.001)
            self.light_led(-1)
            sleep(0.25)

    def login(self):
        for _ in range(2):
            onTimeStart = time()
            while time()-onTimeStart < 0.1:
                for led in range(3):
                    self.light_led(led)
                    sleep(0.001)
            self.light_led(-1)
            sleep(0.1)

    def confirm_valid(self):
        self.login()
    
    
"""additional methods for lighting patterns associated with powering up (and
down) the system."""
