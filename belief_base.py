from sympy import *
from belief import Belief

PROMPT = ">>> "

class BeliefBase:
    def __init__(self):
        # Sort by decreasing order
        self.belief_set = []
        self.belief_order = {}


    ### Defining Beliefs
    def get_information(self):
        print("Define a formula : ")
        prop = input(PROMPT)
        frm = to_cnf(prop.lower())

        for belief in self.belief_set:
            if frm == belief.formula:
                print("Belief is already in belief set : ", prop)
                return None

        print("Define order for given formula : ")
        order = input(PROMPT)

        return Belief(frm, order)

    def add_belief(self, belief):
        self.belief_set.append(belief)
        return self.belief_set

    def remove_belief(self, belief):
        for i in self.belief_set:
            if belief.formula == i.formula:
                self.belief_set.remove(belief)
        return self.belief_set

