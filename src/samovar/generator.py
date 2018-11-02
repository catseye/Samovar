# encoding: UTF-8

from itertools import permutations
import random
import re

from samovar.ast import Assert, Retract
from samovar.query import match_all
from samovar.terms import Term


# Python 2/3
try:
    xrange = xrange
except NameError:
    xrange = range


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
    def __init__(self, world, scenario, debug=False):
        self.world = world
        self.debug = debug
        self.state = set()  # set of things currently true about the world
        self.scenario = scenario
        for term in self.scenario.propositions:
            self.state.add(term)

    def generate_events(self, count):
        acceptable = False
        while not acceptable:
            if self.debug:
                self.debug_state()
            events = []
            for i in xrange(0, count):
                event = self.generate_event()
                if event is None:
                    break
                events.append(event)
            acceptable = self.events_meet_goal(events)
            if not acceptable:
                count *= 2
        return events

    def events_meet_goal(self, moves):
        matches = match_all(self.state, self.scenario.goal.exprs, {})
        return len(matches) > 0

    def generate_event(self):
        candidates = self.get_candidate_rules()
        if not candidates:
            return None
        rule, unifier = random.choice(candidates)
        self.update_state(unifier, rule)
        return Event(rule, unifier)

    def get_candidate_rules(self):
        candidates = []
        for rule in self.scenario.rules:
            for unifier in match_all(self.state, rule.pre.exprs, {}):
                candidates.append((rule, unifier))

        if self.debug:
            print("Candidate rules:")
            for rule, unifiers in candidates:
                print(rule.nu_format())
                print("->", unifiers)
            print("")

        return candidates

    def update_state(self, env, rule):
        for expr in rule.post.exprs:
            term = expr.term.subst(env)
            if isinstance(expr, Assert):
                self.state.add(term)
            elif isinstance(expr, Retract):
                self.state.remove(term)
        if self.debug:
            self.debug_state()

    def debug_state(self):
        print("Things now:")
        for term in self.things:
            print(u"  %s" % term)
        print("State now:")
        for term in self.state:
            print(u"  %s" % term)
        print("")
