import pygame
import numpy as np
from src import Board

# Instance puzzle generator
board = Board()

# Init font
pygame.font.init()

# Init GUI window
WIDTH = 500
HEIGTH = 650

screen = pygame.display.set_mode((WIDTH, HEIGTH))

# Header
pygame.display.set_caption("Sudoku: Generator & Solver")

# Init
x = 0
y = 0
diff = WIDTH / 9
val = 0

# Generate board
code = board.generate_question_board_code(1)[0]

grid = np.array([int(code[i : i + 1]) for i in range(0, len(code), 1)]).reshape((9, 9)).tolist()

# Set fonts
font_large = pygame.font.SysFont("segoeui", 26)
font_small = pygame.font.SysFont("segoeui", 16)


def get_cord(pos):
    """Get coordinates."""
    global x
    x = pos[0] // diff

    global y
    y = pos[1] // diff


def draw_box():
    """Highlight selected cell."""
    for i in range(2):
        pygame.draw.line(
            screen,
            (255, 113, 113),
            (x * diff - 3, (y + i) * diff),
            (x * diff + diff + 3, (y + i) * diff),
            4,
        )
        pygame.draw.line(
            screen,
            (255, 113, 113),
            ((x + i) * diff, y * diff),
            ((x + i) * diff, y * diff + diff),
            4,
        )


def draw():
    """Draw Sudoku grid lines."""

    # Draw minor lines
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                # Fill blue color in already numbered grid
                pygame.draw.rect(screen, (112, 184, 184), (i * diff, j * diff, diff + 1, diff + 1))

                # Fill grid with default numbers specified
                txt = font_large.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(txt, (i * diff + 22, j * diff + 10))

    # Draw major lines
    for i in range(10):
        if i % 3 == 0:
            thick = 5
        else:
            thick = 1

        pygame.draw.line(screen, (0, 0, 0), (0, i * diff), (WIDTH, i * diff), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * diff, 0), (i * diff, WIDTH), thick)


def draw_val(val):
    """Draw value in cell."""

    value = font_large.render(str(val), 1, (0, 0, 0))
    screen.blit(value, (x * diff + 15, y * diff + 15))


# Exceptions
def raise_invalid():
    print("Invalid.")


def raise_invalid_number():
    print("Invalid number.")


def valid(m, i, j, val):
    """Check entered value validity."""

    for it in range(9):
        if m[i][it] == val:
            return False

        if m[it][j] == val:
            return False

    it = i // 3
    jt = j // 3

    for i in range(it * 3, it * 3 + 3):
        for j in range(jt * 3, jt * 3 + 3):
            if m[i][j] == val:
                return False

    return True


def solve(grid, i, j):
    """Backtracking algorithm: Solve board."""

    while grid[i][j] != 0:
        if i < 8:
            i += 1
        elif i == 8 and j < 8:
            i = 0
            j += 1
        elif i == 8 and j == 8:
            return True

    pygame.event.pump()

    for it in range(1, 10):
        if valid(grid, i, j, it) == True:
            grid[i][j] = it
            global x, y
            x = i
            y = j

            screen.fill((255, 255, 255))
            draw()
            draw_box()
            pygame.display.update()
            pygame.time.delay(20)

            if solve(grid, i, j) == 1:
                return True
            else:
                grid[i][j] = 0

            screen.fill((255, 255, 255))

            draw()
            draw_box()
            pygame.display.update()
            pygame.time.delay(50)

    return False


def instruction():
    """Draw instructions."""
    text_new = font_small.render("Press 'D' te generate new puzzle.", 1, (0, 0, 0))
    text_empty = font_small.render("Press 'R' to clear board.", 1, (0, 0, 0))
    text_solve = font_small.render("Press 'ENTER' to solve visually.", 1, (0, 0, 0))

    screen.blit(text_new, (20, 520))
    screen.blit(text_empty, (20, 540))
    screen.blit(text_solve, (20, 560))


def result():
    """Draw result when solved."""

    text_result = font_large.render("Puzzle solved.", 1, (0, 0, 0))
    screen.blit(text_result, (20, 590))


# GUI persistence loop
run = True
flag1 = 0
flag2 = 0
rs = 0
error = 0

while run:
    # Background color
    screen.fill((255, 255, 255))

    # Iterate over events
    for event in pygame.event.get():
        # Quit event handler
        if event.type == pygame.QUIT:
            run = False

        # Mouse position event handler
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag1 = 1
            pos = pygame.mouse.get_pos()
            get_cord(pos)

        # Key down event handlers
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 1
                flag1 = 1
            if event.key == pygame.K_RIGHT:
                x += 1
                flag1 = 1
            if event.key == pygame.K_UP:
                y -= 1
                flag1 = 1
            if event.key == pygame.K_DOWN:
                y += 1
                flag1 = 1
            if event.key == pygame.K_1:
                val = 1
            if event.key == pygame.K_2:
                val = 2
            if event.key == pygame.K_3:
                val = 3
            if event.key == pygame.K_4:
                val = 4
            if event.key == pygame.K_5:
                val = 5
            if event.key == pygame.K_6:
                val = 6
            if event.key == pygame.K_7:
                val = 7
            if event.key == pygame.K_8:
                val = 8
            if event.key == pygame.K_9:
                val = 9
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                flag2 = 1
            # Clear board
            if event.key == pygame.K_r:
                rs = 0
                error = 0
                flag2 = 0

                grid = [
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
            # Generate new puzzle
            if event.key == pygame.K_d:
                rs = 0
                error = 0
                flag2 = 0

                code = board.generate_question_board_code(difficulty=1)[0]

                grid = (
                    np.array([int(code[i : i + 1]) for i in range(0, len(code), 1)])
                    .reshape((9, 9))
                    .tolist()
                )

    if flag2 == 1:
        if solve(grid, 0, 0) == False:
            error = 1
        else:
            rs = 1

        flag2 = 0

    if val != 0:
        draw_val(val)

        if valid(grid, int(x), int(y), val) == True:
            grid[int(x)][int(y)] = val
            flag1 = 0
        else:
            grid[int(x)][int(y)] = 0
            raise_invalid_number()

        val = 0

    if error == 1:
        raise_invalid()

    if rs == 1:
        result()

    draw()

    if flag1 == 1:
        draw_box()

    instruction()

    # Update GUI state
    pygame.display.update()

# Teardown
pygame.quit()
