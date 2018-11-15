# encoding: UTF-8

from collections import namedtuple


# Python 2/3
try:
    unicode = unicode
except NameError:
    unicode = str


World = namedtuple('World', ['scenarios'])
Rule = namedtuple('Rule', ['pre', 'words', 'post'])
Scenario = namedtuple('Scenario', ['name', 'propositions', 'rules', 'goal'])
Cond = namedtuple('Cond', ['exprs', 'bindings'])
Assert = namedtuple('Assert', ['term'])
Retract = namedtuple('Retract', ['term'])


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


def format_rule(rule, unifier):
    return join_sentence_parts([unicode(t.subst(unifier)) for t in rule.words])


def rule_to_json(rule):
    return join_sentence_parts([unicode(t) for t in rule.words])
