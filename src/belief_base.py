from sympy import Not
from sympy.logic.boolalg import to_cnf
from .resolution import pl_resolution
from itertools import combinations
import numpy as np


class BeliefBase:
    def __init__(self, beliefs=[]) -> None:
        self.beliefs = beliefs

    def add_belief(self, sentence, confidence: float):
        cnf_sentence = to_cnf(sentence)

        print(f"\n >> Adding {sentence} and converted to CNF: {cnf_sentence}")

        self.beliefs = self.revise(self.beliefs, cnf_sentence, confidence)

    def __repr__(self) -> str:
        return "\n".join(str(x) for x in self.beliefs)

    def entails(self, base, formula):
        formula = to_cnf(formula)

        if self.check_if_already_there(base, formula):
            return True

        return pl_resolution(base, formula)

    def check_if_already_there(self, base, formula):

        if len(base) > 0:
            formulas = [x.sentence for x in base]
            return True if formula in formulas else False
        else:
            return False

    def remainders(self, base, formula: str = ""):
        formula = to_cnf(formula)

        all_combinations = []
        for L in range(0, len(base) + 1):
            for subset in combinations(base, L):
                if len(subset) > 0:
                    all_combinations.append(list(subset))

        entailments = []
        for subset in all_combinations:
            entailments.append(pl_resolution([belief for belief in subset], formula))
        remainders = [
            set(x) for i, x in enumerate(all_combinations) if not entailments[i]
        ]

        not_maximum_set = []
        for x in remainders:
            for y in remainders:
                if x.issubset(y) and x is not y:
                    not_maximum_set.append(x)

        out = [element for element in remainders if element not in not_maximum_set]

        return out

    def contract(self, base, formula):
        remainders = self.remainders(base, formula)

        if len(remainders) > 0:

            scores = []

            for element in remainders:
                confidences = [x.confidence for x in element]
                scores.append(np.mean(confidences))

            return list(remainders[scores.index(max(scores))])
        else:
            return []

    def expand(self, base, formula, confidence):
        base.append(Belief(formula, confidence))
        return base

    def revise(self, base, formula, confidence):

        if pl_resolution([], formula):
            confidence = 1.0
            print(f"{formula} is a tautology")

        if pl_resolution([], Not(formula)) or self.check_if_already_there(
            base, formula
        ):
            return base
        else:
            neg_formula = Not(formula)

            base = self.contract(base, neg_formula)
            base = self.expand(base, formula, confidence)

            return base


class Belief:
    def __init__(self, sentence, confidence: float) -> None:
        self.sentence = sentence
        self.confidence = confidence

    def __repr__(self) -> str:
        return f"Belief: {self.sentence} with confidence:{self.confidence}"


if __name__ == "__main__":
    test = BeliefBase()

    test.add_belief("p", 0.8)
    print(f">>>1\n {test}")
    test.add_belief("q", 0.5)
    print(f">>>2\n {test}")
    test.add_belief("p & q", 0.1)
    print(f">>>3\n {test}")
    test.add_belief("p | q", 0.9)
    print(f">>>4\n {test}")
    test.add_belief("p >> q", 0.75)
    print(f">>>5\n {test}")
    test.add_belief("~q", 0.96)
    print(f">>>6\n {test}")
    test.add_belief("~s | s", 0.96)
    print(f">>>7\n {test}")
    test.add_belief("~s & s", 0.96)
    print(f">>>8\n {test}")
