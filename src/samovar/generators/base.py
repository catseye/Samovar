# encoding: UTF-8

import sys

from samovar.ast import Assert, Retract


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
    def __init__(self, world, scenario, **kwargs):
        self.world = world
        self.scenario = scenario

    def goal_is_met(self, state):
        matches = state.match_all(self.scenario.goal.exprs, self.scenario.goal.bindings)
        return len(matches) > 0

    def get_candidate_rules(self, state):
        candidates = []
        for rule in self.scenario.rules:
            for unifier in state.match_all(rule.pre.exprs, rule.pre.bindings):
                candidates.append((rule, unifier))

        if self.verbosity >= 3:
            sys.stderr.write("Candidate rules:\n")
            for rule, unifiers in candidates:
                sys.stderr.write("-> " + rule.to_json() + "\n")
                sys.stderr.write("---> {}\n".format(unifiers))
            sys.stderr.write("")

        return candidates

    def update_state(self, state, env, rule):
        for expr in rule.post.exprs:
            term = expr.term.subst(env)
            if isinstance(expr, Assert):
                state.add(term)
            elif isinstance(expr, Retract):
                state.remove(term)

    def debug_state(self, state, label):
        sys.stderr.write(":::: {} State [\n".format(label))
        for term in sorted(state.contents):
            sys.stderr.write("::::   {}\n".format(term))
        sys.stderr.write(":::: ]\n")
