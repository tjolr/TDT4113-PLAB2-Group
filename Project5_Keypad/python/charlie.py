'''Module for implementing the led-interface. Using Charlieplexing.'''

import time
import RPi.GPIO as GPIO

class Charlie:
    '''Interface between the agent and the charlieplexed LED-board.'''

    pins = [16, 20, 21]
    led_dict = {"A": [1, 0, -1],
                "B": [1, -1, 0], #[0, 1, -1]
                "C": [-1, 1, 0],
                "D": [-1, 0, 1],
                "E": [0, -1, 1], #[1, -1, 0]
                "F": [0, 1, -1]} #[0, -1, 1]

    def setup(self):
        '''Sets up the proper mode'''
        GPIO.setmode(GPIO.BCM)

    def light_led(self, led_n):
        '''Turns on a single LED. Uses the dict to decide which pin is output
        and input, and which output is high and low.'''
        for pin_index, mode in enumerate(Charlie.led_dict[led_n]):
            if mode == 1:
                GPIO.setup(Charlie.pins[pin_index], GPIO.OUT)
                GPIO.output(Charlie.pins[pin_index], GPIO.HIGH)
            elif mode == 0:
                GPIO.setup(Charlie.pins[pin_index], GPIO.OUT)
                GPIO.output(Charlie.pins[pin_index], GPIO.LOW)
            elif mode == -1:
                GPIO.setup(Charlie.pins[pin_index], GPIO.IN)

    def light_leds(self, led_ns, duration):
        '''Turns on multiple LESs by using a loop.'''
        start_t = time.time()
        while time.time() - start_t < duration:
            for led in led_ns:
                self.light_led(led)

    def all_off(self):
        '''Turns all the LEDs off, mainly for debugging maybe.'''
        for pin in Charlie.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def light_all(self, duration):
        '''Turns on all LEDs for duration'''
        self.light_leds(["A", "B", "C", "D", "E", "F"], duration)

    def power_up(self):
        '''Sequence of lights when powering on.'''
        self.light_leds(["C", "D"], 0.25)
        self.light_leds(["B", "C", "D", "E"], 0.25)
        self.light_all(0.25)
        self.all_off()
        time.sleep(0.25)
        self.light_all(0.25)
        self.all_off()

    def deny(self):
        '''Blinking all LEDs when the password is wrong.'''
        self.light_all(0.25)
        self.all_off()
        time.sleep(0.25)
        self.light_all(0.25)
        self.all_off()
        time.sleep(0.25)
        self.light_all(0.25)
        self.all_off()
        time.sleep(0.25)
        self.light_all(0.25)
        self.all_off()

    def login(self):
        '''Sequence of lights when successful login'''
        self.light_leds(["A", "C", "D", "F"], 0.25)
        self.light_leds(["B", "E"], 0.25)
        self.light_leds(["A", "C", "D", "F"], 0.25)
        self.light_leds(["B", "E"], 0.25)

    def power_off(self):
        '''Sequence of lights when logging out'''
        self.light_all(0.5)
        self.light_leds(["B", "C", "D", "E"], 0.25)
        self.light_leds(["C", "D"], 0.25)
        self.all_off()

def main():
    '''Main function'''
    testpad = Charlie()
    testpad.setup()
    testpad.light_leds(["A", "B", "C"], 5)
    testpad.all_off()


if __name__ == "__main__":
    main()
