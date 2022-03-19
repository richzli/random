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
NEQB    = XORB
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
# bool_tests()
# Yep, it works.

"""
NATURAL NUMBERS
"""

# Start with the inductive definitions, as usual.
# λs z. z
ZERO    = lambda s: lambda z: z
# λn s z. s (n s z)
SUCC    = lambda n: lambda s: lambda z: s(n(s)(z))

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
# λn. n FALSE1 TRUE
EQZ     = lambda n: n(FALSE1)(TRUE)
# λn. NEGB (EQZ n)
NEQZ    = lambda n: NEGB(EQZ(n))

# To implement integer equality, I think we need the predecessor function.
# We might write the equality definition recursively as
"""
Fixpoint eq (m n : nat) : bool :=
match m, n with
| O, O       => true
| S m', S n' => eq m' n'
| _, _       => false.
"""
# Note that m' = m-1 and n' = n-1.

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
# I like this "the first application is ignored" idea. Here's the plan:
# - We have a datatype that boxes a number, which applies a function when
#     passed to it.
# - We wrap zero in a box, except it ignores the function passed to it. Let's
#     call it a wrapper, or maybe "fake box".
# - We define a box-function-applier: when a function is passed in, we apply
#     it to the value inside the box. We do this by using the original box to
#     apply the function, then enclosing it in another box.
# - On the first successor application, the fake box doesn't actually apply it,
#     and zero is left inside the resultant box.
# - On subsequent evaluations, the successor is successfully applied through
#     the box.

# λx b. b x
BOX     = lambda x: lambda b: b(x)
# λx w. x
WRAP    = lambda x: lambda w: x
# λf bx. BOX (bx f)
APP     = lambda f: lambda bx: BOX(bx(f))

# In the end, we end up with a box containing the actual value. So we just
#   apply the identity function to get it out.
# λn s z. n (APP s) (WRAP z) ID
PRED    = lambda n: lambda s: lambda z: n(APP(s))(WRAP(z))(ID)

# We can step through the first two applications.
# APP s (WRAP z)  = BOX (WRAP z s)
#                 = BOX z
#
# APP s (BOX z)   = BOX (BOX z s)
#                 = BOX (s z)

# Let's test it out...
def pred_tests():
    # Let's use a "real" successor function...
    s = lambda x: x+1

    print("pred 3:", PRED(THREE)(s)(0))
    print("pred 7:", PRED(SEVEN)(s)(0))
    print("pred 1:", PRED(ONE)(s)(0))
    print("pred 0:", PRED(ZERO)(s)(0))
# pred_tests()
# Wow!

# Let's try defining equality now.
# Obviously, we can't define lambda expressions recursively, so the earlier
#   equality definition doesn't really work.
# But something like less-than-or-equals should be easy enough...
# λm n. EQZ (n PRED m)
LEQ     = lambda m: lambda n: EQZ(n(PRED)(m))
# And equality should follow immediately.
# λm n. ANDB (LEQN m n) (LEQN n m)
EQN     = lambda m: lambda n: ANDB(LEQ(m)(n))(LEQ(n)(m))

# Maybe some other arithmetic comparisons for fun?
# λm n. NEGB (EQN m n)
NEQN    = lambda m: lambda n: NEGB(EQN(m)(n))
# λm n. LEQ n m
GEQ     = lambda m: lambda n: LEQ(n)(m)
# λm n. ANDB (LEQ m n) (NEQN m n)
LT      = lambda m: lambda n: ANDB(LEQ(m)(n))(NEQN(m)(n))
# λm n. ANDB (GEQ m n) (NEQN m n)
GT      = lambda m: lambda n: ANDB(GEQ(m)(n))(NEQN(m)(n))

def comp_tests():
    print("leq 1 2:", LEQ(ONE)(TWO)(True)(False))
    print("leq 2 1:", LEQ(TWO)(ONE)(True)(False))
    print("eq 3 3:", EQN(THREE)(THREE)(True)(False))
    print("neq 5 4:", NEQN(FIVE)(FOUR)(True)(False))
    print("gt 3 3:", GT(THREE)(THREE)(True)(False))
    print("lt 1 7:", LT(ONE)(SEVEN)(True)(False))
# comp_tests()

# Let's create numbers greater than seven by creating some basic
#   arithmetic operations.
# Remember again that the natural numbers are defined by applying a
#   successor some number of times to a zero.

# Addition is just applying s to m, n times.
# λm n s z. n s (m s z)
ADD     = lambda m: lambda n: lambda s: lambda z: n(s)(m(s)(z))
# I basically already defined subtraction in LEQ, but just apply PRED n times.
# λm n s z. n PRED m
SUB     = lambda m: lambda n: n(PRED)(m)
# Multiplication is just adding m to 0, n times.
# (At this point I realize that my previous notation of putting z before
#   s makes this case kind of annoying, so off I go to make everything λs z.)
# λm n s z. n (m s) z
MUL     = lambda m: lambda n: lambda s: lambda z: n(m(s))(z)

