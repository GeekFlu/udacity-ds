"""
Exercise 2

In the next exercise, you will write a function that checks sudoku squares for correctness.

Sudoku is a logic puzzle where a game is defined by a partially filled 9 x 9 square of digits where each square contains
one of the digits 1, 2, 3, 4, 5, 6, 7, 8, 9. For this question we will generalize and simplify the game.

Define a procedure, check_sudoku, that takes as input a square list of lists representing an n x n sudoku puzzle
solution and returns the boolean True if the input is a valid sudoku square and returns the boolean False otherwise.

A valid sudoku square satisfies these two properties:

    Each column of the square contains each of the whole numbers from 1 to n exactly once.

    Each row of the square contains each of the whole numbers from 1 to n exactly once.

You may assume that the input is square and contains at least one row and column.

"""


def check_sudoku(matrix):
    if len(matrix) == 0:
        return False

    rows = len(matrix)
    cols = len(matrix[0])

    if rows != cols:
        return False

    isValid = True
    for i in range(0, rows):
        generated = [x for x in range(1, cols + 1)]
        for j in range(0, cols):
            if matrix[i][j] in generated:
                generated.remove(matrix[i][j])
        if len(generated) != 0:
            isValid = False
            break

    if isValid:
        for i in range(0, rows):
            generated = [x for x in range(1, cols + 1)]
            for j in range(0, cols):
                if matrix[j][i] in generated:
                    generated.remove(matrix[j][i])
            if len(generated) != 0:
                isValid = False
                break

    return isValid


if __name__ == "__main__":
    generated_ = [x for x in range(1, 5)]
    correct = [[1, 2, 3],
               [2, 3, 1],
               [3, 1, 2]]

    incorrect = [[1, 2, 3, 4],
                 [2, 3, 1, 3],
                 [3, 1, 2, 3],
                 [4, 4, 4, 4]]

    incorrect2 = [[1, 2, 3, 4],
                  [2, 3, 1, 4],
                  [4, 1, 2, 3],
                  [3, 4, 1, 2]]

    incorrect3 = [[1, 2, 3, 4, 5],
                  [2, 3, 1, 5, 6],
                  [4, 5, 2, 1, 3],
                  [3, 4, 5, 2, 1],
                  [5, 6, 4, 3, 2]]

    incorrect4 = [['a', 'b', 'c'],
                  ['b', 'c', 'a'],
                  ['c', 'a', 'b']]

    incorrect5 = [[1, 1.5],
                  [1.5, 1]]

    # Define a function check_sudoku() here:

    # print(check_sudoku(incorrect))
    # >>> False
    print(check_sudoku(correct))
    # >>> True
    print(check_sudoku(incorrect2))
    # >>> False
    print(check_sudoku(incorrect3))
    # >>> False
    print(check_sudoku(incorrect4))
    # >>> False
    print(check_sudoku(incorrect5))
    # >>> False
