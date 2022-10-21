# encoding: UTF-8

"""A breadth-first searching Generator that finds the
shortest path of events that leads to the goal state
(if any such path exists).
"""

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

        while True:
            new_situations = []
            if self.verbosity >= 2:
                sys.stderr.write("Considering {} situations\n".format(len(situations)))
            for (events, state) in situations:
                for rule, unifier in self.get_candidate_rules(state):
                    if not rule.post.exprs:
                        # Rules that don't change the state of the world are not worth considering.
                        continue
                    new_event = Event(rule, unifier)
                    new_state = state.clone()
                    self.update_state(new_state, unifier, rule)
                    new_events = events + [new_event]
                    if self.goal_is_met(new_state):
                        return new_events
                    new_situations.append(
                        (new_events, new_state)
                    )
            if self.verbosity >= 2:
                sys.stderr.write("Installing {} new situations\n".format(len(new_situations)))
            situations = new_situations
