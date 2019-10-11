# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 10:56:45 2019

@author:
"""


class Rule:
    """Rule implementation"""

    def __init__(self, from_state: int, to_state: int, condition, action):
        # State in which this rule applies
        self.from_state = from_state
        # State to which this rule sends the state machine
        self.to_state = to_state
        # Condition to fire rule
        self.condition = condition
        # Action when firing rule (Agent method)
        self.action = action
        # Last signal
        self.sig = None

    def validate(self, sig):
        """
        Check rule conditions
        param sig: signal to compare with conditions
        return: True or false
        """
        self.sig = sig
        return self.condition(sig)

    def consequence(self, *sig):
        """
        Run consequence of this rule being fired

        return: next state
        """
        self.action(*sig) # Return type void
        return self.to_state


class FSM:
    """
    class FSM
    Implementation of a general finite state machine
    to be instantiated with a ruleset and a reference
    to an agent.
    """

    def __init__(self, agent):
        self.state = 0
        self.agent = agent
        self.rules = []

    def add_rule(self, rule: Rule):
        """
        Add a new rule to the end of the FSM’s rule list.
        """
        self.rules.append(rule)

    #def get_next_signal(self):
    #    """
    #    Query the agent for the next signal.
    #    (Unused)
    #    """
    #    agent.get_next_signal()

    @staticmethod
    def apply_rule(rule: Rule, sig):
        """
        Check whether the conditions of a rule are met.
        """
        return rule.validate(sig)

    def run_rules(self, sig):
        """
        Go through the rule set, in order,
        applying each rule until one of the rules is fired.
        """
        for rule in [rule for rule in self.rules if rule.from_state == self.state]:
            if FSM.apply_rule(rule, sig):
                self.fire_rule(rule, *sig)

        print("Currently in state: ", self.state)

    def fire_rule(self, rule: Rule, *sig):
        """
        Use the consequent of a rule to
        a) set the next state of the FSM, and
        b) call the appropriate agent action method.
        rule.consequence() runs the given agent action
        and returns next state.
        """
        self.state = rule.consequence(*sig)

    def main_loop(self):
        """
        Begin in the FSM’s default initial state and
        then repeatedly call get next signal and run rules
        until the FSM enters its default final state.
        """
        while 1:
            # sig is in [*, #, Y, N, 0-9]
            sig = self.agent.get_next_signal()
            print("Got signal:", sig)
            self.run_rules(sig)
            print("Password buffer is:", self.agent.password_buffer)

