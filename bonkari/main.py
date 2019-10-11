"""
Created on Tue Oct  8 2019

Main file
"""

from RPi import GPIO

from fsm import Rule, FSM
from keypad_interface import Keypad
from keypad_controller import KPC
from led_board import LED_board

# Pins for Keypad
ROWPINS = [18, 23, 24, 25]
COLPINS = [17, 27, 22]

# Pins for charlieplexed keyboard
LEDPINS = [16, 20, 21]

def main():
    """
    Program main method
    """
    k = Keypad(ROWPINS, COLPINS)
    k.setup()
    agent0 = KPC(k, LED_board(LEDPINS), "/password.txt")
    agent0.exit_action()

    state_machine = FSM(agent0)
    # Frequently used conditions
    def hash_pressed(sig):
        """Return if hash # was pressed"""
        return sig == '#'

    def star_pressed(sig):
        """Return if star * was pressed"""
        return sig == '*'

    def num_pressed(sig):
        """Return if a number was pressed"""
        return sig in "0123456789"

    # Declare rules
    # States are:
    #   0: start
    #   1: password entry
    #   2: password validate
    #   3: logged in
    #   4: LED selected
    #   5: Change password
    rules = [
        # --------------------------------------------------------------
        # Using lambda expression to reject sig argument when not needed
        # --------------------------------------------------------------

        # Initiate password entry
        Rule(0, 1, lambda sig: True, lambda sig: agent0.init_passcode_entry()),
        # Cancel password entry
        Rule(1, 0, hash_pressed, lambda sig: agent0.exit_action()),
        # Input numbers
        Rule(1, 1, num_pressed, agent0.password_buffer_add),
        # Validate password
        Rule(1, 2, star_pressed, lambda sig: agent0.verify_login()),
        # Accepted
        Rule(2, 3, lambda sig: sig == 'Y', lambda sig: None),
        # Denied
        Rule(2, 0, lambda sig: sig == 'N', lambda sig: None),
        # Log out
        Rule(3, 0, hash_pressed, lambda sig: agent0.exit_action()),
        # Select LED
        Rule(3, 4, lambda sig: sig in "01234567", agent0.set_led_id),
        # Accept
        # Concatenate to duration
        Rule(4, 4, num_pressed, agent0.add_led_dur),
        # Cancel LED select
        Rule(4, 3, hash_pressed, lambda sig: agent0.exit_action()),
        # Accept and activate LED if duration is not empty string
        Rule(4, 3, star_pressed, lambda sig: agent0.light_leds()),
        # Initiate change password
        Rule(3, 5, star_pressed, lambda sig: agent0.init_passcode_entry()),
        # Input numbers
        Rule(5, 5, num_pressed, agent0.password_buffer_add),
        # Cancel password change
        Rule(5, 3, hash_pressed, lambda sig: agent0.exit_action()),
        # Validate new password
        #Rule(5, 3, star_pressed, lambda sig: agent0.validate_passcode_change()),

        Rule(5, 6, star_pressed, lambda sig: agent0.reenter_password()),

        Rule(6, 6, num_pressed, agent0.password_buffer_add2),

        Rule(6, 3, hash_pressed, lambda sig: agent0.exit_action()),

        Rule(6, 3, star_pressed, lambda sig: agent0.validate_passcode_change()),
    ]

    # Add the declared rules
    for rule in rules:
        state_machine.add_rule(rule)

    # Run main loop
    state_machine.main_loop()


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    try:
        main()
    finally:
        GPIO.cleanup()
