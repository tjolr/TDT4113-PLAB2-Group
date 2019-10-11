# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 11:00:03 2019

@author: Andreas Gravrok
"""
import os


from time import sleep


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

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

    def __init__(self, keypad, led_board, path_name):
        self.keypad = keypad
        self.led_board = led_board
        self.password_buffer = ""
        self.path_name = "".join([__location__, path_name])
        self.override_signal = None
        self.led_id = ""
        self.led_dur = ""

        self.password_buffer2 = ""

    def init_passcode_entry(self):
        """
        Clear the passcode-buffer and initiate a ”power up” lighting sequence
        on the LED Board. This should be done when the user first presses the
        keypad.
        """
        self.password_buffer = ""
        self.led_board.power_up()

    def get_next_signal(self):
        """
        Return the override-signal, if it is non-blank; otherwise query the
        keypad for the next pressed key.
        """
        if self.override_signal == None:
            self.override_signal = self.keypad.get_next_signal()
        override_buffer = self.override_signal
        self.override_signal = None
        sleep(0.2)
        return override_buffer

    def verify_login(self):
        """
        Check that the password just entered via the keypad matches that in the
        password file. Store the result (Y or N) in the override-signal. Also,
        this should call the LED Board to initiate the appropriate lighting
        pattern for login success or failure.
        """
        f = open(self.path_name, "r")
        password = f.read()
        f.close()
        print("The password is:", password)
        try:
            if int(self.password_buffer) == int(password):
                self.override_signal = "Y"
                self.led_board.login()


            else:
                self.override_signal = "N"
                self.led_board.deny()
        except ValueError:
            self.override_signal = "N"
            self.led_board.deny()

        self.password_buffer = ""


    def validate_passcode_change(self):
        """
        Check that the new password is legal. If so, write the new password in
        the password file. A legal password should be at least 4 digits long
        and should contain no symbols other than the digits 0-9. As in verify
        login, this should use the LED Board to signal success or failure in
        changing the password.
        """
        print(self.password_buffer)
        print(self.password_buffer2)
        if self.password_buffer == self.password_buffer2:

            if len(self.password_buffer) >= 4 and self.password_buffer.isdigit():
                self.led_board.confirm_valid()
                f = open(self.path_name, "w")
                f.write(self.password_buffer)
                f.close()
                print("SHALALALA")
            else:
                self.led_board.deny()

        self.password_buffer = ""
        self.password_buffer2 = ""

    def reenter_password(self):
        pass


    def password_buffer_add(self, signal):
        """add number to the password buffer"""
        self.password_buffer += signal

    def password_buffer_add2(self, signal):
        """add number to the password buffer"""
        self.password_buffer2 += signal

    def set_led_id(self, signal):
        """set the led id variable"""
        self.led_id = signal

    def add_led_dur(self, signal):
        """add a number to the led duration"""
        self.led_dur += signal

    def light_leds(self):
        """
        Using values stored in the Lid and Ldur slots, call the LED Board and
        request that LED # Lid be turned on for Ldur seconds.
        """
        if not self.led_dur:
            self.led_dur = "0"
        if self.led_id in "012345":
            self.led_board.timed_light(int(self.led_id), int(self.led_dur))
        elif self.led_id == "6":
            self.flash_leds(int(self.led_dur))
        elif self.led_id == "7":
            self.twinkle_leds(int(self.led_dur))

        self.led_id = ""
        self.led_dur = ""

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
