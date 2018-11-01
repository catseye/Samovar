Samovar
=======

This is a literate test suite for Samovar, in Falderal format.
It describes Samovar, and includes examples inline; each example
specifies the expected result of running it, so these examples
can be run as tests.  (That's what Falderal does.)

    -> Tests for functionality "Run Samovar Simulation"

    -> Functionality "Run Samovar Simulation" is implemented by
    -> shell command
    -> "bin/samovar %(test-body-file) --words 20 --line-per-sentence --seed 0"

Ignatz
------

    scenario IgnatzWithBrick {
    
      [actor(α),item(β),~holding(α,β)]  α picks up the β.   [holding(α,β)]
      [actor(α),item(β),holding(α,β)]   α puts down the β.  [~holding(α,β)]
      
      actor(Ignatz).
      item(brick).
    
    }
    ===> Ignatz picks up the brick.
    ===> Ignatz puts down the brick.
    ===> Ignatz picks up the brick.
    ===> Ignatz puts down the brick.


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
    
    }
    ===> Hastings sits down in the chair.
    ===> Hastings leans back in the chair.
    ===> Wembley sits down in the recliner.
    ===> Petersen sits down in the sofa.


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
    
    }
    ===> Alice scratches her head.
    ===> Alice scratches her head.
    ===> Bob scratches his head.
    ===> Bob scratches his head.
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
    
    }
    ===> Alice scratches her head.
    ===> Alice scratches her head.
    ===> Bob scratches his head.
    ===> Bob scratches his head.
    ===> Alice scratches her head.
