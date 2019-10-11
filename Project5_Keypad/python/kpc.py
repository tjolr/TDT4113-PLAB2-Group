# -*- coding: utf-8 -*-

import os
from time import sleep

CWD = os.getcwd()
DIRNAME = os.path.dirname(__file__)
DIRECTORY = os.path.realpath(os.path.join(CWD, DIRNAME))
NEXT_SIGNAL_PAUSE = 0.2

class KPC:
    """
    Variables:
        • a pointer to the keypad,
        • a pointer to the LED Board
        • a few simple strings or arrays for holding important sequences of
        keystrokes, such as a passcode-buffer for all numbers in an ongoing
        password-entry attempt.
        • the complete pathname to the file holding the KPC’s password.
        • the override-signal (discussed earlier in this document)
        • slots for holding the LED id (Lid) and lighting duration (Ldur) –
        both entered via the keypad – so that it can initiate the action of
        turning a specific LED on for a specific length of time.
    """

    def __init__(self, keypad, led_board, path):
        self.keypad = keypad
        self.led_board = led_board
        self.passcode_buffer = ""
        self.path_name = "".join([DIRECTORY, path])
        self.override_signal = None
        self.led_id = ""
        self.lightning_duration = ""

    def init_passcode_entry(self):
        """
        Clear the passcode-buffer and initiate a ”power up” lighting sequence
        on the LED Board. This should be done when the user first presses the
        keypad.
        """
        self.passcode_buffer = ""
        self.led_board.power_up()

    def get_next_signal(self):
        """
        Return the override-signal, if it is non-blank;
        otherwise query the keypad for the next pressed key.
        """
        if self.override_signal == None:
            self.override_signal = self.keypad.get_next_signal()
        override_buffer = self.override_signal
        self.override_signal = None
        sleep(NEXT_SIGNAL_PAUSE)
        return override_buffer

    def verify_login(self):
        """
        Check that the password just entered via the keypad matches that in the
        password file. Store the result (Y or N) in the override-signal. Also,
        this should call the LED Board to initiate the appropriate lighting
        pattern for login success or failure.
        """
        file_path = self.path_name
        passcode = None
        with open(file_path, 'r') as file:
            passcode = file.read()
        print("Passcode:", passcode)

        self.override_signal = "N"
        try:
            if int(self.passcode_buffer) == int(passcode):
                self.override_signal = "Y"
                self.led_board.login()

            else:
                self.led_board.deny()

        except ValueError:
            self.led_board.deny()

        self.passcode_buffer = ""

    def _is_legal_passcode(self):
        return len(self.passcode_buffer) >= 4 and self.passcode_buffer.isdigit()

    def validate_passcode_change(self):
        """
        Check that the new password is legal. If so, write the new password in
        the password file. A legal password should be at least 4 digits long
        and should contain no symbols other than the digits 0-9. As in verify
        login, this should use the LED Board to signal success or failure in
        changing the password.
        """
        if self._is_legal_passcode():
            self.led_board.confirm_valid()
            with open(self.path_name, 'w') as out_file:
                out_file.write(self.passcode_buffer)

        else:
            self.led_board.deny()

        self.passcode_buffer = ""


    def light_one_led(self):
        """
        Using values stored in the Lid and Ldur slots, call the LED Board and
        request that LED # Lid be turned on for Ldur seconds.
        """
        pass

    def flash_leds(self, duration):
        """
        Call the LED Board and request the flashing of all LEDs.
        """
        self.led_board.flash_all_leds(duration)

    def twinkle_leds(self, duration):
        """
        Call the LED Board and request the twinkling of all LEDs.
        """
        self.led_board.twinkle_all_leds(duration)

    def exit_action(self):
        """
        Call the LED Board to initiate the ”power down” lighting sequence.
        """
        self.led_board.power_down()