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
        self.reset_state()

    def generate_events(self):
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

    def goal_is_met(self, state):
        matches = state.match_all(self.scenario.goal.exprs, self.scenario.goal.bindings)
        return len(matches) > 0

    def generate_event(self):
        candidates = self.get_candidate_rules()
        if not candidates:
            return None
        rule, unifier = self.random.choice(candidates)
        self.update_state(unifier, rule)
        return Event(rule, unifier)

    def get_candidate_rules(self, state):
        candidates = []
        for rule in self.scenario.rules:
            for unifier in state.match_all(rule.pre.exprs, rule.pre.bindings):
                candidates.append((rule, unifier))

        if self.verbosity >= 3:
            sys.stderr.write("Candidate rules:\n")
            for rule, unifiers in candidates:
                sys.stderr.write("-> " + rule.to_json() + "\n")
                sys.stderr.write("---> {}\n".format(unifiers))
            sys.stderr.write("")

        return candidates

    def update_state(self, state, env, rule):
        new_state = state.clone()
        for expr in rule.post.exprs:
            term = expr.term.subst(env)
            if isinstance(expr, Assert):
                new_state.add(term)
            elif isinstance(expr, Retract):
                new_state.remove(term)
        if self.verbosity >= 3:
            self.debug_state("Intermediate")
        return new_state

    def debug_state(self, label):
        sys.stderr.write(":::: {} State [\n".format(label))
        for term in sorted(self.state.contents):
            sys.stderr.write("::::   {}\n".format(term))
        sys.stderr.write(":::: ]\n")
