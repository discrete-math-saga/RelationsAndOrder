from relations import Relation
# Quiz 1 for 2024
R = Relation("R", Relation.converter({("a","a"),("a","b"),("b","d"),("c","a")}))
S = Relation("S",Relation.converter({("a","c"),("a","d"),("b","c")}))
A = Relation.multiply(S, R)
print(A)
B = Relation.multiply(R, R)
print(B)
C = Relation.multiply(S, S)
print(C)