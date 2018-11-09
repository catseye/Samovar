# encoding: UTF-8

from copy import deepcopy
from pprint import pprint
import random


# Python 2/3
try:
    unicode = unicode
except NameError:
    unicode = str


class AST(object):
    def __init__(self, **kwargs):
        self.attrs = kwargs

    def __repr__(self):
        return "%s(%s)" % (
            self.__class__.__name__,
            ', '.join(['%s=%r' % (k, v) for k, v in self.attrs.iteritems()])
        )

    def __getattr__(self, name):
        if name in self.attrs:
            return self.attrs[name]
        raise AttributeError(name)


class World(AST):
    pass


def join_sentence_parts(parts):
    acc = u''
    quote_open = False
    for part in parts:
        last = '' if not acc else acc[-1]
        if last == '':
            acc += part
        elif last == '"' and quote_open:
            acc += part
        elif last == '"' and not quote_open:
            if part in (u'.', u',', u'!', u'?'):
                acc += part
            else:
                acc += ' ' + part
        elif last == ',' and part == u'"' and not quote_open:
            acc += ' ' + part
        elif last in (u'.', u',', u'!', u'?', u"'") and part == u'"' and not quote_open:
            acc += part
        elif part in (u'.', u',', u'!', u'?', u"'", u'"'):
            acc += part
        else:
            acc += u' ' + part
        if part == '"':
            quote_open = not quote_open
    return acc


class Rule(AST):
    def nu_format(self):
        return self.pre.format() + u" " + u' '.join([unicode(t) for t in self.words]) + u" " + self.post.format()

    def format(self, unifier):
        return join_sentence_parts([unicode(t.subst(unifier)) for t in self.words])

    def to_json(self):
        return join_sentence_parts([unicode(t) for t in self.words])


class Scenario(AST):
    pass


class Cond(AST):
    def __str__(self):
        return u'[%s]' % ','.join([unicode(e) for e in self.exprs])

    def format(self):
        return u'[%s]' % ','.join([e.format() for e in self.exprs])


class Assert(AST):
    def format(self):
        return u'%s' % self.term


class Retract(AST):
    def format(self):
        return u'~%s' % self.term
