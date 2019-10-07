'''Finite state machine'''

class FSM():
    '''Finite state machine class'''

    def __init__(self):
        '''Init'''
        self.rule_list = []

    def add_rule(self, rule):
        '''Add a rule to the end of the rule_list'''
        self.rule_list.append(rule)

    def get_next_signal(self):
        '''query the agent for next signal'''

    def run_rules(self):
        '''Go through the rule list, applying each rule until one is fired'''

    def apply_rule(self, rule):
        '''Applying a rule, checking whether the conditions are met'''

    def fire_rule(self, rule):
        '''Use the consequent of a rule
        sets the next state of FSM, and calls the
        appropiate agent action method'''







