# encoding: UTF-8

from copy import deepcopy
from pprint import pprint
import random


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


class Rule(AST):
    def nu_format(self):
        return self.pre.format() + u" " + u' '.join([unicode(t) for t in self.terms]) + u" " + self.post.format()

    def format(self, unifier, functions):
        acc = u''
        for t in self.terms:

            t = t.subst(unifier)

            # now resolve functions.  NOTE: this is a terrible hacky just-for-now implementation.  TODO: better it.
            for f in functions:
                if t == f.sign:
                    t = f.result
                    break

            s = unicode(t)
            if (acc == u'') or (s in (u'.', u',', u'!', u'"', u"'")):
                acc += s
            else:
                acc += u' ' + s
        return acc


class Function(AST):
    pass


class Situation(AST):
    pass


class Cond(AST):
    def __str__(self):
        return u'[%s]' % ','.join([unicode(e) for e in self.exprs])

    def format(self):
        return u'[%s]' % ','.join([e.format() for e in self.exprs])

    def eval(self, unifier, state):
        for expr in self.exprs:
            term = expr.term.subst(unifier)
            if isinstance(expr, Assert):
                if term not in state:
                    return False
            if isinstance(expr, Retract):
                if term in state:
                    return False
        return True


class Assert(AST):
    def format(self):
        return u'%s' % self.term


class Retract(AST):
    def format(self):
        return u'~%s' % self.term
