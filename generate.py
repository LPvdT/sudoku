import yaml
import numpy as np
from rich.console import Console
from src import Board

if __name__ == "__main__":
    # Init
    console = Console()
    board = Board()

    # Parse difficulty
    try:
        difficulties = yaml.load(open("./settings.yml"), Loader=yaml.FullLoader)

        difficulty = difficulties["difficulty_choice"]
    except FileNotFoundError:
        console.log(
            "[bold red]WARNING:[/bold red] 'settings.yml' not found. Defaulting to 1 (medium difficulty)."
        )

        difficulty = 1

    # Puzzle codes
    puzzle = board.generate_question_board_code(difficulty)

    # Puzzle
    puzzle_grid = np.array(
        [int(puzzle[0][i : i + 1]) for i in range(0, len(puzzle[0]), 1)]
    ).reshape((9, 9))

    console.rule(f"Puzzle - Difficulty: '{difficulties['difficulty_levels'][difficulty]}'")
    console.print(f"\nCode: {puzzle[0]}")
    console.print(f"\nGrid:\n{puzzle_grid}")

    # Solution
    solution_grid = np.array(
        [int(puzzle[1][i : i + 1]) for i in range(0, len(puzzle[1]), 1)]
    ).reshape((9, 9))

    console.rule(f"Solution - Difficulty: '{difficulties['difficulty_levels'][difficulty]}'")
    console.print(f"\nCode: {puzzle[1]}")
    console.print(f"\nGrid:\n{solution_grid}")
    console.print(f"\nNumber of possible solutions: {len(board.find_number_of_solutions())}")
