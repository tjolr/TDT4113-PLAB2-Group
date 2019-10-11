'''KPC agent'''
from finite_state_machine import signal_accept_all, signal_is_digit

class KPC:
    '''KPC agent class'''

    def __init__(self, keypad, led_board):
        '''Constructor'''
        self.keypad = keypad
        self.led_board = led_board
        self.cump = ""
        self.cp_pathname = ""
        self.passcode_buffer = "buffer"
        #First override signal from init will be all characters
        self.override_signal = signal_accept_all
        self.led_id = 0
        self.led_dur = 0

    def init_passcode_entry(self):
        '''clear passcode buffer and power-up'''
        self.passcode_buffer = ""
        self.led_board.led_power_up()

    def get_next_signal(self):
        '''returns override signal if non-blank,
        otherwise query the keypad for next pressed key'''
        if self.override_signal != "":
            return self.override_signal
        return self.keypad.get_next_signal()

    def verify_login(self):
        '''Check if password just typed matches save password in file
        Store result in override-signal
        call led board to light up succesful login'''
        if self.cump == self.read_password():
            self.override_signal = "Y"
            self.led_board.led_login_successful()
        else:
            self.override_signal = "N"
            self.led_board.led_login_unsuccessful()

    def validate_passcode_change(self, password):
        '''Check that the new password is legal.'''
        valid_password = True
        if len(password) < 4:
            valid_password = False
        else:
            for letter in password:
                if not signal_is_digit(letter):
                    valid_password = False
                    break





    def read_password(self):
        '''Reads current password from file'''

    def set_new_password(self, password):
        '''Overwrites old password in file with new password'''




