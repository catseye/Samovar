Samovar
=======

This is a literate test suite for Samovar, in [Falderal][] format.
It describes Samovar, and includes examples inline, which consist
of valid Samovar descriptions and what you might expect from
running them.

Falderal can actually run these examples and check that they actually
produce these results, so these examples serve as tests.

However, Samovar only specifies the declarative meaning of a
Samovar description, not the operational aspect.  An implementation
of Samovar is allowed to do pretty much whatever it likes.
However, there are certain behaviours that many Samovar implementations
(and in particular, the reference implementation) would be reasonably
expected to support, and it is this behaviour which these examples
will illustrate.

[Falderal]: http://catseye.tc/node/Falderal

    -> Functionality "Run Samovar Simulation" is implemented by shell command
    -> "python2 bin/samovar %(test-body-file) --min-events 4 --deterministic"
    -> but only if shell command "command -v python2" succeeds

    -> Functionality "Run Samovar Simulation" is implemented by shell command
    -> "python3 bin/samovar %(test-body-file) --min-events 4 --deterministic"
    -> but only if shell command "command -v python3" succeeds

    -> Tests for functionality "Run Samovar Simulation"

Basic Syntax
------------

A minimally valid Samovar description looks like this.
(The `===>` is not part of the Samovar description.  It
indicates what output we would expect from this.  In this case,
nothing.)

    scenario A {}
    
    ===> 

You can include comments with `//`.

    // This is my minimal Samovar description.
    scenario A {}
    
    ===> 

The name of a scenario must begin with a letter or underscore,
and can consist of letters, numbers, hyphens, underscores, and
apostrophes.

The same rules apply to most other "words" appearing in a Samovar
description.

    scenario Pin_afore-isn't-1000 {
        this-is-a-constructor(this-is-an-atom).
    }
    
    ===> 

Basic Semantics
---------------

The basic unit of a Samovar world is a scenario.  Inside a scenario,
facts are defined with _propositions_, and possible events are
defined with _event rules_.  Each event rule looks like

    [A] X [B]

which can be read

> If A holds, then X is a possible action to take, and if you do take it,
> you must make B hold afterwards.

By "hold" we mean "matches the current set of facts."

As an example,

    [actor(α),item(β),~holding(α,β)] α picks up the β. [holding(α,β)]

Which can be read as

>   If α is an actor and β is an item and α is not holding β, then one possible
>   action is to write out 'α picks up the β' and assert that α is now holding β.

The Greek letters represent variables, which are bound to concrete
terms during the pattern-matching process.  (Variables can also be
written with Latin letters, and given names longer than one character,
by introducing them with a question mark, like this: `?var`.)

Now, we can add a complementary rule:

    [actor(α),item(β),holding(α,β)] α puts down the β. [~holding(α,β)]

And we can package this all into a scenario:

    scenario IgnatzWithBrick {
    
      [actor(α),item(β),~holding(α,β)]  α picks up the β.   [holding(α,β)]
      [actor(α),item(β),holding(α,β)]   α puts down the β.  [~holding(α,β)]
      
      actor(Ignatz).
      item(brick).
    
      goal [].
    }
    ===> Ignatz picks up the brick.
    ===> Ignatz puts down the brick.
    ===> Ignatz picks up the brick.
    ===> Ignatz puts down the brick.

Scenarios
---------

The basic unit of a Samovar world is a scenario.  A scenario may contain
any number of propositions and event rules, and an optional goal, in any order.

    scenario IgnatzWithBrick {
    
      [actor(α),item(β),~holding(α,β)]  α picks up the β.   [holding(α,β)]
      [actor(α),item(β),holding(α,β)]   α puts down the β.  [~holding(α,β)]
      
      actor(Ignatz).
      item(brick).
    
      goal [].
    }
    ===> Ignatz picks up the brick.
    ===> Ignatz puts down the brick.
    ===> Ignatz picks up the brick.
    ===> Ignatz puts down the brick.

