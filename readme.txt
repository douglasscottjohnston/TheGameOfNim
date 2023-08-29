Evaluation function:

Count the number of squares the move blocks (b)
Count the number of remaining empty squares (e)

If b and e are odd then return -b / 10 if max otherwise return b / 10
If b is odd and e is even then return b / 10 if max otherwise return -b / 10
If b is even and e is odd then return b / 10 if max otherwise return -b / 10
If b is even and e is even then return -b / 10 if max otherwise return b / 10

The strategy behind this function comes from Kozma and nim. Only take an even number of marbles
from an odd pile and only take an odd number of stones from an even pile. This should force the other
player into making moves such that the AI will always have the last move

-- Minimax --
*** 6 x 6 Board ***

AI is player 2:
Minimax
Nodes expanded: 9030
Depth level 3

*** 6 x 6 Board ***

AI is player 2:
Minimax
Nodes expanded: 16288
Depth level 3

*** 7 x 6 Board ***

AI is player 2:
Minimax
Nodes expanded: 30154
Depth level 3

*** 5 x 5 Board ***

AI is player 2:
Minimax
Nodes expanded: 1136
Depth level 3

*** 7 x 8 Board ***

AI is player 2:
Minimax
Nodes expanded: 67015
Depth level 3


-- AB Pruning --
*** 6 x 6 Board ***

AI is player 2:
Minimax with AB pruning
Nodes expanded: 33156
Depth level 3

*** 6 x 7 Board ***

AI is player 1:
Minimax with AB pruning
Nodes expanded: 94015
Depth level 3

*** 7 x 7 Board ***

AI is player 1:
Minimax with AB pruning
Nodes expanded: 179352
Depth level 3

*** 8 x 8 Board ***

AI is player 2:
Minimax with AB pruning
Nodes expanded: 388917
Depth level 3

