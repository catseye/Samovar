# encoding: UTF-8

import re


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
        if self.scan_pattern(ur'\~|→|=|¬|∧|∨', 'operator'):
            return
        # TODO: not sure about the ? overloading (here and in punct).  should be okay though?
        if self.scan_pattern(r'\?[a-zA-Z_]+', 'qmark'):
            return
        if self.scan_pattern(r'\,|\.|\?|\!|\"' + r"|\'", 'punct'):
            return
        if self.scan_pattern(r'\(|\)|\{|\}|\[|\]', 'bracket'):
            return
        if self.scan_pattern(r'[a-zA-Z_]+', 'word'):
            return
        if self.scan_pattern(ur'[αβγδεζθικλμνξοπρστυφχψω]', 'variable'):
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
