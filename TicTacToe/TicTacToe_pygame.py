import sys
import random
import pygame

# CONSTANTS

WIDTH: int = 600
HEIGHT: int = 600

ROWS: int = 3
COLS: int = 3
SQSIZE: int = WIDTH // COLS

LINE_WIDTH: int = 15
CIRC_WIDTH: int = 15
CROSS_WIDTH: int = 20

RADIUS: int = SQSIZE // 4

OFFSET: int = 50

BG_COLOR: tuple = (28, 170, 156)
LINE_COLOR: tuple = (23, 145, 135)
CIRC_COLOR: tuple = (239, 231, 200)
CROSS_COLOR: tuple = (66, 66, 66)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TIC TAC TOE")
screen.fill(BG_COLOR)


class Board:
    def __init__(self) -> None:
        self.squares: list[list[int]] = [[0, 0, 0],
                                         [0, 0, 0],
                                         [0, 0, 0]
                                         ]
        self.marked_sqrs: int = 0
        self.draw_board()

    def mark_sqr(self, row: int, col: int, player: int) -> None:
        self.squares[row][col]: int = player
        self.marked_sqrs += 1

    def empty_sqr(self, row: int, col: int) -> bool:
        return self.squares[row][col] == 0

    def get_empty_sqrs(self) -> list[tuple[int, int]]:
        """Returning a list of tuple of empty sqrs"""
        return [(i, j) for j in range(3) for i in range(3) if self.empty_sqr(i, j)]

    @staticmethod
    def draw_board() -> None:
        screen.fill(BG_COLOR)

        # Vertical
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (2 * SQSIZE, 0), (2 * SQSIZE, HEIGHT), LINE_WIDTH)

        # Horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQSIZE), (WIDTH, 2 * SQSIZE), LINE_WIDTH)

    def draw_fig(self, row: int, col: int, player: int) -> None:
        if player == 1:
            self.draw_croos(row, col)
        elif player == 2:
            self.draw_circle(row, col)

    @staticmethod
    def draw_croos(row: int, col: int) -> None:
        # draw cross
        # descending line
        start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
        end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
        pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
        # ascending line
        start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
        end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
        pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

    @staticmethod
    def draw_circle(row: int, col: int) -> None:
        # draw circle
        center: tuple[int, int] = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
        pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)


class Game:
    def __init__(self) -> None:
        self.board: Board = Board()
        self.player: int = 1  # 1-cross 2-circles

    def next_turn(self) -> None:
        self.player: int = self.player % 2 + 1

    def computer_choice(self) -> None:
        empty_case: list[tuple[int, int]] = self.board.get_empty_sqrs()
        choice: tuple[int, int] = random.choice(empty_case)
        self.make_move(choice[0], choice[1], 2)

    def make_move(self, row: int, col, player) -> None:
        self.board.mark_sqr(row, col, self.player)
        self.board.draw_fig(row, col, player)
        self.is_a_winner()
        self.next_turn()

    def is_a_winner(self) -> bool:
        color: tuple = (CROSS_COLOR if self.player == 2 else CIRC_COLOR)

        for i in range(3):
            # Horizontal
            if self.board.squares[i][0] == self.board.squares[i][1] == self.board.squares[i][2] != 0:
                pygame.draw.line(screen, color, (0, (0.5 + i) * SQSIZE), (WIDTH, (0.5 + i) * SQSIZE), LINE_WIDTH)
                return True
            # Vertical
            if self.board.squares[0][i] == self.board.squares[1][i] == self.board.squares[2][i] != 0:
                pygame.draw.line(screen, color, ((0.5 + i) * SQSIZE, 0), ((0.5 + i) * SQSIZE, HEIGHT), LINE_WIDTH)
                return True

        # Diagonal
        if self.board.squares[0][0] == self.board.squares[1][1] == self.board.squares[2][2] != 0:
            pygame.draw.line(screen, color, (0, 0), (WIDTH, HEIGHT), LINE_WIDTH)
            return True

        if self.board.squares[0][2] == self.board.squares[1][1] == self.board.squares[2][0] != 0:
            pygame.draw.line(screen, color, (WIDTH, 0), (0, HEIGHT), LINE_WIDTH)
            return True

    def is_game_over(self) -> bool:
        return self.board.marked_sqrs == 9 or self.is_a_winner()

    def reset(self) -> None:
        self.__init__()

    def handle_event(self, events) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()

            if event.type == pygame.MOUSEBUTTONDOWN and not self.is_game_over():
                pos: tuple[int, int] = event.pos
                row: int = pos[1] // SQSIZE
                col: int = pos[0] // SQSIZE

                if self.board.empty_sqr(row, col):
                    self.make_move(row, col, 1)
                    if not self.is_game_over():
                        self.computer_choice()


def main() -> None:
    game: Game = Game()

    while True:
        pygame.time.Clock().tick(60)
        if game.is_game_over():
            game.is_a_winner()
        game.handle_event(pygame.event.get())

        pygame.display.flip()


if __name__ == '__main__':
    main()
