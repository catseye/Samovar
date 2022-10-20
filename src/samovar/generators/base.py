# encoding: UTF-8

# Python 2/3
try:
    xrange = xrange
except NameError:
    xrange = range

# Python 2/3
try:
    unicode = unicode
except NameError:
    unicode = str


class Event(object):
    def __init__(self, rule, unifier):
        self.rule = rule
        self.unifier = unifier

    def to_json(self):
        u = dict([(unicode(k), unicode(v)) for k, v in self.unifier.items()])
        return [self.rule.to_json(), u]

    def __str__(self):
        return self.rule.format(self.unifier)


class BaseGenerator(object):
    pass
