# encoding: UTF-8

import sys

from samovar.ast import Assert, Retract
from samovar.query import match_all


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


class Generator(object):
    def __init__(self, random, world, scenario, verbosity=0):
        self.random = random
        self.world = world
        self.verbosity = verbosity
        self.scenario = scenario
        self.reset_state()

    def reset_state(self):
        self.state = set()  # set of things currently true about the world
        for term in self.scenario.propositions:
            self.state.add(term)

    def generate_events(self, count, max_count, lengthen_factor):
        acceptable = False
        while not acceptable:
            if self.verbosity >= 1:
                sys.stderr.write("Generating {} events\n".format(count))
            self.reset_state()
            if self.verbosity >= 2:
                self.debug_state("Initial")
            events = []
            for i in xrange(0, count):
                event = self.generate_event()
                if event is None:
                    break
                events.append(event)
            if self.verbosity >= 2:
                self.debug_state("Final")
            acceptable = self.events_meet_goal(events)
            if not acceptable:
                count = int(float(count) * lengthen_factor)
            if count > max_count:
                raise ValueError("{}: count exceeds maximum".format(self.scenario.name))
        return events

    def events_meet_goal(self, moves):
        matches = match_all(self.state, self.scenario.goal.exprs, self.scenario.goal.bindings)
        return len(matches) > 0

    def generate_event(self):
        candidates = self.get_candidate_rules()
        if not candidates:
            return None
        rule, unifier = self.random.choice(candidates)
        self.update_state(unifier, rule)
        return Event(rule, unifier)

    def get_candidate_rules(self):
        candidates = []
        for rule in self.scenario.rules:
            for unifier in match_all(self.state, rule.pre.exprs, rule.pre.bindings):
                candidates.append((rule, unifier))

        if self.verbosity >= 3:
            sys.stderr.write("Candidate rules:\n")
            for rule, unifiers in candidates:
                sys.stderr.write("-> " + rule.to_json() + "\n")
                sys.stderr.write("---> {}\n".format(unifiers))
            sys.stderr.write("")

        return candidates

    def update_state(self, env, rule):
        for expr in rule.post.exprs:
            term = expr.term.subst(env)
            if isinstance(expr, Assert):
                self.state.add(term)
            elif isinstance(expr, Retract):
                self.state.remove(term)
        if self.verbosity >= 3:
            self.debug_state("Intermediate")

    def debug_state(self, label):
        sys.stderr.write(":::: {} State [\n".format(label))
        for term in sorted(self.state):
            sys.stderr.write("::::   {}\n".format(term))
        sys.stderr.write(":::: ]\n")
