import RPi.GPIO as GPIO

class Keypad:
    """Class for interacting with the physical keypad"""

    def setup(self):
        """Set the proper mode via: GPIO.setmode(GPIO.BCM). Also, use GPIO functions to
        set the row pins as outputs and the column pins as inputs."""
    
    def do_polling(self): 
        """Use nested loops (discussed above) to determine the key currently being pressed 
        on the keypad."""
    
    def get_next_signal(self):
        """This is the main interface between the agent and the keypad. It should
        initiate repeated calls to do polling until a key press is detected."""
