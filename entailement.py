from sympy import *
from AGM import AGM
import itertools
import sys

PROMPT = ">>> "

class Resolution:
    
    def __init__(self):
        self.agm = AGM()

    # To show that KB |= φ, we show that KB ∧ ¬φ is unsatisfiable
    #
    # 1. there are no new clauses that can be added, in which case KB does not entail φ; or,
    # 2. two clauses resolve to yield the empty clause, in which case KB entails φ.
    def check_entailment(self, base, formula):
        # converted into CNF
        clauses = []
        for b in base:
            cnf_b = to_cnf(b)
            clauses.append(cnf_b)

        # contradiction ¬φ
        cnf_frm = to_cnf(~to_cnf(formula))
        clauses.append(cnf_frm)

        # Apply resolution to resulting clauses
        repeat = True
        temp_clauses = []
        clauses_to_be_resolved = clauses
        resolved = []
        while repeat:
            # unique combinations of clauses
            list_pairs = self.pair_maker(clauses_to_be_resolved)
            # print(list_pairs)

            # compare literals of all pairs
            repeat = False
            for clause1, clause2 in list_pairs:
                c1_literals = list(clause1.args) if len(list(clause1.args)) > 1 else [clause1]
                c2_literals = list(clause2.args) if len(list(clause2.args)) > 1 else [clause2]

                # resolve complementary literals, if any
                left_overs = self.resolve_complementary(c1_literals, c2_literals)

                if left_overs is not None:
                    # every time we produce a new clause we will start resolving again
                    # until no new clause is created or the set is empty
                    repeat = True
                    c = Or(*tuple(left_overs))
                    if c not in temp_clauses:
                        temp_clauses.append(c)
                    if clause1 not in resolved:
                        resolved.append(clause1)
                    if clause2 not in resolved:
                        resolved.append(clause2)

            if False in temp_clauses:
                return True

            clauses_to_be_resolved = list(set(clauses_to_be_resolved).difference(set(resolved)) | set(temp_clauses))

            if repeat:
                temp_clauses = []

        isEmptyClause = not len(clauses_to_be_resolved) > 0
        return isEmptyClause
    
    def resolve_complementary(self, c1_literals, c2_literals):
        updated = False
        literals = c1_literals + c2_literals
        for i in literals:
            if ~i in literals:
                updated = True
                literals.remove(i)
                literals.remove(~i)

        return list(set(literals)) if updated else None

    def pair_maker (self, clauses):
        # unique combinations of clauses
        pairs = itertools.combinations(clauses, 2)
        list_pairs = list(pairs)
        return list_pairs
        
        


if __name__ == "__main__":
    res = Resolution()
    # example
    Belief_Set = res.check_entailment(['~p >> q'], 'p | q')
    print(Belief_Set)

    # example from slides9 page 48/73
    Belief_Set = res.check_entailment(['~r | p | s', '~p | r', '~s | r', '~r'], '~p')
    print(Belief_Set)

    # example from ex9 1.
    Belief_Set = res.check_entailment(['~p >> q', 'q >> p', 'p >> r', 'r & s'], 'p & r & s')
    print(Belief_Set)

    # example from ex9 1. wrong
    Belief_Set = res.check_entailment(['~p >> q', 'q >> p', 'p >> r', 'r & s'], 'p & r & u')
    print(Belief_Set)

    # example from ex9 1. wrong
    Belief_Set = res.check_entailment(['~p >> q'], 'q')
    print(Belief_Set)
