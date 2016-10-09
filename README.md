Samovar
=======

*Work-in-progress.  Subject to change in backwards-incompatible ways.*

Samovar is a DSL for world-modeling using predicates rather than explicit objects.

The remainder of this document will probably be trying to explain what I mean by
that.

It could be thought of as an "assertion-retraction engine", which itself could be
thought of as a very stilted style of Prolog programming plus some syntactic
sugar.

Alternately, it could be thought of as assigning preconditions and postconditions,
like you would find in a program proof, to actions in a world-model.  Instead of
proving that the action satisfies the conditions, though, we simply assume it
does, and use the conditions to chain actions together in a sensible order.

A Samovar world is an immutable set of rules which operate on a mutable set of
facts.  Each rule looks like

    [A] X [B]

and means "If A holds, then X is a possible action to take, and if you do take it,
you must make B hold afterwards."

By "hold" we mean "can unify with the current set of facts."

As an example,

    [actor(α),item(β),~holding(α,β)] α picks up the β. [holding(α,β)]

Which can be read "If A is an actor and B is an item and A is not holding B, then
one possible action is to say 'A picks up the B' and assert that A is now holding B."

We can add a complementary rule:

    [actor(α),item(β),holding(α,β)] α puts down the β. [~holding(α,β)]

And we can package this all into a world-description:

    rules
      [actor(α),item(β),~holding(α,β)]  α picks up the β.   [holding(α,β)]
      [actor(α),item(β),holding(α,β)]   α puts down the β.  [~holding(α,β)]
    situations
      [actor(Ignatz),item(brick)]
    end

And an implementation of Samovar can take this world-description and use it to,
among other things, generate chains of events like

    Ignatz picks up the brick. Ignatz puts down the brick.

Of course, this is a very simple example.  A more complex example might have
more actors, more items, and more rules (for example, that two actors cannot
be holding the same item at the same time.)
