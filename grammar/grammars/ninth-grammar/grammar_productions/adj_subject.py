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
VP[AGR=?a, MOOD=?m] -> NEG V[AGR=?a, MOOD=?m, SUBCAT='intr']
VP[AGR=?a, MOOD=?m] -> NEG V[AGR=?a, MOOD=?m, SUBCAT='tr'] NP
# NP expansion productions
NP[AGR=?a] -> D[AGR=?a] N[AGR=?a] A[AGR=?a]
NP[AGR=?a] -> D[AGR=?a] A[AGR=?a] N[AGR=?a]
# ###################
# Lexical Productions
# ###################
AA -> 'a'
NEG -> 'no'
"""