import random
from sympy import *
from belief import Belief
from belief_base import BeliefBase


class Postulates:
    def __init__(self):
        # Sort by decreasing order
        self.bb = BeliefBase()

    # example type: ~r | p | s & ~p | r & ~s | r
    def set_base(self, str_base: str):
        if not str_base == None:
            print("Old belief base :")
            self.print_base()
            formulas = str_base.split('&')
            new_base = []
            for f in formulas:
                # [0.0, 1.0)
                order = random.random()
                formula = to_cnf(f)
                new_base.append(Belief(formula, order))

            # set new base
            self.bb.belief_base = new_base
            print("New belief base :")
        self.print_base()

    # example type: p
    def add_belief(self, str_formula: str):
        if not str_formula == None :
            print("Old belief base :")
            self.print_base()
            # [0.0, 1.0)
            order = random.random()
            formula = to_cnf(str_formula)
            self.bb.add(Belief(formula, order))
            print("New belief base :")
        self.print_base()

    def reset_base(self):
        self.bb.belief_base = []

    def print_base(self, withOrder = False):
        bb_output = output(self.bb.belief_base, withOrder)
        print('Belief base : ', bb_output)


def output(bb, withOrder = False):
    if withOrder:
        beliefs = {}
        for belief in bb:
            beliefs[belief.formula] = belief.order
    else:
        beliefs = []
        for belief in bb:
            beliefs.append(belief.formula)

    return beliefs

def handle_action(postulates: Postulates, action):
    failed = False
    print(100 * "_")
    if action == '1':
        print("Type belief base :")
        bb_input = input(PROMPT) or None
        print('setting base...')
        postulates.set_base(bb_input)
    elif action == '2':
        print('resetting base...')
        postulates.reset_base()
    elif action == '3':
        print("Type belief :")
        b_input = input(PROMPT) or None
        print('adding belief...')
        postulates.add_belief(b_input)
    elif action == '4':
        print('printing base...')
        postulates.print_base(True)
    elif action == '5':
        print('revising base... (TBA)')
    else:
        print('* Chose an available action! *')
        failed = True
    print(100 * "_")
    return failed

# Global variables
PROMPT = ">>> "
ACTIONS = [
    'ACTIONS',
    100*"-",
    'Set belief base : 1',
    'Reset belief base : 2',
    'Add one belief to belief base: 3',
    'Print belief base : 4',
    'Revise belief base : 5'
]
p = Postulates()
if __name__ == "__main__":
    while True:
        print(100*"=")

        # Request action
        for a in ACTIONS:
            print(a)
        action_input = input(PROMPT)

        # ...
        failed = handle_action(p, action_input)

        # Request termination
        if not failed:
            print("Do you want to perform more actions? : Type 'n' (stop) | Press Enter (continue)")
            continue_input = input(PROMPT) or 'y'
            if continue_input != 'y':
                break