import time
import RPi.GPIO as GPIO

class Keypad:
    '''Class for interacting with the physical keypad'''

    rows = [18, 23, 24, 25]
    cols = [17, 27, 22]
    key_mapping = {(18, 17): "1", (18, 27): "2", (18, 22): "3",
                   (23, 17): "4", (23, 27): "5", (23, 22): "6",
                   (24, 17): "7", (24, 27): "8", (24, 22): "9",
                   (25, 17): "*", (25, 27): "0", (25, 22): "#"}

    def setup(self):
        '''Set the proper mode via: GPIO.setmode(GPIO.BCM). Also, use GPIO functions to
        set the row pins as outputs and the column pins as inputs.'''
        GPIO.setmode(GPIO.BCM)
        for rp in Keypad.rows:
            GPIO.setup(rp, GPIO.OUT)
        for cp in Keypad.cols:
            GPIO.setup(cp, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    
    def do_polling(self): 
        '''Use nested loops to determine the key currently being pressed on the keypad.
        Sets one row at a time to high, and checks whether a col on that row is high.
        uses that combination og row and col to check which button is pressed.'''
        pressed = False
        for rp in Keypad.rows:
            GPIO.output(rp, GPIO.HIGH)
            for cp in Keypad.cols:
                for _ in range(20): # checks whether it's not just noise by checking 20 times in a row
                    if GPIO.input(cp) == GPIO.HIGH:
                        pressed = True
                        time.sleep(0.001) # waits 10 milliseconds and tries again
                    else:
                        #if it's not high, we set pressed to false, and breaks out of the testing-loop
                        pressed = False
                        break
                if pressed:
                    return (Keypad.rows[rp], Keypad.cols[cp])
            GPIO.output(rp, GPIO.LOW) # set the row to low before we move to the next
        return False
    
    def get_next_signal(self):
        '''This is the main interface between the agent and the keypad. It should
        initiate repeated calls to do polling until a key press is detected.'''
        polled = self.do_polling()
        while not polled:
            polled = self.do_polling()
        return Keypad.key_mapping[polled]