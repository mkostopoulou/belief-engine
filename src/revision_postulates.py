from sympy import *
from bs import BeliefBase

class RevisionPostulates():
        # B ∗ φ = Cn(B ∗ φ)
        def closure(self, engine: BeliefBase):
            if not base_exists(engine.beliefs):
                return False

            f = request_formula()
            c = request_confidence()

            # Do revision
            rev_B = engine.revise(engine.beliefs, f, c)  # B ∗ φ

            # produce base set Cn(rev_B)
            cn_rev_B = []  # TODO

            # check if f is present in both rev_B and Cn(rev_B)
            frm = to_cnf(f)
            return frm in rev_B and frm in cn_rev_B

        # φ ∈ B ∗ φ
        def success(self, engine: BeliefBase):
            f = b.formula

            # Do revision
            rev_B = []  # B ∗ φ

            # chek if f exists in rev_B

            return True

        # B ∗ φ ⊆ B + φ
        def inclusion(self, engine: BeliefBase):
            if not base_exists(engine.beliefs):
                return False

            f = request_formula()
            c = request_confidence()

            # Do revision
            rev_B = engine.revise(engine.beliefs, f, c)  # B ∗ φ

            # Do expansion
            exp_B = engine.expand(engine.beliefs, f, c)  # B + φ

            # chek if rev_B is a subset of exp_B
            return rev_B.issubset(exp_B)

        # f ¬φ /∈ B, then B ∗ φ = B + φ
        def vacuity(self, engine: BeliefBase):
            if not base_exists(engine.beliefs):
                return False

            f = request_formula()
            c = request_confidence()

            # check ~f does not exist in B
            inConflict = False
            conflict = to_cnf(Not(f))
            for belief in engine.beliefs:
                if belief.sentence == conflict:
                    inConflict = True
                    break

            # Do revision
            rev_B = engine.revise(engine.beliefs, f, c)  # B ∗ φ

            # Do expansion
            exp_B = engine.expand(engine.beliefs, f, c)  # B + φ

            # if not inConflict, check if rev_B is equal to exp_B
            return not inConflict and exp_B == rev_B

        # B ∗ φ is consistent if φ is consistent
        # A consistent set of sentences is a set all of which can be true together
        # KB ∧ ¬φ
        def consistency(self, engine: BeliefBase):
            if not base_exists(engine.beliefs):
                return False

            f = request_formula()

            return engine.entails(engine.beliefs, f)

        # If (φ ↔ ψ) ∈ Cn(∅), then B ∗ φ = B ∗ ψ
        def extensionality(self, engine: BeliefBase):
            if not base_exists(engine.beliefs):
                return False

            print('Provide two formulas that are bi-implicated: φ ↔ ψ')
            f1 = request_formula()
            c1 = request_confidence()
            f2 = request_formula()
            c2 = request_confidence()

            rev_B1 = engine.revise(engine.beliefs, f1, c1)  # B ∗ φ
            rev_B2 = engine.revise(engine.beliefs, f2, c2)  # B ∗ φ

            return rev_B1 == rev_B2

PROMPT = ">>> "

def request_formula():
    formula_input = None
    while formula_input is None:
        print("Provide belief formula, ex: ~p | q")
        formula_input = input(PROMPT) or None
    return formula_input

def request_confidence():
    confidence_input = None
    while confidence_input is None:
        print("Provide belief confidence in range (0,1], ex: 0.2")
        confidence_input = float(input(PROMPT)) or None
    return confidence_input

def base_exists(beliefs):
    if not len(beliefs) > 0:
        print("No belief base found.")
        return False
    return True



