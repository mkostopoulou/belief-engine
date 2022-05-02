from copy import deepcopy
from sympy import to_cnf, Not
from belief_base import RankedBelief, BeliefBase
from resolution import pl_resolution
from itertools import combinations
from numpy import array

TAUTOLOGY = "s | ~s"
CONTRADICTION = "s & ~s"
TEST_STATEMENTS = [
    ("p", 0.8),
    ("q", 0.5),
    ("p & q", 0.1),
    ("p|q", 0.9),
    ("p>>q", 0.75),
    ("q>>p", 0.75),
]
TEST_BELIEF_BASE = [RankedBelief(to_cnf(x), i+1) for i,x in enumerate(TEST_STATEMENTS)]
TEST_BELIEF_BASE_UN = [RankedBelief(to_cnf("p & q"), 1)]


def success(base,p):
    p = to_cnf(p)
    if not pl_resolution([], p):
        base = BeliefBase(base)
        base.add_belief(p)

        return p in [belief.sentence for belief in base.beliefs]


def inclusion(base, p):
    p = to_cnf(p)
    BBase = BeliefBase(base)
    BBase.add_belief(p)
    base.append(RankedBelief(p,BBase.max_rank))
    return set([belief.sentence for belief in BBase.beliefs]).issubset(set([belief.sentence for belief in base]))


def relevance(base, p, q):
    p = to_cnf(p)
    q = RankedBelief(to_cnf(q), 0.95)

    possible_A_primes = BeliefBase().remainders(base, p)
    for A_prime in possible_A_primes:
        if not q in A_prime:
            A_prime.add(q)
            if pl_resolution(A_prime, p):
                return True
    return False


def uniformity(base, p, q):
    q = to_cnf(q)
    p = to_cnf(p)

    A_primes = []
    for L in range(0, len(base) + 1):
        for subset in combinations(base, L):
            if len(subset) > 0:
                A_primes.append(list(subset))

    q_follows = []
    p_follows = []

    for subset in A_primes:
        if pl_resolution(subset, q) != pl_resolution(subset, p):
            return False

        q_follows.append(pl_resolution(subset, q))
        p_follows.append(pl_resolution(subset, p))

    return (q_follows == p_follows) and (
        BeliefBase().contract(base, p, BeliefBase().ranked_selection_function) == BeliefBase().contract(base, q,BeliefBase().ranked_selection_function)
    )


def consistency(base):
    base = deepcopy(base)
    base_clean = deepcopy(base)
    
    
    base.append(RankedBelief(to_cnf(CONTRADICTION), len(base)+1))
    base_clean.append(RankedBelief(to_cnf(TAUTOLOGY), len(base_clean)+1))
    
    random_sentences = [to_cnf("x | f"), to_cnf("x & ~x")]
    with_contradiction = []
    without_contradiction = []
    
    for sentence in random_sentences:
        with_contradiction.append(pl_resolution(base, sentence))
        without_contradiction.append(pl_resolution(base_clean, sentence))

    return all(array(with_contradiction) & ~array(without_contradiction))
    


def vacuity(base, p):
    p = to_cnf(p)
    notp = Not(p)
    base = deepcopy(base)
    if not pl_resolution(base, notp):
        BBase = BeliefBase(base)
        base.append(RankedBelief(p,BBase.max_rank+1))
        revised_auto = BBase.revise(base, p)

        return base == revised_auto


if __name__ == "__main__":
    print('Test of Succes postulate')
    print(success(TEST_BELIEF_BASE, "q"))
    print('--------------------------------------')
    print('Test of Inclusion postulate')
    print(inclusion(TEST_BELIEF_BASE, "o"))
    print('--------------------------------------')
    print('Test of Relevance postulate')
    print(relevance(TEST_BELIEF_BASE, "p", "p & q"))
    print('--------------------------------------')
    print('Test of Uniformity postulate')
    print(uniformity(TEST_BELIEF_BASE_UN, "p", "q"))
    print('--------------------------------------')
    print('Test of Vacuity postulate')
    print(vacuity(TEST_BELIEF_BASE, "s"))
    print('--------------------------------------')
    print('Test of Consistency postulate')
    print(consistency(TEST_BELIEF_BASE))
