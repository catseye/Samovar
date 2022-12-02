# encoding: UTF-8

"""A breadth-first searching Generator that finds the
shortest path of events that leads to the goal state
(if any such path exists).
"""

import sys
import time

from samovar.ast import Assert, Retract
from samovar.database import Database

from .base import Event, BaseGenerator


class BreadthFirstGenerator(BaseGenerator):
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

        seen_states = set()

        while True:
            new_situations = []
            if self.verbosity >= 1:
                sys.stderr.write("Considering {} situations\n".format(len(situations)))
                start_time = time.time()
            for (events, state) in situations:
                for rule, unifier in self.candidate_rules(state, require_change=True):
                    new_event = Event(rule, unifier)
                    new_state = state.clone()
                    self.update_state(new_state, unifier, rule)
                    froz = frozenset(new_state.contents)
                    if froz in seen_states:
                        continue
                    seen_states.add(froz)
                    new_events = events + [new_event]
                    if self.goal_is_met(new_state):
                        return new_events
                    new_situations.append(
                        (new_events, new_state)
                    )
            if self.verbosity >= 1:
                end_time = time.time()
                duration = end_time - start_time
                sys.stderr.write("Considered {} situations in {} seconds ({} situations / second)\n".format(len(situations), duration, float(len(situations))/duration))
                sys.stderr.write("Installing {} new situations\n".format(len(new_situations)))
            situations = new_situations
