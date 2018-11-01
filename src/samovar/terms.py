# encoding: UTF-8


class AbstractTerm(object):

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(unicode(self))

    def match_many(self, terms):
        successes = []
        for term in terms:
            unifier = {}
            try:
                self.match(term, unifier)
                successes.append((term, unifier))
            except ValueError as e:
                pass
        return successes


class Term(AbstractTerm):
    def __init__(self, constructor, subterms=None):
        if subterms is None:
            subterms = []
        self.constructor = constructor
        self.subterms = subterms

    def __str__(self):
        if len(self.subterms) == 0:
            return self.constructor
        return u"%s(%s)" % (self.constructor, ', '.join([unicode(s) for s in self.subterms]))

    def __repr__(self):
        if self.subterms:
            return "%s(%r, subterms=%r)" % (
                self.__class__.__name__, self.constructor, self.subterms
            )
        else:
            return "%s(%r)" % (
                self.__class__.__name__, self.constructor
            )

    def __eq__(self, other):
        if not isinstance(other, Term):
            return False
        if self.constructor != other.constructor:
            return False
        if len(self.subterms) != len(other.subterms):
            return False
        for (st1, st2) in zip(self.subterms, other.subterms):
            if st1 != st2:
                return False
        return True

    def is_atom(self):
        return len(self.subterms) == 0

    def is_ground(term):
        for subterm in term.subterms:
            if not subterm.is_ground():
                return False
        return True

    def match(self, term, env):
        if self.constructor != term.constructor:
            raise ValueError("`%s` != `%s`" % (self.constructor, term.constructor))
        if len(self.subterms) != len(term.subterms):
            raise ValueError("`%s` != `%s`" % (len(self.subterms), len(term.subterms)))
        for (subpat, subterm) in zip(self.subterms, term.subterms):
            env = subpat.match(subterm, env)
        return env

    def subst(self, env):
        return Term(self.constructor, subterms=[subterm.subst(env) for subterm in self.subterms])

    def collect_atoms(self, atoms):
        if self.is_atom():
            atoms.add(self)
        else:
            for subterm in self.subterms:
                subterm.collect_atoms(atoms)

    def collect_variables(self, vars_):
        for subterm in self.subterms:
            subterm.collect_variables(vars_)


class Var(AbstractTerm):
    def __init__(self, name):
        self.name = unicode(name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.name)

    def __eq__(self, other):
        if not isinstance(other, Var):
            return False
        return self.name == other.name

    def is_atom(self):
        return False

    def is_ground(term):
        return False

    def match(self, term, env):
        if self.name in env:
            bound_to = env[self.name]
            return bound_to.match(term, env)
        else:
            return dict(list(env.items()) + [(self.name, term)])

    def subst(self, env):
        return env[self.name]

    def collect_atoms(self, atoms):
        pass

    def collect_variables(self, vars_):
        vars_.add(self)
