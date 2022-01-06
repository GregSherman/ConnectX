"""CSC111 Winter 2021 Project, Tree generator file

This file contains functions used to generate trees of games
of Connect X.

Copyright and Usage Information
===============================

Base code for these two functions are retrieved from Assignment 2

This file is Copyright (c) 2021 Greg Sherman, Ismail Ahmed,
Kevin Vaidyan, and Akash Illangovan."""
import copy

from typing import Any
from players import ExploringPlayer, RandomPlayer, run_game

import board
import game_tree


def generate_complete_game_tree(root_move: tuple[int, int], game_state: board.Board, d: int) \
        -> game_tree.GameTree:
    """Generate a complete game tree of depth d for all valid moves from the current game_state.

    Preconditions:
        - d >= 0
        - root_move == GAME_START_MOVE or root_move is a valid Connect X move
    """
    # Change the player's move for the next level depth
    red = game_state.is_red_active
    if red:
        piece = 1
    else:
        piece = 2

    # Apply a win probability depending on the game state winner
    win_probability = 0.0
    if game_state.get_winner() == 'Red':
        win_probability = 1.0

    # Make a node in the tree based off of the root move, who's turn it is,
    # and the win probability
    tree = game_tree.GameTree(root_move, red, win_probability)

    # Base case, returns the tree and adds it as a leaf
    if d == 0:
        return tree

    # Recursive step, makes a move and calls this function to add a subtree to
    # the tree created above.
    else:
        # Get the valid moves from the current state
        moves = game_state.get_valid_moves()

        for move in moves:
            if game_state.board[move[0]][move[1]] == 0:
                # copy the game state and generate a new subtree
                game_copy = copy.deepcopy(game_state)
                game_copy.drop_piece(move[0], move[1], piece)
                tree.add_subtree(generate_complete_game_tree(move, game_copy, d - 1))
        return tree


def run_learning_algorithm(exploration_probabilities: list[float], size: int) -> Any:
    """Play a sequence of Connect X games using an ExploringPlayer as the Red player.
    """
    # Start with a GameTree in the initial state
    tree = game_tree.GameTree()

    # Play games using the GreedyRandomPlayer and update the GameTree after each one
    results_so_far = []

    for i in range(len(exploration_probabilities)):

        red = ExploringPlayer(tree, exploration_probabilities[i])
        yellow = RandomPlayer()
        winner, move_sequence = run_game(red, yellow, size)

        red_win_probability = 0.0
        if winner == 'Red':
            red_win_probability = 1.0

        results_so_far.append(winner)
        tree.insert_move_sequence(move_sequence, red_win_probability)

    # board.plot_game_statistics(results_so_far)

    return (tree, results_so_far)


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
