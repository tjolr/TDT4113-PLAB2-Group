'''Finite state machine'''
from inspect import isfunction

class FSM:
    '''Finite state machine class'''

    def __init__(self, agent):
        '''Init'''
        self.rule_list = []
        self.agent = agent
        self.state = None
        self.symbol = None

    def add_rule(self, rule):
        '''Add a rule to the end of the rule_list'''
        self.rule_list.append(rule)

    def get_next_signal(self):
        '''query the agent for next signal'''
        return self.agent.get_next_signal()

    def run_rules(self):
        '''Go through the rule list, applying each rule until one is fired'''
        for rule in self.rule_list:
            if self.apply_rule(rule):
                self.fire_rule(rule)


    def apply_rule(self, rule):
        '''Applying a rule, checking whether the conditions are met'''
        return rule.match(self.state, self.symbol)

    def fire_rule(self, rule):
        '''Use the consequent of a rule
        sets the next state of FSM, and calls the
        appropiate agent action method'''
        self.state = rule.state2
        self.agent.do_action(rule.action, self.symbol)

    def main(self):
        '''Main method'''





class Rule:
    '''Rule Class that holds its current state and next state'''

    def __init__(self, state1, state2, signal, action):
        '''Constructor of the Rule class'''
        self.state1 = state1
        self.state2 = state2
        self.signal = signal
        self.action = action
        self.symbol = None #When defining rule: rule.symbol = signal_is_digit()

    def match(self, state, symbol):
        '''Checking whether the conditions are met for a rule'''
        return state == self.state1 and symbol == self.signal

def signal_is_digit(signal): return 48 <= ord(signal) <= 57








