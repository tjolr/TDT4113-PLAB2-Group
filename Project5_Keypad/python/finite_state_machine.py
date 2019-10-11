'''Finite state machine'''
from inspect import isfunction

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

    def get_next_signal(self, debug = True):
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
        self.agent.do_action(rule.action, self.symbol)

        if debug:
            print("FSM is now in state: ",self.state)


    def main(self):
        '''Main method'''

        #Setting up the FSM with the correct rules
        # Rules that are representing one arc each in the full FSM graph.
        # Setting the rules in the order which makes specific-before-general

        # From state s_init
        R1 = Rule("s_init", "s_read", signal_accept_all, "reset_password_accumulator")

        # From state s_read
        R3 = Rule("s_read", "s_verify", "*", "verify_login")
        R2 = Rule("s_read", "s_read", signal_is_digit, "append_next_password_digit")
        R13 = Rule("s_read", "s_init", signal_accept_all, "reset_agent")

        # From state s_verify
        R5 = Rule("s_verify", "s_active", "Y", "fully_activate_agent")  # Not sure about agent action here
        R4 = Rule("s_verify", "s_init", signal_accept_all, "reset_agent")

        # From state s_active
        R6 = Rule("s_active", "s_read_2", "*", "init_passcode_entry")

        # From state s_read_2
        R8 = Rule("s_read_2", "s_read_3", "*", "cache_1st_new_password")
        R7 = Rule("s_read_2", "s_read_2", signal_is_digit, "get_next_signal")
        R10 = Rule("s_read_2", "s_active", signal_accept_all, "fully_ activate_agent")  # Not sure about agent action

        # From state s_read_3
        R12 = Rule("s_read_3", "s_active", "*", "fully_ activate_agent")  # Not sure about agent action
        R9 = Rule("s_read_3", "s_read_3", signal_is_digit, "get_next_signal")
        R11 = Rule("s_read_3", "s_read_3", signal_accept_all, "fully_ activate_agent")  # Not sure about agent action


        # Same order as the rules above
        rule_order = [R1, R3, R2, R13, R5, R4, R6, R8, R7, R10, R12, R9, R11]
        #Adding each rule to the FSM
        for rule in rule_order:
            self.add_rule(rule)


        #Query for next signal and run rules until the FSM enters its default final state
        while self.symbol != "#":
            self.get_next_signal()
            self.run_rules()


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
            #Symbol is a function that accepts one argument
            return state == self.state1 and self.signal(symbol)
        else:
            return state == self.state1 and symbol == self.signal

def signal_is_digit(signal): return 48 <= ord(signal) <= 57

def signal_accept_all(signal): return True

class Agent:
    '''Agent class just for testing'''
    def __init__(self):
        ''''''
        self.signals = ["2", "8", "3", "6", "*", "Y", "*","5","1","7", "*", "5", "1", "7", "*"]

    def get_next_signal(self):
        if self.signals:
            return self.signals.pop(0)
        return "#"

    def do_action(self, action, symbol):
        pass

def main():
    '''Main method for testing'''
    agent = Agent()
    fsm = FSM(agent)


    fsm.main()


main()






