'''Finite state machine'''
from inspect import isfunction
#from kpc_2 import *


class FSM:
    '''Finite state machine class'''

    def __init__(self, agent):
        '''Init'''
        self.rule_list = []
        self.agent = agent
        self.symbol = None
        self.state = 's_init'

    def add_rule(self, rule):
        '''Add a rule to the end of the rule_list'''
        self.rule_list.append(rule)

    def get_next_signal(self, debug=True):
        '''query the agent for next signal'''
        self.symbol = self.agent.get_next_signal()

        if debug:
            print(f'Next signal: {self.symbol}')

    def run_rules(self):
        '''Go through the rule list, applying each rule until one is fired'''
        for rule in self.rule_list:
            if self.apply_rule(rule):
                self.fire_rule(rule)
                break

    def apply_rule(self, rule):
        '''Applying a rule, checking whether the conditions are met'''
        return rule.match(self.state, self.symbol)

    def fire_rule(self, rule, debug=True):
        '''Use the consequent of a rule
        sets the next state of FSM, and calls the
        appropiate agent action method'''
        self.state = rule.state2
        sym = self.symbol
        rule.action(sym)

        if debug:
            print("FSM is now in state: ", self.state)

    def main(self):
        '''Main method'''

        # Query for next signal and run rules until the FSM enters its default
        # final state
        i = 0
        while i < 25:
            self.get_next_signal()

            self.run_rules()
            i += 1


class Rule:
    '''Rule Class that holds its current state and next state'''

    def __init__(self, state1, state2, signal, action):
        '''Constructor of the Rule class'''
        self.state1 = state1
        self.state2 = state2
        self.signal = signal
        self.action = action

    def match(self, state, symbol):
        '''Checking whether the conditions are met for a rule'''
        if isfunction(self.signal):
            # Symbol is a function that accepts one argument
            return state == self.state1 and self.signal(symbol)
        return state == self.state1 and symbol == self.signal


def signal_is_digit(signal):
    '''Returns if the signal is a digit'''
    return 48 <= ord(signal) <= 57


def signal_accept_all(signal):
    '''Accept every signal'''
    return True



