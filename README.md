# Somewhat_Square_Sudoku_Jane_Street_Puzzle

My solution to the January 2025 "Somewhat Square Sudoku" Jane Street puzzle follows the following process:

1. Defining a function that finds the GCD of an array of numbers. This function allows for calculating the GCD of the sudoku board by treating each row of the board as a number in the input array of the function.
2. Find all possible permutations of a subset of 9 unique values from 0-9 for the first row of the sudoku board, while adhereing to rules of sudoku.
3. For the rest of the rows, all the possible combinations of the board are explored while adhereing to the rules of sudoku for each unique board. To reduce runtime and file sizes, the GCD is calculated for each unique board as the combinations are explored at each row to filter boards that don't meet a certain GCD threshold.
4. Once all the rows are completed, the "boards_with_gcd.json" file found in the "complete_board_combination.zip" file is opened in the "board_highest_GCD.py" file to find the board with the highest GCD. The result showed that the board with the highest GCD value of 739 had a middle row of: ['2', '8', '3', '9', '5', '0', '6', '1', '7']

NOTE: the runtime for the whole process takes roughly 12 hours
