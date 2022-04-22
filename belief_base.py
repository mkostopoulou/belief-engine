from sympy import *
from belief import Belief

PROMPT = ">>> "

class BeliefBase:
    def __init__(self):
        # Sort by decreasing order
        self.belief_set = []
        self.belief_base = []
        self.belief_order = {}


    ### Defining Beliefs
    def get_information(self):
        print("Define a formula : ")
        prop = input(PROMPT)
        #frm = to_cnf(prop.lower())
        frm = prop.lower()

        for belief in self.belief_set:
            if frm == belief.formula:
                print("Belief is already in belief set : ", prop)
                return None

        print("Define order for given formula : ")
        order = float(input(PROMPT))
        order = self.order_eval(order)

        return Belief(frm, order)
    
    def order_eval(self, order):
        while order>1 or order<=0:
            print("Invalid Order! Please choose an order between zero and 1 (0, 1]:")
            order = float(input(PROMPT))
        return order
    

    def add_belief(self, belief):
        self.belief_set.append(belief)
        return self.belief_set

    def remove_belief(self, belief):
        for i in self.belief_set:
            if belief.formula == i.formula:
                self.belief_set.remove(belief)
        return self.belief_set

    def add(self, belief):
        self.belief_base.append(belief)
        return self.belief_set

