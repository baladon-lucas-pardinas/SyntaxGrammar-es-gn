### Read: https://www.nltk.org/book/ch09.html
grammar = """% start S
# ###################
# Grammar Productions
# ###################
# S expansion productions
S[AGR=?a] -> NP[AGR=?a] VP[AGR=?a, MOOD=i]
S[AGR=?a] -> NP[AGR=?a] VP[AGR=?a, MOOD=i] PP
S[AGR=?a] -> P[AGR=?a, CASE=n] VP[AGR=?a, MOOD=i]
S[AGR=?a] -> P[AGR=?a, CASE=n] VP[AGR=?a, MOOD=i] PP
# For extra Ancora matching
S[AGR=?a] -> VP[AGR=?a, MOOD=i]
S[AGR=?a] -> VP[AGR=?a, MOOD=i] PP
S[AGR=?a] -> NP[AGR=?a]
S -> PP
# VP expansion productions
VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='intr']
VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='tr'] NP
VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='di'] NP PPA
VP[AGR=?a, MOOD=?m] -> NEG V[AGR=?a, MOOD=?m, SUBCAT='intr']
VP[AGR=?a, MOOD=?m] -> NEG V[AGR=?a, MOOD=?m, SUBCAT='tr'] NP
VP[AGR=?a, MOOD=?m] -> NEG V[AGR=?a, MOOD=?m, SUBCAT='di'] NP PPA
# PP expansion productions
PP -> PR NP
# PPA expansion productions
PPA[AGR=?a] -> AA NP[AGR=?a]
# NP expansion productions
NP[AGR=?a] -> D[AGR=?a] N[AGR=?a]
NP[AGR=?a] -> D[AGR=?a] N[AGR=?a] A[AGR=?a]
NP[AGR=?a] -> D[AGR=?a] A[AGR=?a] N[AGR=?a]
# Lexical Productions
AA -> 'a'
NEG -> 'no'
"""