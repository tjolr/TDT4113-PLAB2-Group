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

    def get_next_signal(self):
        '''query the agent for next signal'''
        self.symbol = self.agent.get_next_signal()

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

        #Query for next signal and run rules until the FSM enters its default final state
        while self.state != "":
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

def signal_accept_all(): return True

def main():
    '''Main method for testing'''
    agent = "Agent()"
    fsm = FSM(agent)

    #Rules that are representing one arc each in the full FSM graph.
    R1 = Rule("s_init", "s_read", signal_accept_all, "init_passcode_entry")
    R2 = Rule("s_read", "s_read", signal_is_digit, "get_next_signal")

    R3 = Rule("s_read", "s_verify", "*", "verify_login")
    R4 = Rule("s_verify", "s_init", signal_accept_all, "init") #Not sure about agent action here
    R5 = Rule("s_verify", "s_active", "Y", "fully_activate_agent") #Not sure about agent action here
    R6 = Rule("s_active", "s_read_2", "*", "init_passcode_entry")
    R7 = Rule("s_read_2", "s_read_2", signal_is_digit, "get_next_signal")

    R8 = Rule("s_read_2", "s_read_3", "*", "cache_1st_new_password")
    R9 = Rule("s_read_3", "s_read_3", signal_is_digit, "get_next_signal")

    R10 = Rule("s_read_2", "s_active", signal_accept_all, "fully_ activate_agent") #Not sure about agent action
    R11 = Rule("s_read_3", "s_read_3", signal_accept_all, "fully_ activate_agent") #Not sure about agent action
    R12 = Rule("s_read_3", "s_active", "*", "fully_ activate_agent") #Not sure about agent action
    R13 = Rule("s_read", "s_init", signal_accept_all, "init") #Not sure about agent action


    #not implemented correct order according to the FSM
    fsm.add_rule(R1)
    fsm.add_rule(R2)
    fsm.add_rule(R3)
    fsm.add_rule(R4)
    fsm.add_rule(R5)
    fsm.add_rule(R6)
    fsm.add_rule(R7)
    fsm.add_rule(R8)
    fsm.add_rule(R9)
    fsm.add_rule(R10)
    fsm.add_rule(R11)
    fsm.add_rule(R12)
    fsm.add_rule(R13)



    print(fsm.rule_list)


#main()






