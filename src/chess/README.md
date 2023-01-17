# Background

Someone sent me this question:

![question photo](https://github.com/sujaldev/skia-animations/blob/main/docs/chess_question.png?raw=True)

so I decided to write a program to solve this (not specifically this but any configuration).

# Solution

While I don't have the time to write a full explanation right now, here's a photo that made me realise the solution:

![solution hint](https://github.com/sujaldev/skia-animations/blob/main/docs/chess_solution.png?raw=True)

You just have to mark each of the cells with the minimum number of moves required to get there and each cell keeps track
of the last cell from where the knight made it to the current cell. \
This can be achieved by calculating all possible moves of the knight in its starting position and then marking the
resulting cells as count 1 and linking the previous cell as the knight's cell itself. Then calculate all possible moves
from all the cells marked 1 and mark the resulting cells as 2 (if and only if they are not already marked) and link back
to previous cells. Continue doing this until the target is reached. This ensures the minimum number of moves to the
target.

# Future plans

Currently, the program just shows you the final output and plays no animation, I want to entirely rewrite this to show
the algorithm at play and then finally when it's done, animate the knight moving to the target (and also because the
code is very messy right now). But as I said, I currently don't have the time, I have exams coming up.