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

# The identity function will probably be useful later...
ID      = lambda x: x

"""
BOOLEANS
"""

# First, the datatypes.
# λt. λf. t
TRUE    = lambda t: lambda f: t
# λt. λf. f
FALSE   = lambda t: lambda f: f

# Let's start with a basic if-then-else.
# λc. λt. λe. c t e
# (c)ond (t)then (e)lse
IF      = lambda c: lambda t: lambda e: c(t)(e)

# We should be able to build binary relations off of IF.
# λb. IF b FALSE TRUE
NEGB    = lambda b: IF(b)(FALSE)(TRUE)
# λb1. λb2. IF b1 b2 FALSE
ANDB    = lambda b1: lambda b2: IF(b1)(b2)(FALSE)
# λb1. λb2. IF b1 TRUE b2
ORB     = lambda b1: lambda b2: IF(b1)(TRUE)(b2)
# λb1. λb2. IF b1 (NEGB b2) b2
XORB    = lambda b1: lambda b2: IF(b1)(NEGB(b2))(b2)
# λb1. λb2. IF b1 b2 (NEGB b2)
EQB     = lambda b1: lambda b2: IF(b1)(b2)(NEGB(b2))

# Maybe let's do some tests?
def bool_tests():
    print("true:", TRUE(True)(False))
    print("false:", FALSE(True)(False))
    print("if true then true else false:", IF(TRUE)(TRUE)(FALSE)(True)(False))
    print("not false:", NEGB(FALSE)(True)(False))
    print("and true true:", ANDB(TRUE)(TRUE)(True)(False))
    print("eq true false:", EQB(TRUE)(FALSE)(True)(False))
    print("xor false true:", XORB(FALSE)(TRUE)(True)(False))

    # I think it's interesting to note that these operations depend not at
    #   all on what the "true evaulator" and "false evaluator" are, only
    #   that they are different!
    print("true' -> 'foo', false' -> 'bar'")
    print("or false' false':", ORB(FALSE)(FALSE)("foo")("bar"))
    print("eq true' true':", EQB(TRUE)(TRUE)("foo")("bar"))
# Yep, it works.
# bool_tests()

"""
NATURAL NUMBERS
"""

# Start with the inductive definitions, as usual.
# λz s. z
ZERO    = lambda z: lambda s: z
# λn z s. s (n z s)
SUCC    = lambda n: lambda z: lambda s: s(n(z)(s))

# Maybe let's define some small numbers, just for funsies.
ONE     = SUCC(ZERO)
TWO     = SUCC(ONE)
THREE   = SUCC(TWO)
FOUR    = SUCC(THREE)
FIVE    = SUCC(FOUR)
SIX     = SUCC(FIVE)
SEVEN   = SUCC(SIX)

# I think the next step is to define relations on numbers, right?
# Let's see...

# We could probably make a equals-to-zero function easily.
# Need a helper function to always return false...
# λx. FALSE
FALSE1  = lambda x: FALSE
# Then we can split numbers into its cases.
# λn. n TRUE FALSE1
EQZ     = lambda n: n(TRUE)(FALSE1)
# λn. NEGB (EQZ n)
NEQZ    = lambda n: NEGB(EQZ(n))

# To implement integer equality, I think we need the predecessor function.
# We might write the equality definition recursively as
"""
Fixpoint eq (m n : nat) : bool :=
match m, n with
| O, O       => true
| S m', S n' => eq m' n'
| _, _       => false
"""

# If we think about how numbers are defined, n is just z with s applied n times.
# So the predecessor function should somehow generate a number that is z with
#   s applied n-1 times.
# n takes s and z as arguments. We probably need to define some s' and z' such
#   that when s' is applied to z' n times, it's somehow equivalent to s being
#   applied to z n-1 times.
# I've seen a variation of the Church encoding before that essentially keeps a
#   pair (n-1, n) for every natural number. Predecessor would be easy in that
#   case. But the main idea is that in the first application of successor,
#   i.e. (0, 0) -> (0, 1), the first term somehow ignores the application.
# So here's the plan:
# - We have a datatype that boxes a number, which applies a function when
#     passed to it.
# - We transform zero to a similar box, except it ignores the function passed
#     to it. Let's call it a wrapper, or maybe "fake box".
# - We define a box-function-applier: when a function is passed in, we apply
#     it to the value inside the box.
# - On the first SUCC application, the fake box doesn't actually apply it, and
#     ZERO is left inside the box.
# - On subsequent evaluations, SUCC is successfully applied through the box.

# λx b. b x
BOX     = lambda x: lambda b: b(x) # Not actually used, but for understanding.
# λx w. x
WRAP    = lambda x: lambda w: x
# λg box b. b (box g)
BOX_APP = lambda g: lambda box: lambda b: b(box(g))

# In the end, we end up with a box containing the actual value. So we just
#   apply the identity function to get it out.
# λn z s. n (WRAP z) (BOX_APP s) ID
PRED    = lambda n: lambda z: lambda s: n(WRAP(z))(BOX_APP(s))(ID)

# We can step through the first two applications.
# BOX_APP(s)(WRAP(z)) = λb. b(WRAP(z)(s))
#                     = λb. b(z)
#                     = BOX(z)
#
# BOX_APP(s)(BOX(z))  = λb. b(BOX(z)(s))
#                     = λb. b(s(z))
#                     = BOX(s(z))

# Let's test it out...
def pred_tests():
    # Let's start off with a successor function...
    s = lambda x: x+1

    print("pred(3):", PRED(THREE)(0)(s))
    print("pred(7):", PRED(SEVEN)(0)(s))
    print("pred(1):", PRED(ONE)(0)(s))
    print("pred(0):", PRED(ZERO)(0)(s))
pred_tests()
# Wow!