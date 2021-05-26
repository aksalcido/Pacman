# Pacman
A Python influenced-version of the well known arcade game, Pacman. The game immediately starts when the `main.pyw` file is ran. The program does not contain a Main Menu, but does include levels and acceleration of the game. Losing all the lives results in a Game Over screen, and the program is done.

# Libraries Used
`tkinter` - Graphics library that allows the game to be playable with constant updates. <br />
`os`- Supported the GameImage class, and allowed images to be organized in it's own directory. <br />
`PIL.ImageTk` - Handles the special images used for Pacman, Enemies, and Pickup objects.<br />
`collections.deque` - Data structure required in the Breadth First-Search Algorithm, which was required to for the enemies pathfinding.<br />
`random` - Allowed random movement for certain enemies that had their own unique movement.<br />

# Instructions / Hot Keys
<h4> Movement </h4>

<h4> Player Movement </h4>
`W` -> Upward Movement        <br />
`A` -> Leftward Movement      <br />
`D` -> Downward Movement      <br />
`S` -> Rightward Movement     <br />

<h4> Other </h4>
`esc` -> Pauses the Game <br />

<h4> Enemy Movement </h4>
<img src='/images/blinky.png' title='' width='' alt='' /> Blinky attempts to chase Pacman from directly behind.
<img src='/images/pinky.png' title='' width='' alt='' /> Pinky attempts to ambush Pacman from the front, depending on the position can
lead to Pinky chasing from behind.
<img src='/images/clyde.png' title='' width='' alt='' /> Clyde has completely random movement on the board.
<img src='/images/inky.png' title='' width='' alt='' /> Inky can have an equal chance of any of the previous Ghost's movement for
any duration amount of time.


# Demonstration #

## Acquiring Points and Boost
<img src='static/gifs/boost.gif' title='Video Walkthrough' width='' alt='Video Walkthrough' />

## Gameplay
<img src='static/gifs/gameplay2.gif' title='Video Walkthrough' width='' alt='Video Walkthrough' />

## Level Completion and Transitioning
<img src='static/gifs/transition.gif' title='Video Walkthrough' width='' alt='Video Walkthrough' />

## Gameover
<img src='static/gifs/gameover.gif' title='Video Walkthrough' width='' alt='Video Walkthrough' />
