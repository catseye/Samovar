# encoding: UTF-8

import sys

from samovar.database import Database

from .base import xrange, Event, BaseGenerator


class StochasticGenerator(BaseGenerator):
    def __init__(self, world, scenario, verbosity=0, sorted_search=True, randomness=None):
        self.world = world
        self.scenario = scenario
        self.verbosity = verbosity
        self.sorted_search = sorted_search
        self.random = randomness
        self.reset_state()

    def reset_state(self):
        self.state = Database(self.scenario.propositions, sorted_search=self.sorted_search)

    def generate_events(self, min_count=0, max_count=100, lengthen_factor=1.5):
        acceptable = False
        count = min_count
        while not acceptable:
            if self.verbosity >= 1:
                sys.stderr.write("Generating {} events\n".format(count))
            self.reset_state()
            if self.verbosity >= 2:
                self.debug_state(self.state, "Initial")
            events = []
            for i in xrange(0, count):
                event = self.generate_event()
                if event is None:
                    break
                events.append(event)
            if self.verbosity >= 2:
                self.debug_state(self.state, "Final")
            acceptable = self.goal_is_met(self.state)
            if not acceptable:
                count = int(float(count) * lengthen_factor)
            if count > max_count:
                raise ValueError("{}: count exceeds maximum".format(self.scenario.name))
        return events

    def generate_event(self):
        candidates = self.get_candidate_rules(self.state)
        if not candidates:
            return None
        rule, unifier = self.random.choice(candidates)
        self.update_state(self.state, unifier, rule)
        if self.verbosity >= 3:
            self.debug_state(self.state, "Intermediate")
        return Event(rule, unifier)
