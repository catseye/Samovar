# encoding: UTF-8


# Python 2/3
try:
    unicode = unicode
except NameError:
    unicode = str


import re


GREEK = [
    (u'?alpha', u'α'),
    (u'?beta', u'β'),
    (u'?gamma', u'γ'),
    (u'?delta', u'δ'),
    (u'?epsilon', u'ε'),
    (u'?zeta', u'ζ'),
    (u'?theta', u'θ'),
    (u'?iota', u'ι'),
    (u'?kappa', u'κ'),
    (u'?lambda', u'λ'),
    (u'?mu', u'μ'),
    (u'?nu', u'ν'),
    (u'?xi', u'ξ'),
    (u'?omicron', u'ο'),
    (u'?pi', u'π'),
    (u'?rho', u'ρ'),
    (u'?sigma', u'σ'),
    (u'?tau', u'τ'),
    (u'?upsilon', u'υ'),
    (u'?phi', u'φ'),
    (u'?chi', u'χ'),
    (u'?psi', u'ψ'),
    (u'?omega', u'ω'),
]


class Scanner(object):
    def __init__(self, text):
        self.text = unicode(text)
        self.token = None
        self.type = None
        self.scan()

    def near_text(self, length=10):
        if len(self.text) < length:
            return self.text
        return self.text[:length]

    def scan_pattern(self, pattern, type, token_group=1, rest_group=2):
        pattern = r'^(' + pattern + r')(.*?)$'
        match = re.match(pattern, self.text, re.DOTALL)
        if not match:
            return False
        else:
            self.type = type
            self.token = match.group(token_group)
            self.text = match.group(rest_group)
            return True

    def scan(self):
        self.scan_pattern(r'[ \t\n\r]*', 'whitespace')
        while self.scan_pattern(r'\/\/.*?[\n\r]', 'comment'):
            self.scan_pattern(r'[ \t\n\r]*', 'whitespace')
        if not self.text:
            self.token = None
            self.type = 'EOF'
            return
        if self.scan_pattern(u'\\~|→|=|¬|∧|∨', 'operator'):
            return
        # TODO: not sure about the ? overloading (here and in punct).  should be okay though?
        if self.scan_pattern(r'\?[a-zA-Z_]+', 'variable'):
            return
        if self.scan_pattern(r'\,|\.|\;|\:|\?|\!|\"', 'punct'):
            return
        if self.scan_pattern(r'\(|\)|\{|\}|\[|\]', 'bracket'):
            return
        if self.scan_pattern(r"[a-zA-Z_]['a-zA-Z0-9_-]*", 'word'):
            return
        if self.scan_pattern(u'[αβγδεζθικλμνξοπρστυφχψω]', 'variable'):
            for varname, letter in GREEK:
                if letter == self.token:
                    self.token = varname
                    break
            assert self.token.startswith('?'), repr(self.token)
            return
        if self.scan_pattern(r'.', 'unknown character'):
            return
        else:
            raise AssertionError("this should never happen, self.text=(%s)" % self.text)

    def expect(self, token):
        if self.token == token:
            self.scan()
        else:
            raise SyntaxError(u"Expected '%s', but found '%s' (near '%s')" %
                              (token, self.token, self.near_text()))

    def on(self, *tokens):
        return self.token in tokens

    def on_type(self, *types):
        return self.type in types

    def check_type(self, *types):
        if not self.on_type(*types):
            raise SyntaxError(u"Expected %s, but found %s ('%s') (near '%s')" %
                              (types, self.type, self.token, self.near_text()))

    def consume(self, *tokens):
        if self.token in tokens:
            self.scan()
            return True
        else:
            return False
