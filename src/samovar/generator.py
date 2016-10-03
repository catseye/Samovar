# encoding: UTF-8

from itertools import permutations
import random

from samovar.ast import Assert, Retract
from samovar.terms import Term


def all_assignments(vars_, things):
    assignments = []
    var_names = [v.name for v in vars_]
    for p in permutations(things, len(vars_)):
        assignments.append(dict(zip(var_names, p)))
    return assignments


class Generator(object):
    def __init__(self, world, debug=False, length=5):
        self.world = world
        self.debug = debug
        self.state = set()  # set of things currently true about the world
        self.things = set()
        self.length = length
        for e in self.world.situations[0].cond.exprs:
            if isinstance(e, Assert):
                self.state.add(e.term)
                atoms = set()
                e.term.collect_atoms(atoms)
                self.things |= atoms

    def generate(self):
        if self.debug:
            self.debug_state()
        for i in xrange(0, self.length):
            self.generate_move()

    def generate_move(self):
        candidates = self.get_candidate_rules()
        rule, unifier = random.choice(candidates)
        print rule.format(unifier)
        self.update_state(unifier, rule)

    def get_candidate_rules(self):
        candidates = []
        for rule in self.world.rules:
            vars_ = set()
            for expr in rule.pre.exprs:
                expr.term.collect_variables(vars_)

            for a in all_assignments(vars_, self.things):
                result = rule.pre.eval(a, self.state)
                if self.debug:
                    print rule.nu_format(), "WITH", a, "==>", result
                if result:
                    candidates.append((rule, a))

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
