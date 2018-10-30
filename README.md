Samovar
=======

*Version 0.2 (unreleased).  Subject to change in backwards-incompatible ways.*

Samovar is a DSL for world-modeling using propositions.

A Samovar world is an immutable set of rules which operate on a mutable set of
facts.  Each rule looks like

    [A] X [B]

and means "If A holds, then X is a possible action to take, and if you do take it,
you must make B hold afterwards."

By "hold" we mean "matches the current set of facts."

As an example,

    [actor(α),item(β),~holding(α,β)] α picks up the β. [holding(α,β)]

Which can be read

>   If α is an actor and β is an item and α is not holding β, then one possible
>   action is to write out 'α picks up the β' and assert that α is now holding β.

We can add a complementary rule:

    [actor(α),item(β),holding(α,β)] α puts down the β. [~holding(α,β)]

And we can package this all into a world-description:

    rules
      [actor(α),item(β),~holding(α,β)]  α picks up the β.   [holding(α,β)]
      [actor(α),item(β),holding(α,β)]   α puts down the β.  [~holding(α,β)]
    end
    situations
      [actor(Ignatz),item(brick)]
    end

And an implementation of Samovar could take this world-description and use it to,
among other things, generate textual descriptions of chains of events like

    Ignatz picks up the brick. Ignatz puts down the brick.

Of course, this is a very simple example.  A more complex example might have
more actors, more items, and more rules (for example, that two actors cannot
be holding the same item at the same time.)

### Discussion

Samovar could be described as an "assertion-retraction engine", which itself could
be thought of as a highly stylized form of Prolog programming plus some syntactic
sugar.

Alternately, it could be thought of as assigning preconditions and postconditions,
like you would find in [Hoare logic][], to actions in a world-model.  Instead of
proving that the action satisfies the conditions, though, we simply assume it
does, and use the conditions to chain actions together in a sensible order.

[Hoare logic]: https://en.wikipedia.org/wiki/Hoare_logic

### TODO

*   Implement the pattern-matching of propositions using
    [this algorithm](https://github.com/NaNoGenMo/2018/issues/6#issuecomment-433445689)
*   Allow `¬` instead of `~`, `∧` instead of `,`.
*   Maybe allow `∨` - there doesn't seem to be as much call for it, though.
*   Should probably also allow ASCII tokens for those who don't want to type Greek
    letters and weird logical connectives.
*   Allow actions to define sentence trees.
*   Give the implementation some mode where it deterministically processes rules.
*   Given the above, write a Falderal test document for Samovar.
*   Allow situations to define a termination condition, so that the implementation
    can generate a scenario where the condition is met (by whatever method).
