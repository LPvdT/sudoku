import copy
import random
from typing import Optional, List


class Board:
    """Sudoku board object."""

    def __init__(self, code: Optional[str] = None) -> None:
        """Initilise the board object"""

        self.__reset_board()

        # Create a board from optional code
        if code:
            self.code = code

            for row in range(9):
                for col in range(9):
                    self.board[row][col] = int(code[0])
                    code = code[1:]
        else:
            self.code = None

    def board_to_code(self, input_board: Optional[list] = None) -> str:
        """Convert a board represented by a list into a string representation."""

        if input_board:
            _code = "".join([str(i) for j in input_board for i in j])
            return _code
        else:
            self.code = "".join([str(i) for j in self.board for i in j])
            return self.code

    def find_spaces(self) -> bool:
        """Finds the first empty space, represented by a 0, on the current board"""

        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == 0:
                    return (row, col)

        return False

    def check_space(self, num: int, space: list) -> bool:
        """Returns a bool, depending if the number passed in can exist in a space on the current board, provided by the tuple argument"""

        # Check to see if space is a number already
        if not self.board[space[0]][space[1]] == 0:
            return False

        # Check to see if number is already in row
        for col in self.board[space[0]]:
            if col == num:
                return False

        # Check to see if number is already in column
        for row in range(len(self.board)):
            if self.board[row][space[1]] == num:
                return False

        _internal_box_row = space[0] // 3
        _internal_box_col = space[1] // 3

        # Check to see if internal box already has number
        for i in range(3):
            for j in range(3):
                if self.board[i + (_internal_box_row * 3)][j + (_internal_box_col * 3)] == num:
                    return False

        return True

    def solve(self) -> bool:
        """Solves the current board using backtracking."""

        _spaces_available = self.find_spaces()

        if not _spaces_available:
            return True
        else:
            row, col = _spaces_available

        for n in range(1, 10):
            if self.check_space(n, (row, col)):
                self.board[row][col] = n

                if self.solve():
                    return self.board

                self.board[row][col] = 0

        return False

    def solve_for_code(self) -> str:
        """Calls the solve method and returns the solved board in a string code format."""

        return self.board_to_code(self.solve())

    def generate_question_board_code(self, difficulty: int) -> tuple:
        """Calls the generate_question_board method and returns a question board and its solution in code format."""

        self.board, _solution_board = self.generate_question_board(
            self.__generate_random_complete_board(), difficulty
        )
        return self.board_to_code(), self.board_to_code(_solution_board)

    def generate_question_board(self, full_board: str, difficulty: int) -> tuple:
        """Returns a randomly generated question board and the solution to the same board, the difficulty represents the number of number squares
		removed from the board."""

        self.board = copy.deepcopy(full_board)

        if difficulty == 0:
            _squares_to_remove = 36
        elif difficulty == 1:
            _squares_to_remove = 46
        elif difficulty == 2:
            _squares_to_remove = 52
        else:
            return

        _counter = 0
        while _counter < 4:
            _r_row = random.randint(0, 2)
            _r_col = random.randint(0, 2)
            if self.board[_r_row][_r_col] != 0:
                self.board[_r_row][_r_col] = 0
                _counter += 1

        _counter = 0
        while _counter < 4:
            _r_row = random.randint(3, 5)
            _r_col = random.randint(3, 5)
            if self.board[_r_row][_r_col] != 0:
                self.board[_r_row][_r_col] = 0
                _counter += 1

        _counter = 0
        while _counter < 4:
            _r_row = random.randint(6, 8)
            _r_col = random.randint(6, 8)
            if self.board[_r_row][_r_col] != 0:
                self.board[_r_row][_r_col] = 0
                _counter += 1

        _squares_to_remove -= 12
        _counter = 0
        while _counter < _squares_to_remove:
            _row = random.randint(0, 8)
            _col = random.randint(0, 8)

            if self.board[_row][_col] != 0:
                n = self.board[_row][_col]
                self.board[_row][_col] = 0

                if len(self.find_number_of_solutions()) != 1:
                    self.board[_row][_col] = n
                    continue

                _counter += 1

        return self.board, full_board

    def __generate_random_complete_board(self) -> bool:
        """Returns a full randomly generated board."""

        self.__reset_board()

        _l = list(range(1, 10))
        for row in range(3):
            for col in range(3):
                _num = random.choice(_l)
                self.board[row][col] = _num
                _l.remove(_num)

        _l = list(range(1, 10))
        for row in range(3, 6):
            for col in range(3, 6):
                _num = random.choice(_l)
                self.board[row][col] = _num
                _l.remove(_num)

        _l = list(range(1, 10))
        for row in range(6, 9):
            for col in range(6, 9):
                _num = random.choice(_l)
                self.board[row][col] = _num
                _l.remove(_num)

        return self.__generate_cont()

    def __generate_cont(self) -> bool:
        """Uses recursion to finish generating a full board, whilst also making sure the board is solvable by calling the solve method."""

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 0:
                    _num = random.randint(1, 9)

                    if self.check_space(_num, (row, col)):
                        self.board[row][col] = _num

                        if self.solve():
                            self.__generate_cont()
                            return self.board

                        self.board[row][col] = 0

        return False

    def find_number_of_solutions(self) -> list:
        """Finds the number of solutions to the current board and returns a list of all the solutions in code format."""

        _z = 0
        _list_of_solutions = []

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 0:
                    _z += 1

        for i in range(1, _z + 1):
            _board_copy = copy.deepcopy(self)

            _row, _col = self.__find_spaces_number_solutions(_board_copy.board, i)
            _board_copy_solution = _board_copy.__solve_find_number_solutions(_row, _col)

            _list_of_solutions.append(self.board_to_code(input_board=_board_copy_solution))

        return list(set(_list_of_solutions))

    def __find_spaces_number_solutions(self, board: str, h: int) -> bool:
        """Finds the first empty space in the board given as the argument, used within the find_number_of_solutions method."""

        _k = 1
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == 0:
                    if _k == h:
                        return (row, col)

                    _k += 1

        return False

    def __solve_find_number_solutions(self, row: int, col: int) -> bool:
        """Solves the current board using recursion by starting at the position determined by the row and col, used within the find_number_of_solutions method."""

        for n in range(1, 10):
            if self.check_space(n, (row, col)):
                self.board[row][col] = n

                if self.solve():
                    return self.board

                self.board[row][col] = 0

        return False

    def __reset_board(self) -> List[list]:
        """Resets the current board to an empty state."""

        self.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        return self.board
