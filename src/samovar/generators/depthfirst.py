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
        self.seen_states = set()

        # Create initial stack.
        events = []
        state = Database(self.scenario.propositions, sorted_search=self.sorted_search)
        candidate_rules = list(self.candidate_rules(state, require_change=True))
        stack = [
            [events, state, candidate_rules, 0]
        ]

        # Loop, doing work at the top of the stack.
        done = False
        counter = 0
        while not done:
            counter += 1
            [events, state, candidate_rules, cr_index] = stack[-1]
            if self.verbosity >= 1 and counter % 1000 == 0:
                sys.stderr.write("Stack level {}, event count {}, candidate count {}, index {}\n".format(
                    len(stack), len(events), len(candidate_rules), cr_index
                ))
            if cr_index > (len(candidate_rules) - 1):
                # we've exhausted all the candidates on this level.  backtrack.
                if self.verbosity >= 1:
                    sys.stderr.write("*** Backtracking")
                stack.pop()
                continue

            # otherwise, try to make a match.
            rule, unifier = candidate_rules[cr_index]

            new_event = Event(rule, unifier)
            new_state = state.clone()
            self.update_state(new_state, unifier, rule)
            if self.verbosity >= 2:
                self.debug_state(new_state, "Intermediate")
            if self.goal_is_met(new_state):
                return new_events

            froz = frozenset(new_state.contents)
            if froz in self.seen_states:
                stack[-1][3] += 1   # inc cr_index. TODO this is so ugly
                continue
            self.seen_states.add(froz)

            # otherwise, try to extend the events we've got.
            new_events = events + [new_event]
            new_candidate_rules = list(self.candidate_rules(new_state, require_change=True))
            stack.append(
                [new_events, new_state, new_candidate_rules, 0]
            )

        return None
