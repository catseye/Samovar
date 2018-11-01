from samovar.ast import Assert, Retract
from samovar.terms import Term, Var


def match_all(database, patterns, env):
    """Find all matches for the given patterns in the database, and return a list of unifiers.

    `database` is an iterable of Terms.
    `patterns` is a list of Assert's.
    `env` is a dict mapping Var names to Terms (a previous unifier.)

    """
    if not patterns:
        return [env]
    envs = []
    for proposition in database:
        pattern = patterns[0]
        assert isinstance(pattern, Assert)
        try:
            unifier = pattern.term.match(proposition, env)
        except ValueError:
            continue
        envs.extend(match_all(database, patterns[1:], unifier))
    return envs
