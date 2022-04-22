import random
from sympy import *
from belief import Belief
from belief_base import BeliefBase
from postulates_of_revision import PostulatesOfRevision

rev_post = PostulatesOfRevision()
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
    def request_belief(self):
        while True:
            print("Type a belief for postulate check")
            belief_input = input(PROMPT) or None
            if not belief_input == None:
                break

        # [0.0, 1.0)
        order = random.random()
        formula = to_cnf(belief_input)
        return Belief(formula, order)

    def reset_base(self):
        self.bb.belief_base = []

    def print_base(self, withOrder = False):
        bb_output = output(self.bb.belief_base, withOrder)
        print('Belief base : ', bb_output)

    def closure(self):
        belief = self.request_belief()
        return rev_post.closure(self.bb.belief_base, belief)

    def success(self):
        belief = self.request_belief()
        return rev_post.success(self.bb.belief_base, belief)

    def inclusion(self):
        belief = self.request_belief()
        return rev_post.inclusion(self.bb.belief_base, belief)

    def vacuity(self):
        belief = self.request_belief()
        return rev_post.vacuity(self.bb.belief_base, belief)

    def consistency(self):
        belief = self.request_belief()
        return rev_post.consistency(self.bb.belief_base, belief)

    def extensionality(self):
        belief1 = self.request_belief()
        belief2 = self.request_belief()
        return rev_post.extensionality(self.bb.belief_base, belief1, belief2)

    def check_postulate(self, postulate):
        if postulate == '1':
            return "Closure is {0}".format('satisfied' if self.closure() else 'not satisfied')
        elif postulate == '2':
            return "Success is {0}".format('satisfied' if self.success() else 'not satisfied')
        elif postulate == '3':
            return "Inclusion is {0}".format('satisfied' if self.inclusion() else 'not satisfied')
        elif postulate == '4':
            return "Vacuity is {0}".format('satisfied' if self.vacuity() else 'not satisfied')
        elif postulate == '5':
            return "Consistency is {0}".format('satisfied' if self.consistency() else 'not satisfied')
        elif postulate == '6':
            return "Extensionality is {0}".format('satisfied' if self.extensionality() else 'not satisfied')


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


POSTULATES = [
    'POSTULATES',
    100*"-",
    '1 : Closure',
    '2 : Success',
    '3 : Inclusion',
    '4 : Vacuity',
    '5 : Consistency',
    '6 : Extensionality',
]
def request_postulate(postulates: Postulates):
    print('Select which postulate to check:')
    while True:
        print(100 * "=")
        # Request action
        for p in POSTULATES:
            print(p)
        postulate_input = input(PROMPT)
        if int(postulate_input) not in range(1, len(POSTULATES)-1):
            print('* Chose an available postulate! *')
            continue
        else:
            print(postulates.check_postulate(postulate_input))

        # Request termination
        print("Do you want to check more postulates? : Type 'n' (stop) | Press Enter (continue)")
        continue_input = input(PROMPT) or 'y'
        if continue_input != 'y':
            break


ACTIONS = [
    'ACTIONS',
    100*"-",
    '1 : Set belief base',
    '2 : Reset belief base',
    # '3 : Add one belief to belief base',
    '3 : Print belief base',
    '4 : Revise belief base',
    '5 : Check AGM postulates',
]
def request_action(postulates: Postulates):
    print('Select action:')
    while True:
        print(100 * "=")

        # Request action
        for a in ACTIONS:
            print(a)
        action_input = input(PROMPT)
        if int(action_input) not in range(1, len(ACTIONS) - 1):
            print('* Chose an available action! *')
            continue

        # ...
        handle_action(postulates, action_input)

        # Request termination
        print("Do you want to perform more actions? : Type 'n' (stop) | Press Enter (continue)")
        continue_input = input(PROMPT) or 'y'
        if continue_input != 'y':
            break


def handle_action(postulates: Postulates, action):
    print(100 * "_")
    if action == '1':
        print("Type belief base :")
        bb_input = input(PROMPT) or None
        print('setting base...')
        postulates.set_base(bb_input)
    elif action == '2':
        print('resetting base...')
        postulates.reset_base()
    # elif action == '3':
    #     print("Type belief :")
    #     b_input = input(PROMPT) or None
    #     print('adding belief...')
    #     postulates.add_belief(b_input)
    elif action == '4':
        print('printing base...')
        postulates.print_base(True)
    elif action == '5':
        print('revising base... (TBA)')
    elif action == '6':
        request_postulate(postulates)

PROMPT = ">>> "
p = Postulates()
if __name__ == "__main__":
    # Request action
    request_action(p)

    print(100 * "=")
    print("PROCESS TERMINATED")
