from tabnanny import verbose
from sympy import Not
from sympy.logic.boolalg import to_cnf
from utils import arithmetic_series
from resolution import pl_resolution
from itertools import combinations
import numpy as np


class BeliefBase:
    def __init__(self, beliefs=[]) -> None:
        self.beliefs = beliefs
        self.max_rank = len(self.beliefs)
        self.confidence = False

    def add_belief(self, sentence, confidence: float = None, verbose = False):
        if len(self.beliefs)>0:
            assert(self.confidence == (confidence is not None)), "You should either use rank-based valuation function or confidence based. Not both."

        cnf_sentence = to_cnf(sentence)
        if verbose:
            print(f"\n >> Adding: {sentence} | with CNF form: {cnf_sentence}")

        if confidence is not None:
            self.confidence = True
            self.beliefs = self.revise(self.beliefs, cnf_sentence, confidence)
        else:
            new_beliefs = self.revise(self.beliefs, cnf_sentence, confidence)
            new_beliefs.sort(key=lambda x: x.rank)
            self.beliefs = [
                RankedBelief(x.sentence, i + 1) for i, x in enumerate(new_beliefs)
            ]
            self.max_rank = len(self.beliefs)

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

    def contract(self, base, formula, selection_function):
        remainders = self.remainders(base, formula)

        if len(remainders) > 0:
            return selection_function(remainders)
        else:
            return []

    def confidence_selection_function(self, remainders):
        scores = []

        for element in remainders:
            confidences = [x.confidence for x in element]
            scores.append(np.mean(confidences))

        return list(remainders[scores.index(max(scores))])

    def ranked_selection_function(self, remainders):
        scores = []
        denominator = arithmetic_series(0, self.max_rank, 1)
        for element in remainders:
            confidences = [int(self.max_rank - x.rank) for x in element]
            scores.append(sum(confidences) / denominator)

        return list(remainders[scores.index(max(scores))])

    def expand(self, base, formula, confidence):

        if confidence is not None:
            base.append(ConfidenceBelief(formula, confidence))
        else:
            base.append(RankedBelief(formula, self.max_rank + 1))
            self.max_rank += 1

        return base

    def revise(self, base, formula, confidence: float = None):

        if pl_resolution([], formula):
            confidence = 1.0 if confidence is not None else None
            print(f"{formula} is a tautology")

        if pl_resolution([], Not(formula)) or self.check_if_already_there(
            base, formula
        ):
            return base
        else:
            neg_formula = Not(formula)

            if confidence is not None:
                base = self.contract(
                    base, neg_formula, self.confidence_selection_function
                )
            else:
                base = self.contract(base, neg_formula, self.ranked_selection_function)

            base = self.expand(base, formula, confidence)

            return base


class Belief:
    def __init__(self, sentence: str) -> None:
        self.sentence = sentence


class RankedBelief(Belief):
    def __init__(self, sentence: str, rank: int) -> None:
        super().__init__(sentence)
        self.rank = rank

    def __repr__(self) -> str:
        return f"\nBelief: {self.sentence} with rank:{self.rank}."


class ConfidenceBelief(Belief):
    def __init__(self, sentence: str, confidence: float) -> None:
        super().__init__(sentence)
        self.confidence = confidence

    def __repr__(self) -> str:
        return f"\nBelief: {self.sentence} with confidence:{self.confidence}."


if __name__ == "__main__":
    test_confidence = BeliefBase()

    test_confidence.add_belief("p", 0.8)
    print(f">>>1\n {test_confidence}")
    test_confidence.add_belief("q", 0.5)
    print(f">>>2\n {test_confidence}")
    test_confidence.add_belief("p & q", 0.1)
    print(f">>>3\n {test_confidence}")
    test_confidence.add_belief("p | q", 0.9)
    print(f">>>4\n {test_confidence}")
    test_confidence.add_belief("p >> q", 0.75)
    print(f">>>5\n {test_confidence}")
    test_confidence.add_belief("~q", 0.96)
    print(f">>>6\n {test_confidence}")
    test_confidence.add_belief("~s | s", 0.96)
    print(f">>>7\n {test_confidence}")
    test_confidence.add_belief("~s & s", 0.96)
    print(f">>>8\n {test_confidence}")

    test_rank = BeliefBase()
    test_rank.add_belief("p")
    print(f">>>1\n {test_rank}")
    test_rank.add_belief("q")
    print(f">>>2\n {test_rank}")
    test_rank.add_belief("p & q")
    print(f">>>3\n {test_rank}")
    test_rank.add_belief("p | q")
    print(f">>>4\n {test_rank}")
    test_rank.add_belief("p >> q")
    print(f">>>5\n {test_rank}")
    test_rank.add_belief("~q")
    print(f">>>6\n {test_rank}")
    test_rank.add_belief("~s | s")
    print(f">>>7\n {test_rank}")
    test_rank.add_belief("~s & s")
    print(f">>>8\n {test_rank}")
