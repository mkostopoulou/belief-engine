from sympy import *
from bs import BeliefBase

class ContractionPostulates():
    # B ÷ φ = Cn(B ÷ φ)
    def closure(self, engine: BeliefBase):
        return True

    # If φ /∈ Cn(∅), then φ /∈ Cn(B ÷ φ)
    def success(self, engine: BeliefBase):
        return True

    # B ÷ φ ⊆ B
    def inclusion(self, engine: BeliefBase):
        return True

    # f φ /∈ Cn(B), then B ÷ φ = B
    def vacuity(self, engine: BeliefBase):
        return True

    # B ⊆ (B ÷ φ) + φ
    def recovery(self, engine: BeliefBase):
        return True

    # If φ ↔ ψ ∈ Cn(∅), then B ÷ φ = B ÷ ψ
    def extensionality(self, engine: BeliefBase):
        return True

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
