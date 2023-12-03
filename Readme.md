# Zombie Survivor

## Demo
Demo Video: https://vimeo.com/890869436?share=copy

## GitHub Repository
GitHub Repo: https://github.com/B2Hill/Zombie_Survivor

## Description:
Zombie Survivor is intended to be a rouge lite, horde survival game. The game design is applicable to the digital arts field by testing creativity and application of key coding skills to create the final output. The game is a twist on the horde survival/Vampire Survivors Genre with the player character being a Monster/Zombie with abilities inspired by Zombie media and enemy mechanics from other games from the genre.

## Controls:
Movement: WASD
Pause: Escape

## Project Files:
### settings.py
settings.py is a overall settings controller for the main project file. This file allows either the Dev or player to change atributes for the overall game without having to dig through the main project file to alter the WindowSize, Default Player/Enemy/bullet Atributes.

### spritesheet.py
spriteshee.py is a class to control and read .json files for handling loading images from a single .png file. I keep this seperate from the main project file to reduce bloat within the main file.

### project.py
#### Classes
##### Player
The player class is the class that sets up the player character. Within it has several def's that control the players abilities, stats, movement, animations, and other functions that are needed.
##### Enemy
The enemy class is similar to function as the player class but instead of using player inputs for movement, it updates its movement based on angle from the player and moves following its simple AI.
##### Bullet
The Bullet class is the controller for all projectiles within the game. Each projectile is assigned a spawn location, angle of travel, speed, damage value, and an owner. The class also checks for collisions between entities based on the owner(Player/Enemy)
##### UI
The UI Class is all of the UI elements within the game. it also handles the levelup state for the player.
##### enviroment
The enviroment class is how the game generates art assets for each tile. additional assets can be quickly added and has a built in failsafe to generate a tree if the requested asset doesn't exsist.
##### tile
The Tile class is the background or tileset for the game. it is similar to the enviroment class but with the additional featrue relocating itself to a new position based on player movement to create the illusion of an infinite tileset.
##### Gamelevel
The Gamelevel class is the main game controller system for the game. It handles all spawning of enemies, tiles, enviroment art, darawing sprites. it also handles the DEBUG state to create bounding boxes to display hit/hurt boxes and outlines all sprites.
##### Button
The Button class implements the clickable button system for the menu's in game. The class also controlls all the actions if a button is clicked.

## Challenges:
The major challenge within the entire project was time constants. Everything from following the base tutorial I used to gathering the assets took far more time to change and implement than I believed would take. This coupled with having limited time to dedicate to the required me to reduce the scope down to the key elements and ensure the systems for expansion get built, while still using placeholder assets.
## Future Improvements:
For future itterations on this, another pass at the attack system can be done along with having it as its own class to allow for faster exspansion on abilibites to reduce development time on getting diffrent abilibites to function without causing lag. I would also finish out the diffrent png's and json files for the diffrent assets.

## Credits
### Soldiers
    Momonga
        https://momongaa.itch.io/ww2-soldiers-character-sprite-pack

### Homeless Character Pack
    Craftpix.net
        https://free-game-assets.itch.io/homeless-character-pixel-art-pack
### Zombie - simple, becomes projectile
    IronnButterfly
        https://ironnbutterfly.itch.io/zombie-sprite
### Particle FX Smoke
    RagnaPixel
        https://ragnapixel.itch.io/particle-fx-smoke

### Tileset
    RPG Nature Tileset
    RPG Nature Tileset Snow
    RPG Nature Tileset Autumn
    by Stealhix
        https://stealthix.itch.io/rpg-nature-tileset


### Code Tutorial:
    JCode - https://www.youtube.com/@JCode777
        Top down shooter Tutorial - https://www.youtube.com/watch?v=OUOI6iCrmCk