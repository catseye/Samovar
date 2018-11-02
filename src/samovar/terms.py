# encoding: UTF-8


# Python 2/3
try:
    unicode = unicode
except NameError:
    unicode = str


class AbstractTerm(object):
    pass


class Term(AbstractTerm):
    def __init__(self, constructor, *subterms):
        self.t = tuple([constructor] + list(subterms))

    @property
    def constructor(self):
        return self.t[0]

    @property
    def subterms(self):
        return self.t[1:]

    def __str__(self):
        if len(self.subterms) == 0:
            return self.constructor
        return u"%s(%s)" % (self.constructor, ', '.join([unicode(s) for s in self.subterms]))

    def __repr__(self):
        if self.subterms:
            return "%s(%r, *%r)" % (
                self.__class__.__name__, self.constructor, self.subterms
            )
        else:
            return "%s(%r)" % (
                self.__class__.__name__, self.constructor
            )

    def __eq__(self, other):
        return isinstance(other, Term) and self.t == other.t

    def __hash__(self):
        return hash(self.t)

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
        return Term(self.constructor, *[subterm.subst(env) for subterm in self.subterms])

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
        return isinstance(other, Var) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

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
