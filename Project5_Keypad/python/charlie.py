import RPi.GPIO as GPIO

class Charlie:
    '''Interface between the agent and the charlieplexed LED-board.'''

    pins = [1, 2, 3]
    led_dict = {"A": [1, 0, -1],
                "B": [0, 1, -1],
                "C": [-1, 1, 0],
                "D": [-1, 0, 1],
                "E": [1, -1, 0],
                "F": [0, -1, 1]}

    def setup(self):
        '''Sets up the proper mode'''
        GPIO.setmode(GPIO.BCM)

    def light_led(self, led_n):
        '''Turns on a single LED. Uses the dict to decide which pin is output
        and input, and which output is high and low.'''
