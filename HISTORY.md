History of Samovar
==================

### Version 0.5

*   No changes to language, only implementation.
*   Add a complete (breadth-first search-based) generator
    alongside the existing stochastic generator.  The complete
    generator will always find the shortest series of events
    that leads to the goal, as long as such a series exists.
*   Add a depth-first search based generator as well.  If
    the space of world-configurations is finite (I'm not sure
    if Samovar guarantees this, but it's often the case), this
    also is a complete generator, and more efficient than the
    breadth-first one.
*   Allow the generator to be used to be specified with the
    command-line option `--generator`.
*   Replace `--randomness-type` command-line option with
    `--deterministic` option, which replaces `canned` randomness.
    Searching for facts in database is not done in sorted fashion
    when `--deterministic` is not given, improving performance.
*   Add `--verbosity` command-line option.  There are now 4 levels
    of verbosity, from 0 to 3.  `--verbose` is an alias for level 1,
    and `--debug` is an alias for level 2.
*   Add `--version` command-line option.
*   `bin/samovar` script runs under `python3` by default.
*   Simplify test driver by upgrading test doc to Falderal 0.14.

### Version 0.4

*   No changes to language, only implementation.
*   Update code to work under both Python 2 and Python 3.
*   Extend test suite to run the tests under Python 2, or Python 3,
    or both Python 2 and Python 3, depending on what's available.
*   When collecting matches in `match_all`, iterate over the
    database in a predictable order.  Changes to the `set` data
    type in Python 3 mean that the database wasn't always being
    searched in the same order, which was introducing nondeterminism
    into the test suite.
*   The source of randomness can be configured with the new
    `--randomness-type` command-line option.  There is now a
    "canned randomness" provider which is simple and deterministic
    and used when running the Falderal tests.
*   Make an external script, `profile.sh`, responsible for
    profiling, instead of building that into the main executable.
*   Refactor code so that the `bin/samovar` script contains only
    minimal driver logic.
*   Make the source code PEP-8 compliant (except for line lengths).

### Version 0.3

*   The `?_` wildcard variable matches any term, without binding
    it to anything.
*   Multiple bindings in a `where` clause may be seperated by
    commas.
*   Consequences of a rule may not contain a `where` clause;
    this is statically checked before execution.
*   Occurrence of variables in text and consequences is also
    statically checked.
*   Pathologically poor performance of the lexical scanner on
    large input files (essentially a bug) was fixed.

### Version 0.2

Improved during a "sprint" in the first half of November 2018,
for NaNoGenMo 2018.

#### Language

*   Added tests: a Falderal test suite, as well as unit tests.
*   Variables no longer need to be Greek letters; they can be
    alphanumeric identifiers of any length that begin with `?`.
*   Traditional logical connectives can be used in expressions.
*   "Scenarios" instead of "situations"; a scenario is not
    divided into sections, it can have a `goal`, and it can
    `import` other scenarios.
*   When matching a rule, the same term cannot be bound to
    two different variables.
*   Ability to "pre-bind" a variable to a term, in a rule's
    `where` clause.
*   Removed functions, after demonstrating they're not needed.
*   Clearer expectation that punctuation should be retained when
    it appears in a rule's words.

#### Reference implementation

*   Ability to set the random seed with `--seed`.
*   Improved algorithm for matching rules against propositions;
    uses depth-first recursive pattern-matching to find matching
    rules.  Bindings also treated as immutable.  This led to a
    significant performance improvement (the prototype was ugly.)
*   Implemented the AST with namedtuples, for slight performance
    improvement.
*   Able to output generated events as JSON.
*   `--generate-scenarios`, -`-min-events`, `--max-events`,
    `--lengten-factor` command-line options.
*   Support for running under Python 3.

### Version 0.1

The initial prototype, thrown together in October 2016.