A source file may contain more than one scenario.  By default, our
implementation of Samovar runs a simulation on each of the scenarios
that has a goal defined, even if that goal is empty.

    scenario MollyWithBrick {
    
      [actor(α),item(β),~holding(α,β)]  α picks up the β.   [holding(α,β)]
      [actor(α),item(β),holding(α,β)]   α puts down the β.  [~holding(α,β)]
      
      actor(Molly).
      item(brick).
    
    }

    scenario IgnatzWithBrick {
    
      [actor(α),item(β),~holding(α,β)]  α picks up the β.   [holding(α,β)]
      [actor(α),item(β),holding(α,β)]   α puts down the β.  [~holding(α,β)]
      
      actor(Ignatz).
      item(brick).
        
      goal [].
    }
    ===> Ignatz picks up the brick.
    ===> Ignatz puts down the brick.
    ===> Ignatz picks up the brick.
    ===> Ignatz puts down the brick.

Scenarios can import the event rules and propositions from other scenarios.
This makes a scenario a good place to collect a setting, or a group of
characters who will appear together in scenes.  These "library" scenarios
should have no goal, as we don't want to generate simulations for them.

    scenario ItemRules {
      [actor(α),item(β),~holding(α,β)]  α picks up the β.   [holding(α,β)]
      [actor(α),item(β),holding(α,β)]   α puts down the β.  [~holding(α,β)]
    }
    scenario Actors {
      actor(Ignatz).
    }
    scenario Brickyard {
      item(brick).
    }
    scenario Main {
      import ItemRules.
      import Actors.
      import Brickyard.
      goal [].
    }
    ===> Ignatz picks up the brick.
    ===> Ignatz puts down the brick.
    ===> Ignatz picks up the brick.
    ===> Ignatz puts down the brick.

There is nothing stopping an implementation from allowing a Samovar
description to be spread over multiple source files, but there is no
facility to reference one source file from another in Samovar, so how
they are located and collected is up to the implementation.

Goals
-----

A scenario is run until it meets the goal.  How it meets the goal
is up to the implementation.  Our implementation generates events
randomly, until it comes up with a series of events wherein the
goal is met, generating more events each time.

A goal of `[]`, as above, is trivially met.

Generation of events does not stop immediately once the goal is
met.  A number of events are generated, and then the check is made.

    scenario UntilHoldBrick {
      [actor(α),item(β),~holding(α,β)]  α picks up the β.   [holding(α,β)]
      [actor(α),item(β),holding(α,β)]   α puts down the β.  [~holding(α,β)]
      actor(Ignatz).
      item(brick).
      item(oilcan).
      goal [holding(Ignatz,brick)].
    }
    ===> Ignatz picks up the brick.
    ===> Ignatz picks up the oilcan.
    ===> Ignatz puts down the oilcan.
    ===> Ignatz picks up the oilcan.
    ===> Ignatz puts down the oilcan.
    ===> Ignatz picks up the oilcan.
    ===> Ignatz puts down the oilcan.
    ===> Ignatz picks up the oilcan.

Event rules
-----------

We've already seen that an event may be selected if its pattern matches
the current set of facts.  Let's take a closer look at how patterns are
matched.

If a variable appears more than once in a pattern, it must match
the same term in each occurrence.

    scenario IgnatzAndMolly {
      [actor(?A),sitting(?A)] ?A was sitting. []
      actor(Ignatz).
      sitting(Molly).
    
      goal [].
    }
    ===> 

No two variables can match with the same term.  This may seem somewhat
unusual, if you're familiar with Prolog or other languages with
pattern-matching, but it prevents a "reflexive" matches (for example,
"Alice looks at Alice") that don't actually come up very often when
telling a story.

    scenario IgnatzAndMolly {
      [actor(?A),actor(?B)] ?A looks at ?B. [~actor(?A),~actor(?B)]
      actor(Ignatz).
      actor(Molly).
    
      goal [].
    }
    ===> Ignatz looks at Molly.

    scenario IgnatzWithoutMolly {
      [actor(?A),actor(?B)] ?A looks at ?B. [~actor(?A),~actor(?B)]
      actor(Ignatz).
    
      goal [].
    }
    ===> 

