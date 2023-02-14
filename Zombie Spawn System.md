**==== Zombie Spawn Logic ====**

How the system works
---------
1. We can attach a tag to all zombie teams that fires when one or all of the zombies in that team died (todo: verify if we can reliably check if *all* of them died)
2. Once a zombie (or it's entire team) is dead, we immediately spawn a new zombie/team.
3. We respawn these at a random location using a random timer race condition.
4. For better results, we group zombie spawn locations together and localize the respawns to only spawn at locations of that spawnpoint group.

---------
Benefits of grouping together spawnpoints include:
- Reducing the chance of zombies spawning inconsistently at other sides of the map, lowering the risk of a boring gameplay
- Zombies spawning closer heavily reduces pathing lag;
- Less random timers used in the race condition will guarantee a more uniform distribution of the randomness of spawn locations.

Cons of this include:
- Zombies spawning too close to the players will break immersiveness and continuously pester the player that is trying to fight or flee.


---------
About the problem of zombies spawning directly next to players
---------
There are numerous ways in which we can attempt to prevent or mitigate the impact of this problem:

- Increasing the spawn freeze time in which the zombie is idling an invulnerable.
- Using a solid ring of celltags around the spawn point that when triggered, disable the spawn point for a certain amount of time before it reactivates. A caveat with this is that zombies might walk over the celltags and disable the spawnpoint. However, keeping the circle of celltags small and using a short reactivation time mitigates this problem.
- (optional) Only spawn in location groups around the spawn group associated with the killed zombie.


---------
Increasing the difficulty as the game progresses
---------
Doing this is incredibly simple. Since the amount of zombie teams present in the game will forcibly be replenished, we can make the game harder by spawning in an extra team of zombies, effectively raising the cap of zombies on the map.


---------
Technical Estimations
---------
- The circle of celltags around spawnpoints should probably be 3x3 or 5x5
- There should be many spawn locations to give the illusion of completely random locations



