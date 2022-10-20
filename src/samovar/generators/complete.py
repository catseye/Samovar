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
        current_crop_of_states = [Database(self.scenario.propositions, sorted_search=self.sorted_search)]
        goal_has_been_met = False

        while not goal_has_been_met:
            next_crop_of_states = []
            for state in current_crop_of_states:
                for rule, unifier in self.get_candidate_rules(state):
                    new_state = self.update_state(state, unifier, rule)
                    next_crop_of_states.append(new_state)
                    # TODO also record Event(rule, unifier) in there somewhere
                    # TODO if self.goal_is_met(new_state): goal_has_been_met = True (and indicate which one)
