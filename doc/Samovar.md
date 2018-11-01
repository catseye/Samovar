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

    rules
      [actor(α),item(β),~holding(α,β)]  α picks up the β.   [holding(α,β)]
      [actor(α),item(β),holding(α,β)]   α puts down the β.  [~holding(α,β)]
    end
    situations
      [actor(Ignatz),item(brick)]
    end
    
    ===> Ignatz picks up the brick.
    ===> Ignatz puts down the brick.
    ===> Ignatz picks up the brick.
    ===> Ignatz puts down the brick.


chairs
------

    rules
    
      [actor(ρ),~sitting(ρ)]
      ρ walks around the room.
      []
    
      [actor(ρ),~sitting(ρ),nearby(κ),empty(κ)]
      ρ sits down in the κ.
      [sitting(ρ),in(ρ,κ),~empty(κ)]
    
      [actor(ρ),sitting(ρ),in(ρ,κ)]
      ρ leans back in the κ.
      []
    
      [actor(ρ),sitting(ρ),in(ρ,κ)]
      ρ gets up and stretches.
      [~sitting(ρ),~in(ρ,κ),empty(κ)]
    
    end
    
    situations
    
    [
        actor(Hastings),
        actor(Petersen),
        actor(Wembley),
        nearby(chair), empty(chair),
        nearby(recliner), empty(recliner),
        nearby(sofa), empty(sofa)
    ]
    
    end
    ===> Hastings sits down in the chair.
    ===> Hastings leans back in the chair.
    ===> Wembley sits down in the recliner.
    ===> Petersen sits down in the sofa.

idle
----

    rules
    
      [actor(ρ)]
      ρ rubs his chin.
      []
      
      [actor(ρ)]
      ρ yawns.
      []
    
    end
    ???> IndexError

functions
---------

    rules
      [actor(ρ)]
        ρ scratches their(ρ) head.
      []
    end
    functions
      their(Alice) → her
      their(Bob) → his
    end
    situations
    [
        actor(Alice),
        actor(Bob)
    ]
    end
    
    ===> Alice scratches her head.
    ===> Alice scratches her head.
    ===> Bob scratches his head.
    ===> Bob scratches his head.
    ===> Alice scratches her head.

no need for functions
---------------------

    rules
      [actor(ρ),possessive(ρ,ξ)]
        ρ scratches ξ head.
      []
    end
    situations
    [
        actor(Alice),
        possessive(Alice, her),
        actor(Bob),
        possessive(Bob, his)
    ]
    end
    
    ===> Alice scratches her head.
    ===> Alice scratches her head.
    ===> Bob scratches his head.
    ===> Bob scratches his head.
    ===> Alice scratches her head.
