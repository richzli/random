"""
church.py

(20220308)
In class today, we learned about Church encodings, where we essentially define
  constructs in terms of their operations, rather than their values.

For example, Boolean values are defined as either true, or false.

Inductive bool :=
| true
| false.

So, if we have some mystical "true evaluator" and "false evaluator", then we
  can define booleans as

λt. λf. t                      (true)
λt. λf. f                      (false)

We can do a similar thing for the natural numbers, using the Peano construction.

Inductive nat :=
| O
| S (n : nat).

We have two operations, the "zero" and the "successor". So,

    λz. λs. z                  (0)
λn. λz. λs. s (n z s)          (S n)

These are the two definitions I remember most clearly from class. But I want
  to try to derive stuff from these two definitions, by myself. I think it'll
  be a good exercise.
"""

"""
BOOLEANS
"""

# First, the datatypes.
# λt. λf. t
TRUE  = lambda t: lambda f: t
# λt. λf. f
FALSE = lambda t: lambda f: f

# Let's start with a basic if-then-else.
# λc. λt. λe. c t e
# (c)ond (t)then (e)lse
IF    = lambda c: lambda t: lambda e: c(t)(e)

# We should be able to build binary relations off of IF.
# λb. IF b FALSE TRUE
NEGB  = lambda b: IF(b)(FALSE)(TRUE)
# λb1. λb2. IF b1 b2 FALSE
ANDB  = lambda b1: lambda b2: IF(b1)(b2)(FALSE)
# λb1. λb2. IF b1 TRUE b2
ORB   = lambda b1: lambda b2: IF(b1)(TRUE)(b2)
# λb1. λb2. IF b1 (NEGB b2) b2
XORB  = lambda b1: lambda b2: IF(b1)(NEGB(b2))(b2)
# λb1. λb2. IF b1 b2 (NEGB b2)
EQB   = lambda b1: lambda b2: IF(b1)(b2)(NEGB(b2))

# Maybe let's do some tests?
def bool_tests_1():
    print("true:", TRUE(True)(False))
    print("false:", FALSE(True)(False))
    print("if true then true else false:", IF(TRUE)(TRUE)(FALSE)(True)(False))
    print("not false:", NEGB(FALSE)(True)(False))
    print("and true true:", ANDB(TRUE)(TRUE)(True)(False))
    print("eq true false:", EQB(TRUE)(FALSE)(True)(False))
    print("xor false true:", XORB(FALSE)(TRUE)(True)(False))
# Yep, it works.
# bool_tests_1()

"""
NATURAL NUMBERS
"""