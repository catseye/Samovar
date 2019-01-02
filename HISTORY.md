History of Samovar
==================

### Version 0.3

*   The `?_` wildcard variable matches any term, without binding
    it to anything.
*   Multiple bindings in a `where` clause may be seperated by
    commas.
*   Consequences of a rule may not contain a `where` clause;
    this is statically checked before execution.
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
