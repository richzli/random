from z3 import *

a, b, c, d = Ints("a b c d")

solve(
    0 <= a, a < 4,
    0 <= b, b < 4,
    0 <= c, c < 4,
    0 <= d, d < 4,
    ( a +     c + d + 3 ) % 4 == 0,
    ( a + b +     d + 2 ) % 4 == 0,
    (     b + c + d + 2 ) % 4 == 0,
    ( a +         d + 3 ) % 4 == 0
)