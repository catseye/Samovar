from samovar.ast import Assert, Retract
from samovar.terms import Term, Var


def match_all(database, patterns, env):
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
        for proposition in database:
            try:
                unifier = pattern.term.match(proposition, env)
            except ValueError:
                continue
            envs.extend(match_all(database, patterns[1:], unifier))

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

        found = False
        for proposition in database:
            if proposition == expanded_pattern:
                found = True
        if not found:
            envs.extend(match_all(database, patterns[1:], env))

    else:
        raise NotImplementedError

    return envs
