Samovar
=======

Version 0.5 | _Entry_ [@ catseye.tc](https://catseye.tc/node/Samovar)
| _See also:_ [The League of Extraordinarily Dull Gentlemen](https://github.com/catseye/NaNoGenMo-Entries-2018/tree/master/league#readme)
∘ [The Swallows](https://github.com/catseye/The-Swallows#readme)
∘ [Cardboard Prolog](https://github.com/catseye/Cardboard-Prolog#readme)

- - - -

**Samovar** is a domain-specific language (DSL) for modelling a world using
propositions (facts), and possible events that can occur based on those facts,
changing them.

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
[doc/Samovar.md](doc/Samovar.md), which also serves as a test suite.

### Discussion

This looks like logic programming but the internals are actually much simpler,
and what it's doing is not logical inference.

The internals are far simpler than an inference engine or a theorem
prover: there are no logical rules in the database, only propositions, so
they can be selected by simple pattern-matching rather than full unification.

I originally described it as an "assertion-retraction engine", which could
be thought of as a highly stylized form of Prolog programming.  Alternately,
it could be thought of as assigning preconditions and postconditions, like
in [Hoare logic][], to actions in a world-model.  Instead of constructing a
proof, though, we simply chain actions together, by selecting any next one
whose preconditions hold, and altering the world so that its postconditions hold.

In (I think) autumn 2019, I came across the concept of a [production system][],
and I realized that is basically what Samovar implements.  Researching it
further, I discovered [CLIPS][], a production system built in 1985,
and I realized that Samovar is not essentially different from an
inefficiently-implemented, stripped-down version of CLIPS.

The main innovation in Samovar is the ability to "narrate" the choices the
production system makes, with human-readable text.

This isn't too surprising, since my goal with Samovar was to make an expressive
language, a syntax in which the author could write a story generator without
the undue effort of switching context between prose and code.  Picking logical
propositions for the "code" and placing them before and after each fragment of
prose was a reasonably "ergonomic" choice, and happens to coincide with the
structure of a production system.

[Hoare logic]: https://en.wikipedia.org/wiki/Hoare_logic
[production system]: https://en.wikipedia.org/wiki/Production_system_(computer_science)
[CLIPS]: https://en.wikipedia.org/wiki/CLIPS

### TODO

*   Maybe allow variables to be notated so that they can bind reflexively,
    e.g. `?*A looks at ?*B` can bind both variables to Alice.
*   Make `?_` work such that you can say `¬holding(?_, club)` to mean
    "if no one is holding the club".
