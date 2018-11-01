# encoding: UTF-8

from itertools import permutations
import random
import re

from samovar.ast import Assert, Retract
from samovar.query import match_all
from samovar.terms import Term


def word_count(s):
    return len(re.split(r'\s+', s))


class Generator(object):
    def __init__(self, world, debug=False):
        self.world = world
        self.debug = debug
        self.state = set()  # set of things currently true about the world
        for e in self.world.situations[0].cond.exprs:
            if isinstance(e, Assert):
                self.state.add(e.term)

    def generate_events(self, count):
        if self.debug:
            self.debug_state()
        moves = []
        for i in xrange(0, count):
            moves.append(self.generate_move())
        return moves

    def generate_words(self, target):
        if self.debug:
            self.debug_state()
        moves = []
        count = 0
        while count < target:
            move = self.generate_move()
            count += word_count(move)
            moves.append(move)
        return moves

    def generate_move(self):
        candidates = self.get_candidate_rules()
        rule, unifier = random.choice(candidates)
        move = rule.format(unifier)
        self.update_state(unifier, rule)
        return move

    def get_candidate_rules(self):
        candidates = []
        for rule in self.world.rules:
            for unifier in match_all(self.state, rule.pre.exprs, {}):
                candidates.append((rule, unifier))

        if self.debug:
            print "Candidate rules:"
            for rule, unifiers in candidates:
                print rule.nu_format()
                print "->", unifiers
            print

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
        print "Things now:"
        for term in self.things:
            print u"  %s" % term
        print "State now:"
        for term in self.state:
            print u"  %s" % term
        print
