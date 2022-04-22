import random
from sympy import *
from belief import Belief
from belief_base import BeliefBase

class PostulatesOfRevision:
    def __init__(self):
        # Sort by decreasing order
        self.bb = BeliefBase()

    # B ∗ φ = Cn(B ∗ φ)
    def closure(self, B: BeliefBase, b: Belief):
        f = b.formula

        # Do revision
        rev_B = []  # B ∗ φ

        # check if f is not present in both rev_B and Cn(rev_B)

        return True

    # φ ∈ B ∗ φ
    def success(self, B: BeliefBase, b: Belief):
        f = b.formula

        # Do revision
        rev_B = []  # B ∗ φ

        # chek if f exists in rev_B

        return True

    # B ∗ φ ⊆ B + φ
    def inclusion(self, B: BeliefBase, b: Belief):
        f = b.formula

        # Do revision
        rev_B = []  # B ∗ φ

        # Do expansion
        exp_B = []  # B + φ

        # chek if rev_B is a subset of exp_B

        return True

    # f ¬φ /∈ B, then B ∗ φ = B + φ
    def vacuity(self, B: BeliefBase, b: Belief):
        f = b.formula

        # check ~f does not exist in B
        inConflict = false

        # Do revision
        rev_B = []  # B ∗ φ

        # Do expansion
        exp_B = []  # B + φ

        # if not inConflict, check if rev_B is equal to exp_B

        return True

    # B ∗ φ is consistent if φ is consistent
    # A consistent set of sentences is a set all of which can be true together
    def consistency(self, B: BeliefBase, b: Belief):
        return True

    # If (φ ↔ ψ) ∈ Cn(∅), then B ∗ φ = B ∗ ψ
    def extensionality(self, B: BeliefBase, b1: Belief, b2: Belief):
        return True
