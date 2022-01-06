"""CSC111 Winter 2021 Project, Player file

This file contains the Player classes that will be used
in the Connect X game.

MonteCarloFreeVersion inspired by Monte Carlo Search Trees (MCTS).
MCTS became too difficult to implement so MonteCarloFreeVersion takes
inspiration from MCTS selection and rollout.

Copyright and Usage Information
===============================

RandomPlayer and ExploringPLayer retrieved from Assignment 2.

This file is Copyright (c) 2021 Greg Sherman, Ismail Ahmed,
Kevin Vaidyan, and Akash Illangovan."""
import random
import copy

from typing import Optional
from board import Board

import game_tree


class Player:
    """The Player abstract class"""
    def make_move(self, game: Board, previous_move: Optional[tuple[int, int]],
                  num_sims: Optional[int] = None) -> tuple[int, int]:
        """The Player abstract make_move method"""
        raise NotImplementedError


class RandomPlayer(Player):
    """A Connect X AI whose strategy is always picking a random move."""

    def make_move(self, game: Board, previous_move: Optional[tuple[int, int]],
                  num_sims: Optional[int] = None) -> tuple[int, int]:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made. Though previous_move is redundant here.

        Preconditions:
            - game.get_valid_moves() != []
        """
        possible_moves = game.get_valid_moves()
        return random.choice(possible_moves)


class ExploringPlayer(Player):
    """A Connect X player that plays greedily some of the time, and randomly some of the time.
    """
    # Private Instance Attributes:
    #   - _game_tree:
    #       The GameTree that this player uses to make its moves. If None, then this
    #       player just makes random moves.
    _game_tree: Optional[game_tree.GameTree]
    _exploration_probability: float

    def __init__(self, gametree: game_tree.GameTree, exploration_probability: float) -> None:
        """Initialize this player."""
        self._game_tree = gametree
        self._exploration_probability = exploration_probability

    def make_move(self, game: Board, previous_move: Optional[tuple[int, int]],
                  num_sims: Optional[int] = None) -> tuple[int, int]:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        # First let the current tree be the subtree that has the root move
        # of the previous move (or None if there is no such subtree)
        if previous_move is not None and self._game_tree is not None:
            self._game_tree = self._game_tree.find_subtree_by_move(previous_move)

        # If the current tree is None (it can be none from the code above or
        # if it was None from the previous move) or it is a leaf, make a random
        # move from the valid moves.
        if self._game_tree is None or self._game_tree.get_subtrees() == []:
            new_move = random.choice(game.get_valid_moves())
            return new_move

        # If the current tree is not empty and it has subtrees, choose a random
        # number and decide the next move based on if the random number is less
        # than or greater than self._exploration_probability.
        else:
            random_p = random.uniform(0, 1)

            # If random_p is less than self._exploration_probability, choose
            # a random move from all valid moves and update the tree to be either
            # None or the subtree that contains the random move picked.
            if random_p < self._exploration_probability:
                new_move = random.choice(game.get_valid_moves())
                new_tree = None

                for subtree in self._game_tree.get_subtrees():
                    if subtree.move == new_move:
                        new_tree = subtree

                self._game_tree = new_tree
                return new_move

            # Otherwise, choose the subtree with the highest or lowest white_win_probability
            # depending on who's turn it is. If there is a tie, it picks the left most
            # subtree because of the strict inequalities.
            else:
                good_tree = self._game_tree.get_subtrees()[0]
                str_representation = self.make_move_helper(good_tree).move
                tuple_representation = (int(str_representation[0]),
                                        int(str_representation[1]))
                return tuple_representation

    def make_move_helper(self, good_tree: game_tree.GameTree()) -> game_tree.GameTree():
        """Works as a helper to self.make_move()

        This function chooses the subtree of self and reassigns self to
        that subtree based on the red_win_probabilities.

        Preconditions:
            - good_tree is not None
        """
        # Loop through the subtrees if it is white's move and pick the
        # subtree with the highest white_win_probability.
        if self._game_tree.is_red_move:
            for subtree in self._game_tree.get_subtrees():
                if subtree.red_win_probability > good_tree.red_win_probability:
                    good_tree = subtree

        # Loop through the subtrees if it is black's move and pick the
        # subtree with the lowest white_win_probability.
        else:
            for subtree in self._game_tree.get_subtrees():
                if subtree.red_win_probability < good_tree.red_win_probability:
                    good_tree = subtree

        # Reassign the game tree to be the newly picked subtree and return that
        # subtree's move.
        self._game_tree = good_tree
        return self._game_tree


class SabotagePlayer(Player):
    """A Connect X player that is designed to Sabotage the user 100% of the time.

    If the user can win in one move, Sabotage player will stop that move. If the next
    move of Sabotage player can be a winning one, choose that move."""

    def make_move(self, game: Board, previous_move: Optional[tuple[int, int]],
                  num_sims: Optional[int] = None) -> tuple[int, int]:
        """Return the move that is either the winning move or the move that stops
        the user from winning."""

        # the moves where the user wins after this move
        bad_moves = []
        # the moves where the ai wins
        good_moves = []

        # iterate through every valid next move
        for move in game.get_valid_moves():
            game_copy = copy.deepcopy(game)

            # simulate this move being played
            game_copy.drop_piece(move[0], move[1], 1)

            # if this move causes the ai to win, return this move.
            if game_copy.get_winner() == 'Red':
                return move

            # if this move is not a winning move, check if yellow can win after this move
            for yellow_move in game_copy.get_valid_moves():
                game_copy_copy = copy.deepcopy(game_copy)
                game_copy_copy.drop_piece(yellow_move[0], yellow_move[1], 2)

                # if yellow can win after this move, append it to the bad moves
                if game_copy_copy.get_winner() == 'Yellow' or game_copy_copy.get_winner() == 'Draw':
                    bad_moves.append(move)

        # all good moves are those in valid moves which are not bad moves
        for move in game.get_valid_moves():
            if move not in bad_moves:
                good_moves.append(move)

        # if there are multiple good moves, just pick any random one
        if good_moves != []:
            return random.choice(good_moves)

        # if all moves are bad, the ai loses no matter the move, so return a random move
        return random.choice(game.get_valid_moves())


class MonteCarloFreeVersion(Player):
    """A Monte Carlo Tree Search inspired AI for Connect X."""

    def make_move(self, game: Board, previous_move: Optional[tuple[int, int]],
                  num_sims: Optional[int] = None) -> tuple[int, int]:
        """Returns the best move to make as the next move in Connect X

        This function takes the current game state of the connect X board and selects
        one of the possible moves. Then, 200 games are simulated from that move. Every
        winning game has value 1, every draw has value 0, every loss has value -1. The
        possible move that was selected then updates from its subtrees the total score of
        that move (the sum of all game results). This is then repeated for each possible move.

        Return the possible move with the highest results score."""

        # create a new tree instance
        tree = game_tree.GameTree()

        # select each move in get valid moves
        for move in game.get_valid_moves():
            # create a copy of the game and perform the selected move
            game_copy = copy.deepcopy(game)
            game_copy.drop_piece(move[0], move[1], 1)
            # if the move immediately wins the game, do not simulate. Save
            # time and return that move
            if game_copy.get_winner() == 'Red':
                return move

            # begin simulating games after the move was made
            simulate(tree, game_copy, move, num_sims)

        # find the next valid move with the highest win score
        max_tree = tree.get_subtrees()[0]
        for subtree in tree.get_subtrees():
            if subtree.red_win_probability > max_tree.red_win_probability:
                max_tree = subtree

        # return the move with the highest win score
        return max_tree.move


def simulate(tree: game_tree.GameTree, game_copy: Board, move: tuple[int, int],
             num_sims: Optional[int]) -> None:
    """This function takes in a game state and begins simulating games until completion.

    The tree is updated with each move sequence and the score of the game."""
    for _ in range(num_sims):
        # create another copy of the game to save the state of the previous board
        # for each game.
        game_copy_2 = copy.deepcopy(game_copy)

        # rollout (simulate 1 game) the game state using random moves.
        rollout = monte_carlo_rollout(RandomPlayer(), RandomPlayer(), move, game_copy_2)

        # apply the score of the game to the move sequence and insert the
        # move sequence of the 1 rollout to the tree.
        if rollout[0] == 'Red':
            red_win = 1.0
        elif rollout[0] == 'Yellow':
            red_win = -1.0
        else:
            red_win = 0
        tree.insert_move_sequence(rollout[1], red_win)


def monte_carlo_rollout(red: Player, yellow: Player, move: tuple, game_state: Board) \
        -> tuple[str, list[tuple[int, int]]]:
    """Performs one rollout (simulation) of a game and returns a tuple of the winner
    and the list of moves made in the game.

    Each move made is completely random, as guided by the Monte Carlo Tree Search
    definition.

    Preconditions:
        - isinstance(yellow, RandomPlayer)
        - isinstance(red, RandomPlayer)
    """

    # create the move sequence list with the move that's already been played
    move_sequences = [move]

    # yellow is the current player to start because red (the ai) had already made
    # the previous move.
    current_player = yellow
    piece = 2

    # loop until the game has finished
    while game_state.get_winner() is None:
        # a previous move is not passed in as both RandomPlayer and this AI
        # does not require it.
        previous_move = current_player.make_move(game_state, None)
        game_state.drop_piece(previous_move[0], previous_move[1], piece)
        move_sequences.append(previous_move)

        if current_player is red:
            current_player = yellow
            piece = 2
        else:
            current_player = red
            piece = 1

    return game_state.get_winner(), move_sequences


def run_game(red: Player, yellow: Player, size: int) -> tuple[str, list[tuple[int, int]]]:
    """Run a single game between Player red and Player yellow on a board of the given size"""
    game = Board(size)
    move_sequences = []
    previous_move = None
    current_player = red
    piece = 1
    while game.get_winner() is None:
        previous_move = current_player.make_move(game, previous_move)
        game.drop_piece(previous_move[0], previous_move[1], piece)
        move_sequences.append(previous_move)

        if current_player is red:
            current_player = yellow
            piece = 2
        else:
            current_player = red
            piece = 1

    return game.get_winner(), move_sequences


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
