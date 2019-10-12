
from finite_state_machine import *
from kpc_2 import KPC
from charlie import Charlie
from keypad import Keypad

def main():
    '''Main'''
    keypad = Keypad()
    keypad.setup()

    charlie = Charlie()
    charlie.setup()

    kpc = KPC(keypad, charlie)

    #kpc.write_new_password("1234")
    fsm = FSM(kpc)

    def signal_is_digit(signal):
        '''Returns if the signal is a digit'''
        return 48 <= ord(signal) <= 57

    def signal_accept_all(signal):
        '''Accept every signal'''
        return True

    # Setting up the FSM with the correct rules
    # Rules that are representing one arc each in the full FSM graph.
    # Setting the rules in the order which makes specific-before-general

    # From state s_init
    rule_1 = Rule(
        "s_init",
        "s_read",
        signal_accept_all,
        kpc.init_passcode_entry)

    # From state s_read
    rule_3 = Rule("s_read", "s_verify", "*", kpc.verify_login)
    rule_2 = Rule(
        "s_read",
        "s_read",
        signal_is_digit,
        kpc.password_buffer_add)
    rule_13 = Rule("s_read", "s_init", "#", kpc.exit_action)

    # From state s_verify
    # Not sure about agent action here
    rule_5 = Rule("s_verify", "s_active", "Y", kpc.pass_func)
    rule_4 = Rule("s_verify", "s_init", signal_accept_all, kpc.exit_action)

    # From state s_active
    rule_6 = Rule("s_active", "s_read_2", "*", kpc.init_passcode_entry)
    rule_17 = Rule("s_active", "s_init", "#", kpc.exit_action)
    rule_14 = Rule("s_active", "s_led", signal_is_digit, kpc.set_led_id)

    # From state s_led
    rule_15 = Rule("s_led", "s_led", signal_is_digit, kpc.set_led_dur)
    rule_16 = Rule("s_led", "s_active", "*", kpc.light_leds)

    # From state s_read_2
    rule_8 = Rule("s_read_2", "s_read_3", "*", kpc.pass_func)
    rule_7 = Rule(
        "s_read_2",
        "s_read_2",
        signal_is_digit,
        kpc.password_buffer_add)
    rule_10 = Rule("s_read_2", "s_active", signal_accept_all,
                   kpc.exit_action)

    # From state s_read_3
    rule_12 = Rule("s_read_3", "s_active", "*", kpc.validate_passcode_change)
    rule_9 = Rule(
        "s_read_3",
        "s_read_3",
        signal_is_digit,
        kpc.password_buffer_add2)
    rule_11 = Rule("s_read_3", "s_active", signal_accept_all,
                   kpc.exit_action)

    # Same order as the rules above
    rule_order = [
        rule_1,
        rule_3,
        rule_2,
        rule_13,
        rule_5,
        rule_4,
        rule_6,
        rule_17,
        rule_14,
        rule_15,
        rule_16,
        rule_8,
        rule_7,
        rule_10,
        rule_12,
        rule_9,
        rule_11]
    # Adding each rule to the FSM
    for rule in rule_order:
        fsm.add_rule(rule)

    fsm.main()


main()
