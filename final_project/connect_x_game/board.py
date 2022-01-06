"""CSC111 Winter 2021 Project, Board file

This file contains the Board class that will be used
in the Connect X game

Copyright and Usage Information
===============================

Base Code was retrieved from: https://github.com/KeithGalli/Connect4-Python
Corresponding Youtube Tutorial: https://youtube.com/watch?v=XpYz-q1lxu8&t=154s

This file is Copyright (c) 2021 Greg Sherman, Ismail Ahmed,
Kevin Vaidyan, and Akash Illangovan."""
from typing import Optional

import pprint
import pygame

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from constants import *


class Board:
    """A representation of the board in Connect X

    Instance Attributes:
        - board: A two dimensional list containing the state
        of the board
        - size: The number of rows and columns in the board
        - width: The width of the game board
        - height: The height of the game board
        - is_red_active: If red is currently active or not

    Representation Invariants:
        - self.size >= 7
    """
    board: list[list[int]]
    size: int
    width: int
    height: int
    is_red_active: bool

    def __init__(self, size: int) -> None:
        """Initialize the board as a size x size board

        Preconditions:
            - size >= 7
        """
        # generate the board. uses a for loop so there are unique lists
        board = [[0] * size]
        for _ in range(size - 1):
            board = board + [[0] * size]
        self.board = board

        self.size = size
        self.width = self.size * SQUARESIZE
        self.height = (self.size + 1) * SQUARESIZE
        self.is_red_active = True

    def drop_piece(self, row: int, col: int, piece: int) -> None:
        """Change the value at self.board[row][col] to correspond to piece
        indicating that a piece has been dropped there."""
        # Replaces the 0 with the corresponding piece
        self.board[row][col] = piece
        # Changes who is active
        self.is_red_active = not self.is_red_active

    def get_valid_moves(self) -> list[tuple[int, int]]:
        """Return a list of all valid moves from the current position."""

        # Check if the top of the board has a 0. If it has a 0, then
        # this column is a valid move. If it is not a 0, that means
        # the entire column is filled.
        valid_col_indices = []
        for i in range(len(self.board[0])):
            if self.board[0][i] == 0:
                valid_col_indices.append(i)

        # Find the corresponding row for each valid column.
        valid_moves = []
        for column in valid_col_indices:
            open_row = self.get_next_open_row(column)
            valid_moves.append((open_row, column))

        return valid_moves

    def get_next_open_row(self, col: int) -> Optional[int]:
        """Return the index of the next open row in the given column"""

        # For the given column, start at the bottom and iterate up
        # until a 0 is found. This is the index of the next open row
        # for this column
        for row in range(self.size - 1, -1, -1):
            if self.board[row][col] == 0:
                return row

        return None

    def winning_move(self, piece: int) -> bool:
        """Return whether a winning move was made by the color
        corresponding to piece"""
        N = int((self.size - 4) - (self.size % 7) / 2)
        for c in range(self.size - N):
            for r in range(self.size):
                if all(self.board[r][c + n] == piece for n in range(N + 1)):
                    return True

        # Check vertical locations for win
        for c in range(self.size):
            for r in range(self.size - N):
                if all(self.board[r + n][c] == piece for n in range(N + 1)):
                    return True

        # Check positively sloped diagonals
        for c in range(self.size - N):
            for r in range(self.size - N):
                if all(self.board[r + n][c + n] == piece for n in range(N + 1)):
                    return True

        # Check negatively sloped diagonals
        for c in range(self.size - N):
            for r in range(N, self.size):
                if all(self.board[r - n][c + n] == piece for n in range(N + 1)):
                    return True

        return False

    def get_winner(self) -> Optional[str]:
        """Checks if the current game state has a winner or is a draw.

        Return None if the game has not ended."""
        if self.winning_move(1):
            return 'Red'
        elif self.winning_move(2):
            return 'Yellow'
        # if no valid moves remain
        elif self.get_valid_moves() == []:
            return 'Draw'
        else:
            return None

    def print_board(self) -> None:
        """Print the board in matrix style to the console"""
        pprint.pprint(self.board)

    def draw_board(self, screen: pygame.Surface) -> None:
        """Draw the current board on the given pygame screen"""

        # Draw an empty board
        for c in range(self.size):
            for r in range(self.size):
                pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE,
                                                SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, BLACK, (
                    int(c * SQUARESIZE + SQUARESIZE / 2),
                    int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

        # Iterate through the board instance attribute to determine where
        # to draw the pieces that have been dropped
        for c in range(self.size):
            for r in range(self.size):
                if self.board[r][c] == 1:
                    pygame.draw.circle(screen, RED, (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        self.height - int((self.size - r - 1)
                                          * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(screen, YELLOW, (
                        int(c * SQUARESIZE + SQUARESIZE / 2), self.height - int(
                            (self.size - r - 1) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
        pygame.display.update()


#
# def run_games(n: int, red: Player, yellow: Player, game_state: Board, show_stats: bool = True) \
#       -> None:
#     """Run n games using the given Players.
#     """
#     stats = {'Red': 0, 'Yellow': 0, 'Draw': 0}
#     results = []
#     for i in range(0, n):
#         winner, _ = run_game(red, yellow, game_state)
#         stats[winner] += 1
#         results.append(winner)
#
#         print(f'Game {i} winner: {winner}')
#
#     for outcome in stats:
#         print(f'{outcome}: {stats[outcome]}/{n} ({100.0 * stats[outcome] / n:.2f}%)')
#
#     if show_stats:
#         plot_game_statistics(results)


def plot_game_statistics(results: list[str]) -> None:
    """Plot the outcomes and win probabilities for a given list of Minichess game results.
    """
    outcomes = [1 if result == 'Red' else 0 for result in results]

    cumulative_win_probability = [sum(outcomes[0:i]) / i for i in range(1, len(outcomes) + 1)]
    rolling_win_probability = \
        [sum(outcomes[max(i - 50, 0):i]) / min(50, i) for i in range(1, len(outcomes) + 1)]

    fig = make_subplots(rows=2, cols=1)
    fig.add_trace(go.Scatter(y=outcomes, mode='markers',
                             name='Outcome (1 = Red win, 0 = Draw/Yellow win)'),
                  row=1, col=1)
    fig.add_trace(go.Scatter(y=cumulative_win_probability, mode='lines',
                             name='Red win percentage (cumulative)'),
                  row=2, col=1)
    fig.add_trace(go.Scatter(y=rolling_win_probability, mode='lines',
                             name='Red win percentage (most recent 50 games)'),
                  row=2, col=1)
    fig.update_yaxes(range=[0.0, 1.0], row=2, col=1)

    fig.update_layout(title='Connect X Game Results', xaxis_title='Game')
    fig.show()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['sys', 'math', 'pygame', 'constants', 'board',
                          'pprint', 'plotly', 'players', 'tree_generation',
                          'game_tree', 'copy', 'random', 'menu'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'E1136', 'E9999']
    })
