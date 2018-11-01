Samovar
=======

*Version 0.2 (unreleased).  Subject to change in backwards-incompatible ways.*

Samovar is a DSL for modelling a world using propositions (facts), and possible
events that can occur based on those facts, changing them.

Possible events are described with _event rules_.  Each event rule looks like

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

And we can package this all into a scenario:

    scenario IgnatzWithBrick {
      
        [actor(α),item(β),~holding(α,β)]  α picks up the β.   [holding(α,β)]
        [actor(α),item(β),holding(α,β)]   α puts down the β.  [~holding(α,β)]
    
        actor(Ignatz).
        item(brick).
    
        goal [].
    }

And an implementation of Samovar could take this scenario and use it to,
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
*   Maybe allow `∨` - there doesn't seem to be as much call for it, though.
*   Allow sentence trees to be given for actions.
*   Allow scenarios to define a termination condition, so that the implementation
    can generate a scene where the condition is met (by whatever method).
*   Allow scenarios to specify a minimum number of events to generate (maybe?)
*   Consider what it would take to add a predicate that evaluates to whether
    a given action has been taken previously or not.
