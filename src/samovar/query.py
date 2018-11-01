from samovar.terms import Term, Var


def match_all(database, patterns, env):
    if not patterns:
        return [env]
    envs = []
    for proposition in database:
        try:
            unifier = patterns[0].match(proposition, env)
        except ValueError:
            continue
        envs.extend(match_all(database, patterns[1:], unifier))
    return envs
