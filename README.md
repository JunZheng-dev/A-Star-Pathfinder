# A* Pathfinder Visualizer
<h3>Introduction</h3>
This program is a visualizer for the A* pathfinding algorithm. The GUI is produced using the <b>pygame</b> library.</br>
The algorithm is similar to Dijkstra's algorithm but uses a heuristic, the distance between the nodes, to better explore.</br>
The algorithm can travel diagonally or in a straight direction by 1 square at a time.

#### Controls
* **Left click** on a tile to place an obstacle
* **Right click** on an obstacle to remove it
* **Scroll wheel click** to place the start block
* **Scroll wheel click** a second time to place the end block
* **Scroll wheel click** on a start/end block to remove it
* Press **backspace** to clear the grid
* Press **spacebar** to begin the pathfinding process (then click it again after it has finished to continue)
* Grid dimensions, size, and colors as well as delay can be changed in the code

#### Types of Blocks
* **Black** - Obstacle
* **White** - Empty
* **Red** - Start
* **Blue** - End
* **Yellow** - Explored Nodes
* **Green** - Path

<h3>Preview</h3>
<kbd>
<img src="https://github.com/JunZheng-dev/A-Star-Pathfinder-Visualizer/blob/master/preview/1.gif"/ width="200px">
</kbd>
<kbd>
<img src="https://github.com/JunZheng-dev/A-Star-Pathfinder-Visualizer/blob/master/preview/2.gif"/ height="200px">
</kbd>
