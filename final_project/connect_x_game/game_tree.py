"""CSC111 Winter 2021 Project, GameTree file

This file contains the GameTree class that will be used
to map out games of Connect X.

Copyright and Usage Information
===============================

Base code for GameTree is retrieved from Assignment 2.

This file is Copyright (c) 2021 Greg Sherman, Ismail Ahmed,
Kevin Vaidyan, and Akash Illangovan."""
from __future__ import annotations
from typing import Optional

GAME_START_MOVE = (-1, -1)


class GameTree:
    """A decision tree for Connect X moves.

    Each node in the tree stores a Connect X move and a boolean representing whether
    the current player (who will make the next move) is Red or Yellow.

    Many methods are similar to that of Assignment 2. They have been modified
    to work properly with Connect X.

    Instance Attributes:
      - move: the current Connect X move. (-1, -1) as the root move.
      - is_red_move: True if Red is to make the next move after this, False otherwise
      - red_win_probability: the probability that red will win with the root move

    Representation Invariants:
        - self.move == GAME_START_MOVE or self.move is a valid Connect X move
        - self.move != GAME_START_MOVE or self.is_red_move == True
    """
    move: tuple[int, int]
    is_red_move: bool
    red_win_probability: float

    # Private Instance Attributes:
    #  - : the subtrees of this tree, which represent the game trees after a possible
    #      move by the current player
    _subtrees: list[GameTree]

    def __init__(self, move: tuple[int, int] = GAME_START_MOVE,
                 is_red_move: bool = True, red_win_probability: Optional[float] = 0.0) -> None:
        """Initialize a new game tree."""
        self.move = move
        self.is_red_move = is_red_move
        self._subtrees = []
        self.red_win_probability = red_win_probability

    def __str__(self) -> str:
        """Return a string representation of this tree."""
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter."""
        if self.is_red_move:
            turn_desc = "Red's move"
        else:
            turn_desc = "Yellow's move"
        move_desc = f'{str(self.move)} -> {turn_desc} {self.red_win_probability}\n'
        s = '  ' * depth + move_desc
        if self._subtrees == []:
            return s
        else:
            for subtree in self._subtrees:
                s += subtree._str_indented(depth + 1)
            return s

    # def make_board(self, move_sequence: list[tuple], size: int) -> board.Board:
    #     """Create a Board() instance from the given list of moves.
    #
    #     Useful for testing whether the game state is a winner or not
    #
    #     Preconditions:
    #         - size >= 7
    #     """
    #     # Create an empty board instance
    #     new_board = board.Board(size)
    #     piece = 1
    #
    #     # Drop each move into the board in order
    #     for move in move_sequence:
    #         new_board.drop_piece(move[0], move[1], piece)
    #         if piece == 1:
    #             piece = 2
    #         else:
    #             piece = 1
    #     return new_board

    def get_subtrees(self) -> list[GameTree]:
        """Return the subtrees of this game tree."""
        return self._subtrees

    def find_subtree_by_move(self, move: tuple[int, int]) -> Optional[GameTree]:
        """Return the subtree corresponding to the given move.

        Return None if no subtree corresponds to that move.
        """
        for subtree in self._subtrees:
            if subtree.move == move:
                return subtree

        return None

    def add_subtree(self, subtree: GameTree) -> None:
        """Add a subtree to this game tree."""
        self._subtrees.append(subtree)
        # Update win probability after subtree has been added
        self._update_red_win_probability()

    def insert_move_sequence(self, moves: list[tuple[int, int]],
                             win_probability: Optional[float] = 0.0) -> None:
        """Insert the given sequence of moves into this tree.

        The inserted moves form a chain of descendants, where:
            - moves[0] is a child of this tree's root
            - moves[1] is a child of moves[0]
            - moves[2] is a child of moves[1]
            - etc.
        """
        # Do not run with an empty list
        if not moves:
            pass
        else:

            # Takes m steps
            reversed_moves = list(reversed(moves))

            # Takes at most m + n steps
            self.recursive_helper(reversed_moves, win_probability)

            # Update the win probability one last time
            self._update_red_win_probability()

    def recursive_helper(self, moves: list[tuple[int, int]], win_probability: float) -> None:
        """A recursive helper function to assist insert_move_sequence in adding moves
        to the game tree in worst case Theta(m + n) running time.
        """
        if moves:
            # The call to find_subtree_by_move takes at most n steps
            # across all recursive calls

            # All other code takes constant time
            subtree = self.find_subtree_by_move(moves[-1])
            if not self._subtrees or subtree is None:
                if self.is_red_move:
                    self.add_subtree(GameTree(moves.pop(), False, win_probability))
                else:
                    self.add_subtree(GameTree(moves.pop(), True, win_probability))

                self._subtrees[-1].recursive_helper(moves, win_probability)
                self._update_red_win_probability()

            else:
                moves.pop()
                subtree.recursive_helper(moves, win_probability)
                self._update_red_win_probability()

    def _update_red_win_probability(self) -> None:
        """Recalculate the red win probability of this tree.

        Every subtree's win probability has the value as the sum
        of all of its subtrees.
        """
        # Does nothing when self is a leaf
        if self._subtrees == []:
            pass

        # Let each subtree node be the sum of every subtree below it.
        elif self._subtrees != []:
            count = 0.0
            for subtree in self._subtrees:
                count += subtree.red_win_probability
            self.red_win_probability = count


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
