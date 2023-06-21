"""
Regex Lister

Parses a simple regex expression then lists all words that match. Not
much error handling, so play nice :(

When listing words, has:
- * act as ?
- + act as {1,2}
- {,j} act as {j})?
- {i,j} act as {i}
"""

class Token:
    __match_args__ = ("x",)
    def __init__(self, x: str | None = None):
        self.x = x
    def is_num(self):
        return len(self.x) == 1 and ord('0') <= ord(self.x) <= ord('9')
    def __eq__(self, other):
        if isinstance(other, Token):
            return self.x == other.x
        return NotImplemented
    def __repr__(self):
        return f"Token({self.x})"

class RegExTokenizer:
    def __init__(self, s: str):
        self.s = s
        self.pos = 0

    def next(self):
        if self.pos >= len(self.s):
            return

        if self.s[self.pos] == "\\":
            self.pos += 2
            return Token(self.s[self.pos-2:self.pos])
        else:
            self.pos += 1
            return Token(self.s[self.pos-1])

    def peek(self):
        if self.pos >= len(self.s):
            return

        if self.s[self.pos] == "\\":
            return Token(self.s[self.pos:self.pos+2])
        else:
            return Token(self.s[self.pos])

class Node:
    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{v}' for _,v in vars(self).items())})"
class Char(Node):
    __match_args__ = ("c",)
    def __init__(self, c: Token):
        self.c = c
    def __repr__(self):
        return self.c.x

class Unary(Node):
    __match_args__ = ("a",)
    def __init__(self, a: Node):
        self.a = a
class Star(Unary): pass
class Plus(Unary): pass
class Option(Unary): pass

class Binary(Node):
    __match_args__ = ("a", "b")
    def __init__(self, a: Node, b: Node):
        self.a = a
        self.b = b
class And(Binary): pass
class Or(Binary): pass

class Count(Node):
    __match_args__ = ("a", "m", "n")
    def __init__(self, a: Node, m: int, n: int):
        self.a = a
        self.m = m
        self.n = n

class Parser:
    def __init__(self, s: str):
        self.stream = RegExTokenizer(s)

    def read(self, c: str):
        d = self.stream.next()
        if d == Token(c):
            pass
        else:
            raise Exception(f"Expected {c}, got {d.x}")

    def parse(self):
        return self.parse_expr()

    def parse_expr(self, expect: Token = Token()) -> Node:
        if self.stream.peek() is None:
            return
        if self.stream.peek() == expect:
            return
    
        l = self.parse_word(expect)

        match self.stream.peek():
            case Token("|"):
                self.read("|")
                r = self.parse_expr(expect)
                if r is None:
                    return l
                else:
                    return Or(l, r)

        return l

    def parse_word(self, expect: Token = Token()) -> Node:
        l = None

        if self.stream.peek() is None:
            return
        if self.stream.peek() == expect:
            return
        
        match self.stream.peek():
            case Token("("):
                self.read("(")
                l = self.parse_expr(Token(")"))
                self.read(")")
            case Token("["):
                self.read("[")
                l = self.parse_bracket()
            case Token("|"):
                return
            case _:
                l = Char(self.stream.next())
        
        match self.stream.peek():
            case Token("*"):
                self.read("*")
                l = Star(l)
            case Token("+"):
                self.read("+")
                l = Plus(l)
            case Token("?"):
                self.read("?")
                l = Option(l)
            case Token("{"):
                self.read("{")
                m = self.parse_num()
                n = m
                if self.stream.peek() == Token(","):
                    self.read(",")
                    n = self.parse_num()
                self.read("}")
                l = Count(l, m, n)

        r = self.parse_word(expect)
        if r is None:
            return l
        else:
            return And(l, r)

    def parse_bracket(self) -> Node:
        match self.stream.peek():
            case Token("]"):
                self.stream.next()
                return
            case _:
                c = Char(self.stream.next())
                n = self.parse_bracket()

                if n is None:
                    return c
                else:
                    return Or(c, n)

    def parse_num(self) -> int:
        n = 0
        while self.stream.peek().is_num():
            n = 10 * n + int(self.stream.next().x)
        return n

def generate(node: Node) -> list[str]:
    match node:
        case Char(c):
            return [c.x]
        case Star(a):
            return [""] + generate(a)
        case Plus(a):
            g = generate(a)
            return g + [s*2 for s in g]
        case Option(a):
            return [""] + generate(a)
        case And(a, b):
            return [s1+s2 for s1 in generate(a) for s2 in generate(b)]
        case Or(a, b):
            return generate(a) + generate(b)
        case Count(a, m, n):
            if m == 0:
                if n == 0:
                    return [""]
                else:
                    return [""] + [s*n for s in generate(a)]
            else:
                return [s*m for s in generate(a)]
        case _:
            return []

for s in generate(Parser(input()).parse()):
    print(s)
                
                
    



