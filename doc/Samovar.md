Samovar
=======

This is a literate test suite for Samovar, in Falderal format.
It describes Samovar, and includes examples inline; each example
specifies the expected result of running it, so these examples
can be run as tests.  (That's what Falderal does.)

    -> Tests for functionality "Run Samovar Simulation"

    -> Functionality "Run Samovar Simulation" is implemented by
    -> shell command
    -> "bin/samovar %(test-body-file) --events 4 --seed 0"

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

chairs
------

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
    ===> Hastings sits down in the chair.
    ===> Hastings leans back in the chair.
    ===> Petersen sits down in the sofa.
    ===> Wembley sits down in the recliner.


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
    ===> Bob scratches his head.
    ===> Bob scratches his head.
    ===> Alice scratches her head.
    ===> Alice scratches her head.

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
    ===> Bob scratches his head.
    ===> Bob scratches his head.
    ===> Alice scratches her head.
    ===> Alice scratches her head.
