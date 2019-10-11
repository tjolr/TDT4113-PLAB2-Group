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

    def turn_off_all(self):
        '''Turns all the LEDs off, mainly for debugging maybe.'''
        for pin in Charlie.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

def main():
    testpad = Charlie()
    testpad.setup()
    #testpad.light_led("A")
    #testpad.light_led("B")
    #testpad.light_led("C")
    #testpad.light_led("D")
    testpad.turn_off_all()


if __name__ == "__main__":
    main()