from samovar.ast import Assert, Retract


class Database(object):
    """A database is a set of things true at some point in time in a world."""

    def __init__(self, propositions):
        self.contents = set()
        for term in propositions:
            self.contents.add(term)

    def add(self, term):
        self.contents.add(term)

    def remove(self, term):
        self.contents.remove(term)

    def match_all(self, patterns, env):
        """Find all matches for the given patterns in the database, and return a list of unifiers.

        `database` is an iterable of `Term`s.
        `patterns` is a list of `Assert`s and `Retract`s.
        `env` is a dict mapping `Var` names to `Term`s (a previous unifier.)

        """
        if not patterns:
            return [env]
        envs = []
        pattern = patterns[0]

        if isinstance(pattern, Assert):
            # While the construction and iteration of the database set in Python 2 seems to be
            # stable, when running under Python 3, we get an unpredictable order when iterating
            # here.  So we sort the iterable before making matches, so that we can accumulate
            # them in a predictable order (for tests).  TODO: if this hurts performance, provide
            # a command-line option to turn it off.
            for proposition in sorted(self.contents):
                try:
                    unifier = pattern.term.match(proposition, env, unique_binding=True)
                except ValueError:
                    continue
                envs.extend(self.match_all(patterns[1:], unifier))

        elif isinstance(pattern, Retract):
            # to test a negative match, we require first that there are
            # no free variables in our pattern.

            expanded_pattern = pattern.term.subst(env)
            free_vars = set()
            expanded_pattern.collect_variables(free_vars)
            if free_vars:
                # TODO: better exception than this
                raise NotImplementedError

            # now we simply check if the term exists in the database.
            # if it does not, we recurse down to the next clause in the pattern.

            if not (expanded_pattern in self.contents):
                envs.extend(self.match_all(patterns[1:], env))

        else:
            raise NotImplementedError

        return envs
