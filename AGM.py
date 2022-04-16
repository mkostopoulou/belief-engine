from sympy import *


PROMPT = ">>> "
Belief_Set = []


### Connectives  
def Negation (frm):
    return ~(frm)

def Conjunction (frm1, frm2):
    return frm1 and frm2

def Disjunctoin (frm1, frm2):
    return frm1 or frm2

def Implication (frm1, frm2):
    frm1 = Negation(frm1)
    return frm1 or frm2 

def Bi_implication (frm1, frm2):
    imp1 = Implication(frm1, frm2)
    imp2 = Implication(frm2, frm2)
    return imp1 and imp2
    

### Check Subsets of a Belief (??)
def Belief_sub (frm):    
    return frm.atoms() 


### Gain New Information - Revision
def Revision (frm, Belief_Set):
    return Expansion(frm, Contraction(frm, Belief_Set))    


### Gain New Information - Contraction
def Contraction (frm, Belief_Set):
    if Negation(frm) in Belief_Set:
        Belief_Set.remove(Negation(frm))
    for i in Belief_sub(frm):
        if Negation(i) in Belief_Set:
            Belief_Set.remove(Negation(frm))
    return Belief_Set


### Gain New Information - Expansion 
def Expansion (frm, Belief_Set):
    if frm not in Belief_Set:
        Belief_Set.append(frm)
    return Belief_Set 


### Defining Beliefs 
def get_information ():
    print("Define a formula : ")
    prop = input(PROMPT)
    prop = prop.lower()
    frm = to_cnf(prop)
    return frm


### Updating Belife Set
def update_BS (Belief_Set):
    gain_inf = "Y"
    while gain_inf == "Y":
        inf = get_information()
        Belief_Set = Revision(inf, Belief_Set) 
        print("Do you want to add a new blief to the belief set? Y/N")
        # add order (??)
        gain_inf = input(PROMPT)
    return Belief_Set


Belief_Set = update_BS(Belief_Set)
print("Belief_Set update : ", Belief_Set)


































    
