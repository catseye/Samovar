# encoding: UTF-8

"""A breadth-first searching Generator that finds the
shortest path of events that leads to the goal state
(if any such path exists).
"""
#
# NOTE, this is only a rough sketch at the moment!
#

import sys

from samovar.ast import Assert, Retract
from samovar.database import Database

from .base import Event, BaseGenerator


class CompleteGenerator(BaseGenerator):
    def __init__(self, world, scenario, verbosity=0, sorted_search=True, randomness=None):
        self.world = world
        self.scenario = scenario
        self.verbosity = verbosity
        self.sorted_search = sorted_search
        self.random = randomness

    def generate_events(self, **kwargs):
        situations = [
            ([], Database(self.scenario.propositions, sorted_search=self.sorted_search))
        ]
        goal_has_been_met = False

        while not goal_has_been_met:
            new_situations = []
            for (events, state) in situations:
                for rule, unifier in self.get_candidate_rules(state):
                    new_event = Event(rule, unifier)
                    new_state = state.clone()
                    self.update_state(state, unifier, rule)
                    new_events = events + [new_event]
                    if self.goal_is_met(new_state):
                        return new_events
                    new_situations.append(
                        (new_events, new_state)
                    )
            situations = new_situations
