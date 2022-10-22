# encoding: UTF-8

# FIXME: just a sketch for now

import sys
import time

from samovar.ast import Assert, Retract
from samovar.database import Database

from .base import Event, BaseGenerator


class DepthFirstGenerator(BaseGenerator):
    def __init__(self, world, scenario, verbosity=0, sorted_search=True, randomness=None):
        self.world = world
        self.scenario = scenario
        self.verbosity = verbosity
        self.sorted_search = sorted_search
        self.random = randomness
        self.seen_states = set()

    def generate_events(self, **kwargs):
        events = []
        state = Database(self.scenario.propositions, sorted_search=self.sorted_search)

        self.seen_states = set()

        return self._generate_events(events, state)

    def _generate_events(self, events, state):

        for rule, unifier in self.candidate_rules(state, require_change=True):
            new_event = Event(rule, unifier)
            new_state = state.clone()
            self.update_state(new_state, unifier, rule)
            froz = frozenset(new_state.contents)
            if froz in self.seen_states:
                continue
            self.seen_states.add(froz)
            new_events = events + [new_event]
            if self.goal_is_met(new_state):
                return new_events
            # TODO: replace recursion with explicit stack!
            # Because Python often can't handle this.
            result_events = self._generate_events(new_events, new_state)
            if result_events:
                return result_events

        return None
