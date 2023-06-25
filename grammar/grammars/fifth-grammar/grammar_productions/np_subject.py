### Read: https://www.nltk.org/book/ch09.html
grammar = """% start S
# ###################
# Grammar Productions
# ###################
# S expansion productions
S[AGR=?a] -> NP[AGR=?a] VP[AGR=?a, MOOD=i]
# VP expansion productions
VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='intr']
VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='tr'] NP
VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='di'] NP1 A NP2
# NP1 expansion productions
NP1[AGR=?a] -> NP[AGR=?a] 
# NP2 expansion productions
NP2[AGR=?a] -> NP[AGR=?a]
# A expansion productions
A -> 'a'
# NP expansion productions
NP[AGR=?a] -> D[AGR=?a] N[AGR=?a]
# ###################
# Lexical Productions
# ###################
"""