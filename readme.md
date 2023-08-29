# The Game of Nim
Play Nim against an AI

## Description
I made this for a class project. The AI's moves are determined by generating a game tree to a set depth, then it evaluates the moves at that depth and searches the game tree for the best sequence of moves

## How to Play
To play the game run Tester.py with three arguments in this order:
1. AI move: 1 to make the AI go first or 2 to make the AI go second
2. Game tree search method: MM to make the AI use the minimax algorithm or AB for Minimax with alpha beta pruning
3. Board size: Must be entered in the format number\*number, for example 7\*7 will create a 7 by 7 board

Here's an example command to run the program:
python Tester.py 1 MM 3*3

Then once it's your turn, enter your move in row/column format. Here's an example move 3/4

At the end of the game a report of how many nodes where expanded in the game tree is added to readme.txt

## Performance
Depending on the size of the board and the depth of the game tree, the AI can take quite a long time to find the next move. To improve the performance of the program use a small board, or change the GAME_TREE_DEPTH constant in Tester.py on line 9 to a smaller value.