A variable may appear in the pattern that is not used in the text or the
consequences.

    scenario IgnatzAndMolly {
      [actor(?A)] Someone. []
      actor(Ignatz).
      actor(Molly).
    
      goal [].
    }
    ===> Someone.
    ===> Someone.
    ===> Someone.
    ===> Someone.

But a variable may not appear in the text if it did not appear in the
pattern.

    scenario IgnatzAndMolly {
      [actor(?A)] ?B sneezes. []
      actor(Ignatz).
      actor(Molly).
    
      goal [].
    }
    ???> SamovarSyntaxError

Likewise, a variable may not appear in the consequences if it did not
appear in the pattern.

    scenario IgnatzAndMolly {
      [actor(?A)] Someone sneezes. [~actor(?B)]
      actor(Ignatz).
      actor(Molly).
    
      goal [].
    }
    ???> SamovarSyntaxError

A special "wildcard" variable, `?_`, matches any term, and does not unify.

    scenario UntilHoldBrick {
      [actor(?_),item(?_)]  There was an actor and an item.  [~actor(Ignatz)]
      actor(Ignatz).
      item(brick).
      goal [].
    }
    ===> There was an actor and an item.

`?_` cannot appear in the text or the consequences of a rule, even if it
appears in the pattern.

    scenario UntilHoldBrick {
      [actor(?_),item(?_)]  There was ?_ and ?_.  [~actor(Ignatz)]
      actor(Ignatz).
      item(brick).
      goal [].
    }
    ???> SamovarSyntaxError

    scenario UntilHoldBrick {
      [actor(?_),item(?_)]  There was an actor and an item.  [~actor(?_)]
      actor(Ignatz).
      item(brick).
      goal [].
    }
    ???> SamovarSyntaxError

The text inside the event rule is typically expanded with the values
that the pattern variables matched.

    scenario UntilHoldBrick {
      [actor(α),item(β),~holding(α,β)]  α picks up the β.   [holding(α,β)]
      actor(Ignatz).
      item(brick).
      goal [holding(Ignatz,brick)].
    }
    ===> Ignatz picks up the brick.

The text may contain punctuation.

    scenario UntilHoldBrick {
      [actor(α),item(β),~holding(α,β)]  "What a lovely β this is!" says α, picking it up.  [holding(α,β)]
      actor(Ignatz).
      item(brick).
      goal [holding(Ignatz,brick)].
    }
    ===> "What a lovely brick this is!" says Ignatz, picking it up.

    scenario UntilHoldBrick {
      [actor(?A),item(?I),~holding(?A,?I)]  "What a lovely ?I this is!" says ?A, picking it up.  [holding(?A,?I)]
      actor(Ignatz).
      item(brick).
      goal [holding(Ignatz,brick)].
    }
    ===> "What a lovely brick this is!" says Ignatz, picking it up.

Punctuation should be preserved sensibly.

    scenario UntilHoldBrick {
      [actor(α),item(β),~holding(α,β)]  "β, don't you know?" says α, picking it up.  [holding(α,β)]
      actor(Ignatz).
      item(brick).
      goal [holding(Ignatz,brick)].
    }
    ===> "brick, don't you know?" says Ignatz, picking it up.

    scenario UntilHoldBrick {
      [actor(?A),item(?I),~holding(?A,?I)]  "?I, don't you know?" says ?A, picking it up.  [holding(?A,?I)]
      actor(Ignatz).
      item(brick).
      goal [holding(Ignatz,brick)].
    }
    ===> "brick, don't you know?" says Ignatz, picking it up.

