'''KPC agent'''
from finite_state_machine import signal_accept_all, signal_is_digit
import time
from inspect import isfunction

class KPC:
    '''KPC agent class'''

    def __init__(self, keypad, led_board):
        '''Constructor'''
        self.keypad = keypad
        self.led_board = led_board
        self.password_buffer = ""
        self.password_buffer_2 = ""
        self.cp_pathname = "password.txt"
        #First override signal from init will be all characters
        self.override_signal = None
        self.led_id = ""
        self.led_dur = ""
        #local testing
        self.signals = [
            "8",
            "1",
            "2",
            "3",
            "4",
            "*",
            "*",
            "5",
            "1",
            "7",
            "7",
            "*",
            "5",
            "1",
            "7",
            "7",
            "*",
            "2",
            "3",
            "*"
        ]



    def init_passcode_entry(self, *sig):
        '''clear passcode buffer and power-up'''
        self.password_buffer = ""
        self.led_board.power_up()

    def get_next_signal(self):
        '''returns override signal if non-blank,
        otherwise query the keypad for next pressed key'''
        if self.override_signal == None:
            self.override_signal = self.keypad.get_next_signal()

            #Use this line when testing locally
            #self.override_signal = self.get_next_signal2()
        override_buffer = self.override_signal
        self.override_signal = None
        time.sleep(0.25)
        return override_buffer


    def get_next_signal2(self):
        '''Get next signal'''
        if self.signals:
            return self.signals.pop(0)
        return "#"

    def pass_func(self, *sig):
        '''Passing function'''
        pass

    def verify_login(self, *sig):
        '''Check if password just typed matches save password in file
        Store result in override-signal
        call led board to light up succesful login'''
        try:
            print(f'Password buffer {self.password_buffer}')
            if self.password_buffer == self.read_password():
                print('Password verify login correct!!!')
                self.override_signal = "Y"
                self.led_board.login()
            else:
                self.override_signal = "N"
                self.led_board.deny()
        except ValueError:
            self.override_signal = "N"
            self.led_board.deny()

        self.password_buffer = ""

    def validate_passcode_change(self, *sig):
        '''Check that the new password is legal.'''
        print(f'Password buffer 1: {self.password_buffer}')
        print(f'Password buffer 2: {self.password_buffer_2}')

        if self.password_buffer == self.password_buffer_2:
            if self.password_buffer.isdigit() and len(self.password_buffer) >= 4:
                self.write_new_password(self.password_buffer)
                self.led_board.login()
            else:
                self.led_board.deny()

        self.password_buffer, self.password_buffer_2 = "", ""

    def read_password(self):
        '''Reads current password from file'''
        with open(self.cp_pathname, 'r') as file:
            password = file.readline().strip()

        print("Password",password)
        return password

    def write_new_password(self, password):
        '''Overwrites old password in file with new password'''
        with open(self.cp_pathname, "w") as file:
            file.write(password)

    def password_buffer_add(self, signal):
        '''Add number to password buffer 1'''
        self.password_buffer += signal

    def password_buffer_add2(self, signal):
        '''Add number to password buffer 2'''
        self.password_buffer_2 += signal

    def set_led_id(self, signal):
        '''Set the led id variable'''
        self.led_id = signal

    def set_led_dur(self, signal):
        '''Set led lighting duration'''
        self.led_dur= signal

    def light_leds(self, *sig):
        '''Will light up the set led id for led_dur seconds'''
        led_names = ["A", "B", "C", "D", "E", "F"]

        if self.led_dur != "" and self.led_id in "012345":
            self.led_board.light_leds(list(led_names[int(self.led_id)]), int(self.led_dur))
        else:
            self.led_board.deny()

        self.led_id = ""
        self.led_dur = ""

    def flash_leds(self, duration):
        '''Flash all leds for a given duration'''
        self.led_board.light_all(duration)

    def exit_action(self, *sig):
        '''Power off'''
        self.led_board.power_off()

