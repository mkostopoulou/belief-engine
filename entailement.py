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
        cnf_frm = to_cnf(formula)
        clauses.append(~cnf_frm)

        # Apply resolution to resulting clauses
        repeat = True
        clauses_to_be_resolved = clauses
        while repeat:
            previous = clauses_to_be_resolved
            # unique combinations of clauses
            pairs = itertools.combinations(clauses_to_be_resolved, 2)
            list_pairs = list(pairs)
            print("clauses_to_be_resolved: ", clauses_to_be_resolved)

            # compare literals of all pairs
            repeat = False
            clauses_to_be_resolved = []
            for clause1, clause2 in list_pairs:
                c1_literals = self.agm.Belief_sub(clause1)
                c2_literals = self.agm.Belief_sub(clause2)
                print(" c1_literals: ", c1_literals)
                print(" c2_literals: ", c2_literals)
                for literal_c1 in c1_literals:
                    for literal_c2 in c2_literals:
                        # check for complementary literals
                        if literal_c1 == ~literal_c2 or literal_c2 == ~literal_c1:
                            # every time we produce a new clause we will start resolving again
                            # until no new clause is created or the set is empty
                            repeat = True

                            # remove literal_c1 from clause1 and literal_c2 from clause2
                            c1_literals.remove(literal_c1)
                            c2_literals.remove(literal_c2)

                            # combine left overs in one new clause
                            left_overs = list(set(c1_literals + c2_literals))
                            print(" left_overs: ", left_overs)
                            if len(left_overs)>0:
                                c = Or(*tuple(left_overs))
                if c not in clauses_to_be_resolved:
                    print("  add: ", c)
                    clauses_to_be_resolved.append(c)
                print("")
            # Check if no new clause has been added to the KB
            if previous == clauses_to_be_resolved:
                return False
        isEmptyClause = not len(clauses_to_be_resolved) > 0
        # sys.exit()
        return isEmptyClause


if __name__ == "__main__":
    res = Resolution()
    # example from slides9 page 48/73
    Belief_Set = res.check_entailment(['~r | p | s', '~p | r', '~s | r', '~r'], '~p')
    print(Belief_Set)

    # example from ex9 1.
    #Belief_Set = res.check_entailment(['~p >> q', 'q >> p', 'p >> r', 'r & s'], 'p & r & s')
    #print(Belief_Set)

    # print("Belief_Set  : ", output(agm.belief_base.belief_set))