An event rule may come with some variables pre-bound.

    scenario UntilHoldBrick {
      [actor(?A),item(?I),~holding(?A,?I) where ?I=brick] ?A picked up the ?I. [holding(?A,?I)]
      actor(Ignatz).
      item(brick).
      item(banana).
      goal [holding(Ignatz,brick)].
    }
    ===> Ignatz picked up the brick.

A variable pre-bound in a `where` may appear in the text and consequences.

    scenario IgnatzAndMolly {
      [actor(?A) where ?B=Molly] ?B sneezes. [sneezed(?B)]
      actor(Ignatz).
      actor(Molly).
    
      goal [].
    }
    ===> Molly sneezes.
    ===> Molly sneezes.
    ===> Molly sneezes.
    ===> Molly sneezes.

There may be multiple bindings in a where clause.  These may be
seperated by commas.

    scenario UntilHoldBrick {
      [actor(?A),item(?I),~holding(?A,?I) where ?A=Ignatz,?I=brick] ?A picked up the ?I. [holding(?A,?I)]
      actor(Ignatz).
      item(brick).
      item(banana).
      goal [holding(Ignatz,brick)].
    }
    ===> Ignatz picked up the brick.

You can't put a `where` clause in the consequences.

    scenario UntilHoldBrick {
      [actor(?A),item(?I),~holding(?A,?I)] ?A picked up the ?I. [holding(?A,?I) where ?A=Ignatz]
      actor(Ignatz).
      item(brick).
      item(banana).
      goal [holding(Ignatz,brick)].
    }
    ???> SamovarSyntaxError

chairs
------

Somewhat uninteresting due to the deterministic randomness engine required
to get the tests to be reproducible under both Python 2 and Python 3.

    scenario Chairs {
    
      [actor(ρ)∧¬sitting(ρ)]
        ρ walks around the room.
      []
    
      [actor(ρ)∧¬sitting(ρ)∧nearby(κ)∧empty(κ)]
        ρ sits down in the κ.
      [sitting(ρ)∧in(ρ,κ)∧¬empty(κ)]
    
      [actor(ρ)∧sitting(ρ)∧in(ρ,κ)]
        ρ leans back in the κ.
      []
    
      [actor(ρ)∧sitting(ρ)∧in(ρ,κ)]
        ρ gets up and stretches.
      [¬sitting(ρ)∧¬in(ρ,κ)∧empty(κ)]
    
      actor(Hastings).
      actor(Petersen).
      actor(Wembley).
      nearby(chair). empty(chair).
      nearby(recliner).
      empty(recliner).
      nearby(sofa).
      empty(sofa).
    
      goal [].
    }
    ===> Hastings walks around the room.
    ===> Petersen walks around the room.
    ===> Hastings walks around the room.
    ===> Petersen walks around the room.


no need for functions
---------------------

Samovar 0.1 had functions, but they were removed because they
were not necessary.  If you want to look up a property of
some thing, you can just pattern-match for it.  The example was

    their(Alice) → her
    their(Bob) → his
    
but we can just say
    
    scenario ScratchesHead {
    
      [actor(ρ),possessive(ρ,ξ)]
        ρ scratches ξ head.
      []
    
      actor(Alice).
      possessive(Alice, her).
      actor(Bob).
      possessive(Bob, his).
    
      goal [].
    }
    ===> Alice scratches her head.
    ===> Bob scratches his head.
    ===> Alice scratches her head.
    ===> Bob scratches his head.

This loses the nice property of the function name being a readable
placeholder in the sentence, but you can now use named variables
instead:

    scenario ScratchesHead {
    
      [actor(?Actor),possessive(?Actor,?their)]
        ?Actor scratches ?their head.
      []
    
      actor(Alice).
      possessive(Alice, her).
      actor(Bob).
      possessive(Bob, his).
    
      goal [].
    }
    ===> Alice scratches her head.
    ===> Bob scratches his head.
    ===> Alice scratches her head.
    ===> Bob scratches his head.
