Samovar
=======

*Version 0.3.  Subject to change in backwards-incompatible ways.*

Samovar is a DSL for modelling a world using propositions (facts), and possible
events that can occur based on those facts, changing them.

Here is a short example of a Samovar description:

    scenario IgnatzWithBrick {
      
        [actor(?A),item(?I),~holding(?A,?I)]  ?A picks up the ?I.   [holding(?A,?I)]
        [actor(?A),item(?I),holding(?A,?I)]   ?A puts down the ?I.  [~holding(?A,?I)]
    
        actor(Ignatz).
        item(brick).
    
        goal [].
    }

And an implementation of Samovar could take this scenario and use it to,
among other things, generate textual descriptions of chains of events like

    Ignatz picks up the brick. Ignatz puts down the brick.

Of course, this is a very simple example.  (It doesn't even prevent two
actors from picking up the same item at the same time!)  For more complex
examples, and a fuller description of the language, see
[doc/Samovar.md](doc/Samovar.md), which doubles as a test suite.

### Discussion

This looks like logic programming but the internals are actually much simpler.

Samovar could be described as an "assertion-retraction engine", which itself could
be thought of as a highly stylized form of Prolog programming plus some syntactic
sugar.

Alternately, it could be thought of as assigning preconditions and postconditions,
like you would find in [Hoare logic][], to actions in a world-model.  Instead of
proving that the action satisfies the conditions, though, we simply assume it
does, and use the conditions to chain actions together in a sensible order.

But really, the internals are far simpler than an inference engine or a theorem
prover: there are no logical rules in the database, only propositions, so
they can be selected by simple pattern-matching rather than full unification.

[Hoare logic]: https://en.wikipedia.org/wiki/Hoare_logic

### TODO

*   Implement an actual solver.
*   Maybe allow variables to be notated so that they can bind reflexively,
    e.g. `?*A looks at ?*B` can bind both variables to Alice.
*   Make `?_` work such that you can say `¬holding(?_, club)` to mean
    "if no one is holding the club".
