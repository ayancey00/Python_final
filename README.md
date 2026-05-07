# Fantasy Battle Simulator README

## How to Run the Game

1. Make sure Python 3.11 is installed.
2. Make sure pygame is installed.

   pip install pygame

3. Keep all project files in the same folder:

   - main.py
   - battle_logic.py
   - characters.py
   - ui.py
   - numerical_methods.py
   - sprites folder

4. Open a terminal or command prompt in the project folder.
5. Run the game with:

   py -3.11 main.py

If that does not work, try:

   python main.py


## What the Game Is

Fantasy Battle Simulator is a turn-based fighting game. The player chooses one fighter and then chooses an opponent. Each fighter has HP, attack, special attack, defense, speed, a type, and four moves.

The goal is to defeat the opponent by lowering their HP to 0.


## What the User Can Do

### Choose a Fighter

At the start of the game, press one of the number keys to choose your fighter:

1. Emmanuel
2. Ryuzo
3. Shi-Noia
4. King Zarus
5. Jasmine
6. Alexander


### Choose an Opponent

After picking your fighter, press a number key again to choose who you want to fight.

You cannot choose the same character as yourself.


### Pick Moves During Battle

During battle, press:

1. Use move 1
2. Use move 2
3. Use move 3
4. Use move 4

Each move can do something different, such as:

- Deal damage
- Heal HP
- Raise stats
- Lower enemy accuracy
- Cause confusion
- Add damage over time
- Boost future attacks


### Battle Messages

After each turn, the game shows what happened, such as:

- Which moves were used
- How much damage was dealt
- If a move missed
- If a move was super effective
- If someone healed
- If a status effect happened


### Numerical Method Info

During battle, press:

N - Show numerical method information

This shows information from the root-finding and interpolation methods, such as the heal threshold and estimated heal value.


### Monte Carlo Simulation

During battle, press:

M - Run a Monte Carlo simulation

This repeats many computer-controlled battles and estimates things like:

- Win rate
- Average remaining HP
- Average number of turns

This helps show which fighter is stronger over many battles instead of just one lucky match.


### Restart the Game

When the battle ends, press:

R - Return to the fighter select screen

Then you can choose new fighters and play again.




