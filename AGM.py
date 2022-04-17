from sympy import *
from belief_base import BeliefBase

PROMPT = ">>> "

class AGM:
    def __init__(self):
        # Sort by decreasing order
        self.belief_base = BeliefBase()

    ### Connectives
    def Negation (self, frm):
        return ~(frm)

    def Conjunction (self, frm1, frm2):
        return frm1 and frm2

    def Disjunctoin (self, frm1, frm2):
        return frm1 or frm2

    def Implication (self, frm1, frm2):
        frm1 = self.Negation(frm1)
        return frm1 or frm2

    def Bi_implication (self, frm1, frm2):
        imp1 = self.Implication(frm1, frm2)
        imp2 = self.Implication(frm2, frm1)
        return imp1 and imp2


    ### Check Subsets of a Belief (??)
    def Belief_sub (self, frm):
        return frm.atoms()


    ### Gain New Information - Revision
    def Revision (self, belief):
        self.Contraction(belief)
        self.Expansion(belief)
        return self.belief_base.belief_set


    ### Gain New Information - Contraction
    def Contraction (self, belief):
        frm = belief.formula
        neg_frm = self.Negation(frm)
        neg_sub_frm = []
        subsets = self.Belief_sub(frm)
        for i in subsets:
            neg_sub_frm.append(self.Negation(i))

        contractions = neg_sub_frm + [neg_frm]
        for belief in self.belief_base.belief_set:
            if belief.formula in contractions:
                self.belief_base.remove_belief(belief)

        return self.belief_base.belief_set


    ### Gain New Information - Expansion
    def Expansion (self, belief):
        frm = belief.formula
        if frm not in self.belief_base.belief_set:
            self.belief_base.add_belief(belief)
        return self.belief_base.belief_set


    ### Updating Belife Set
    def update_BS (self):
        gain_inf = "Y"
        while gain_inf == "Y":
            belief = self.belief_base.get_information()

            if belief is not None:
                self.Revision(belief)

            print("Do you want to add a new blief to the belief set? Y/N")
            gain_inf = input(PROMPT)
        return self.belief_base.belief_set


def output(belief_set):
    beliefs = []
    for belief in belief_set:
        frm = str(belief.formula)
        if not frm.startswith('('):
            frm = '(' + frm + ')'
        beliefs.append(frm)

    return ' & '.join(map(str, beliefs))

"""
From the slides09 page 37/73:
r ↔ p ∨ s
result: (¬r ∨ p ∨ s) ∧ (¬p ∨ r ) ∧ (¬s ∨ r )

Engine test
Input:
1. r>>(p|s)
2. r<<(p|s)

Output:
(p | s | ~r) & (r | ~p) & (r | ~s)
"""
if __name__ == "__main__":
    agm = AGM()
    Belief_Set = agm.update_BS()
    print("Belief_Set update : ", output(agm.belief_base.belief_set))
