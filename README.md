# What does it do?

23/09/2020 v0.1:

* 5e combat simulation using the d20 system
* Simulating player team versus monster team combat
* Returning the player win and monster win ratio
* Melee combat only

# Why does it do it?

As in the docstring says, designing a 5e complicated endevour. The DM wants to create a suspenseful encounter but
 rarely do they want it to kill the player characters (PCs). 
 
the existing methods for designing encounters are the Challenge Rating (CR) system for many DMs insufficient
see https://www.reddit.com/r/DnD/comments/34q5zz/5e_problem_with_challenge_ratings/

This system can be improved by actually simulating an encounter hundreds of times and discover if the party will
 actually die, and if so how many times. This aids the DM in their encounter design.

#Future improvements?

Most definitely some future improvements, such as:

* GUI
* Danger rating number 
    * Not defined by the number of times the players die, although that will be a factor 
    * Other factors will be how many player characters went down
    * max damage of the opponents
    * Number of times the players hit and were hit
* Map / Movement and ranged combat
* Suggest an optimal monster composition
* Spells (healing and damage)
* Status effects
* Difficult & impassable terrain
* Line of sight and decisions to move in or out of it

# Licenses

This script package uses the [SRD 5.1 from Wizards of the Coast](https://media.wizards.com/2016/downloads/DND/SRD-OGL_V5.1.pdf)

Modifications to this code must be held within the SRD 5.1 and Open Gaming License above and is subject to the 
[GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/)
