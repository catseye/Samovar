# encoding: UTF-8

import sys

from samovar.ast import Assert, Retract
from samovar.database import Database

from .base import xrange, Event, BaseGenerator


class RandomGenerator(BaseGenerator):
    def __init__(self, world, scenario, verbosity=0, sorted_search=True, randomness=None):
        self.world = world
        self.scenario = scenario
        self.verbosity = verbosity
        self.sorted_search = sorted_search
        self.random = randomness
        self.reset_state()

    def reset_state(self):
        self.state = Database(self.scenario.propositions, sorted_search=self.sorted_search)

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
        matches = self.state.match_all(self.scenario.goal.exprs, self.scenario.goal.bindings)
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
            for unifier in self.state.match_all(rule.pre.exprs, rule.pre.bindings):
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
        for term in sorted(self.state.contents):
            sys.stderr.write("::::   {}\n".format(term))
        sys.stderr.write(":::: ]\n")