# Exponentiation is m reapplied on itself, n times.
# λm n. n m
EXP     = lambda m: lambda n: n(m)
# Actually, the mechanics of EXP are really wonky. Note that the natural
#   numbers N are defined under the relation (N->N)->N->N (s->z->N).
#   But here, n seems to accept an N as the first argument! Also, when we
#   eventually evaluate with n(m)(inc)(0), the grouping suggests that inc is
#   actually supposed to represent a zero value! What gives?
# Let's do a beta reduction on n(m). We see that we get λz. m(m(...m(z)...)),
#   which seems correct, ish? m is now recursively applied on itself, so let's
#   just consider the case where n = 2 = λs z. s(s(z)) => we have λz. m(m(z)).
#   Higher-order cases should follow the same logic.
# Let's reduce. We're left with
# 
#       λz. m(m(z))                                                   =>
#       λz. (λs1 z1. s1(...s1(z1)...))((λs2 z2. s2(...s2(z2)...)) z)  =>
#       λz. (λs1 z1. s1(...s1(z1)...))(λz2 z(...z(z2)...))            =>
#       λz. (λz1. (λz2. z(...z(z2)...))(...(z1)...))                  =>
#       λz. (λz1. z(z(...z(z(z1))...))).
#
# Here we can see the squaring at work: the first m uses the second m as an
#   applicator. z2 only appears once in each (λz2. z(...z(z2)...)) term, so
#   the z's get stacked m^2 times. Obviously, for higher exponents, this
#   process would repeat, and we would get higher powers.
# Also note that z has managed to work its way back into being applied in the
#   chain during the process! This is because z ends up being used as the first
#   argument for m, which means it gets used as the successor for m.
# Anyways, all this feels like terrible abuse of the lambda calculus, but this
#   is the stuff you get to do when you're not constrained by a type system,
#   I guess.

# Division is harder, so I'll leave that for later.

def arith_tests():
    s = lambda x: x + 1

    print("add 3 4:", ADD(THREE)(FOUR)(s)(0))
    print("add 7 (add 6 5):", ADD(SEVEN)(ADD(SIX)(FIVE))(s)(0))
    print("sub 7 2:", SUB(SEVEN)(TWO)(s)(0))
    print("mul 6 7:", MUL(SIX)(SEVEN)(s)(0))
    print("exp 3 4:", EXP(THREE)(FOUR)(s)(0))
    print("sub (exp 2 4) 3:", SUB(EXP(TWO)(FOUR))(THREE)(s)(0))

    # And just as a reminder that the operations work regardless
    #   of what the sucessor and zero actually are:
    s1 = lambda x: x * 2
    print("z1=1, s1=(x => x*2)")
    print("add 3 4:", ADD(THREE)(FOUR)(s1)(1))
    print("sub 7 2:", SUB(SEVEN)(TWO)(s1)(1))
    print("mul 6 7:", MUL(SIX)(SEVEN)(s1)(1))
    s2 = lambda x: x + '#'
    print("z2='', s2=(x => x+'#')")
    print("add 3 4:", ADD(THREE)(FOUR)(s2)(''))
    print("sub 7 2:", SUB(SEVEN)(TWO)(s2)(''))
    print("mul 6 2:", MUL(SIX)(TWO)(s2)(''))
# arith_tests()

"""
PAIRS, LISTS, AND MAPS
"""

# A pair takes two values, and takes a function that selects either the
#   first or the second argument.
# λf s p. p f s
PAIR    = lambda f: lambda s: lambda p: p(f)(s)
# We need to select either the first or the second argument... that's exactly
#   the definition of TRUE/FALSE!
FST     = lambda p: p(TRUE)
SND     = lambda p: p(FALSE)

# Lists are just pairs, except the second value is a list.
"""
Inductive list :=
| nil
| cons (h : Any) (t : list).
"""
# λc n. n
# λh t c n. c h (t c n)
NIL     = lambda c: lambda n: n
CONS    = lambda h: lambda t: lambda c: lambda n: c(h)(t(c)(n))

# HEAD is just the first element of the pair. Note that the calling convention
#   is a little weird - we need to give an second argument for nil,
#   even though it's not used. It doesn't really matter what you put there.
HEAD    = lambda l: FST(l)(NIL)
# TAIL is a little more involved. We need to ignore the *last* application of
#   cons, rather than the first, like we saw in PRED.
TAIL    = lambda l: l # ...still trying to figure this one out.

def list_tests():
    # Get some stuff out of the way...
    z = 0
    s = lambda x: x + 1
    nil = []
    cons = lambda h: lambda t: [h] + t

    pair12 = PAIR(ONE)(TWO)
    
    print("fst (1 2):", FST(pair12)(s)(z))
    print("snd (1 2):", SND(pair12)(s)(z))
    print("snd (fst ((1 2) 3)):", SND(FST(PAIR(PAIR(ONE)(TWO))(THREE)))(s)(z))

    # Here's a function to transform a Church-encoded integer list into
    #   a normal Python integer list.
    tf = lambda l: list(map(lambda n: n(s)(z), l(cons)(nil)))
    
    list123 = CONS(ONE)(CONS(TWO)(CONS(THREE)(NIL)))

    print("[1 2 3]:", tf(list123))
    print("head [1 2 3]:", HEAD(list123)(s)(z))
    print("tail [1 2 3]:", tf(TAIL(list123)))
    print("head (tail (tail [1 2 3])):", HEAD(TAIL(TAIL(list123)))(s)(z))
list_tests()