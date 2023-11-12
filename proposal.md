# Zombie Survivor
https://github.com/B2Hill/Zombie_Survivor/tree/main
## Description:
Zombie Survivor is intended to be a rouge lite, horde survival game. The game design is applicable to the digital arts field by testing creativity and application of key coding skills to create the final output. The game is a twist on the horde survival/Vampire Survivors Genre with the player character being a Monster/Zombie with abilities inspired by Zombie media and enemy mechanics from other games from the genre.

## Features/Mechanics:
- Enemy tracking
    - Enemy entities will move toward the player
    * entities calculate the direction that they are from the player character and move in that direction based on its movementspeed value.
- Enemy/Player Hit/Hurt detection
    - Enemies will attempt to attack the player and vis-versa when they are within a distance or a projectile touches them causing damage.
    * All created entities will have Hit box and damaging attacks will have a Hurt box. When these invisible boxes overlap eachother they cause damage to that entity. 
    * All hurtboxes/hitboxes will be assigned if they are player owned or enemy owned, only opposing boxes will be allowed to interact.
- Player Character and Enemy health
    - Player and enemy entities will have seperate tracking for individual stats
    * Executed as seperate classes for each object 
- Directional movement
    - Player input will move the character around the screen
    * Executed by using events for wasd and checking for multi input(wa,wd,ds,sa) to create 8-directional movement
- Random Enemy spawn locations
    - Enemy entities a created outside the player visability
    * A radius around the player based on screen size to create entities 
- Random Item drops
    - On enemies being killed they have a random chance to drop benefitcal items for the player
    * A random function on enemy death to check if an item should be dropped, then randomly selecting an item to create at that location
- Experience/Level-up System
    - On enemy death rewards the player with an amount of experiance, and after an amount has been earned grants the player an increase or new skill, or ability.
    * On enemy death update the experiance value of the player, when it is over the required value give the player a choice between 3 upgrades.
- Difficulty scaling
    - The difficulty will scale upwards as the player last longer.
    * The longer the player survies increase the HP, movementspeed, enemytypes, and damage of the enemy class based on the timer. New enemy types will spawn after diffrent time thresholds.
- Progressive bonuses
    - Out of run currency to spend on upgrading the player stats (HP, Movementspeed, DMG, etc.) before/after runs
    * Use of an external file to track the players saved "currency" and applied upgrades to modify the Player Character entity class when it is created at the begining of each play session.
- Seamless stage looping
    - Large map areas with a seemless pattern that endless continues as the player travels in any direction
    * When outerbounds have been reached either move the player to the otherside of the map when the cross the threshold or endlessly create/destroy map chunks as the player moves around the map
- Tracking survival time
    - On screen timer in Min:Secs to track the players progress
    * implement a tick counter and track the seconds and increment a timer display for the player to see.
- Menu System
    - A clickable interface that allows the player to start/restart/quit the game when they choose to.
    * Before play session this would be the default state of the game with simple graphics. Checking for user input via mouse on pre-defined areas to execute going to diffrent menu states.
    * During play session on the press of the escape key, pause gamestate and display menu options looking for the same user inputs on new locations.

## Challenges:
The major challenges will be creating the mechanics to endlessly loop the play area, the directional movement that keeps the visible area centered on the Player Character, and balancing the game so that it is difficult but also provides the power fantasy that the genre gives to the player.

## Outcomes:
### Ideal:
 The ideal outcome for the project is for the game to have at least 8 different character abilities, 8 different player power- ups, minimum of 10 enemy types, at least 1 playable map, functioning player progression system, a menu system to allow player the player to quickly restart or exit the game, and simple retro graphics(art) for all assets.

### Minimal:
Player movement system fully functioning, 1 playable map that loops, 4 different character abilities, 4 player power- ups, 5 enemy types, enemy tracking, random item/power- ups drops and enemy spawning locations, tracking survival time, a win/failure state and minimalistic graphics(art) for all assets.

## Milestones
### Week 1
- Player character movement
- enemy spawning in a radius around the player character
- 1 player abilities
- 1 Enemy type
- player character stats (Movement speed, attack rate, hp, defense, etc.)
- Simple Timer with display

### Week 2
- screen tracking player location (De- spawn enemies that get too far from the player)
- Enemy Movement toward Player character
- 3 player abilities, & 3 player power- ups
- 3 Enemy types
- setting what enemies spawn to timer
- Experience/Level- up system

### Week 3
- Stage looping or progressive generation of stage with the player
- Win/Failure States
- Extra Enemy types (minimum 1)
- Extra Abilities & Power- ups
- Menu System
- Progression System
- Art assets implementation

