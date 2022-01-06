"""CSC111 Winter 2021 Project, Connect X file

This file contains the code for game logic and visualization
of the Connect X game.

Copyright and Usage Information
===============================

Base Code was retrieved from: https://github.com/KeithGalli/Connect4-Python
Corresponding Youtube Tutorial: https://youtube.com/watch?v=XpYz-q1lxu8&t=154s

This file is Copyright (c) 2021 Greg Sherman, Ismail Ahmed,
Kevin Vaidyan, and Akash Illangovan."""
import sys
import math
import pygame
from constants import *
from board import Board
from players import RandomPlayer, MonteCarloFreeVersion, SabotagePlayer, ExploringPlayer
import tree_generation


def main(game_size: int, p1_wins: int, p2_wins: int, draws: int) -> int:
    """A run function that starts the Connect 4 game loop

    The return value of the main will tell the game how to update the
    Win/Loss/Draw ratio that is displayed
    """

    # Initialize the game board and state
    new_board = Board(game_size)
    game_over = False
    turn = 0

    # Initialize the pygame screen for the game
    size = (new_board.width + 300, new_board.height)
    screen = pygame.display.set_mode(size)
    screen.fill(BLACK)

    new_board.draw_board(screen)

    # Create the fonts for the score text and quit button
    myfont = pygame.font.SysFont('monospace', 17)
    quit_font = pygame.font.SysFont('monospace', 17)

    quit_surface = quit_font.render('Quit', True, (0, 0, 0))

    # Draw the quit button
    pygame.draw.rect(screen, (255, 255, 255), (new_board.width + 30, 50, 60, 50), 0, 3)
    screen.blit(quit_surface, (new_board.width + 40, 60))

    # Draw the Win/Loss/Draw for player 1 and player 2
    text_surface = myfont.render(f'P1 (Win/Loss/Draw): {p1_wins}/{p2_wins}/{draws}',
                                 True, (255, 0, 0))
    screen.blit(text_surface, (new_board.width + 20, 120))

    text_surface = myfont.render(f'P2 (Win/Loss/Draw): {p2_wins}/{p1_wins}/{draws}',
                                 True, (255, 255, 0))
    screen.blit(text_surface, (new_board.width + 20, 160))

    pygame.mixer.music.set_volume(0.5)
    while not game_over:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Updates the position of the current piece when the player moves it
            if event.type == pygame.MOUSEMOTION and \
                    pygame.mouse.get_pos()[0] < new_board.width - 20:
                pygame.draw.rect(screen, BLACK, (0, 0, new_board.width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

            # Change the color of the quit button from white to red depending if the player
            # hovers over it
            if event.type == pygame.MOUSEMOTION and \
                    (new_board.width + 30 <= pygame.mouse.get_pos()[0] <= new_board.width + 90
                     and 50 <= pygame.mouse.get_pos()[1] <= 100):

                pygame.draw.rect(screen, (255, 0, 0), (new_board.width + 30, 50, 60, 50), 0, 3)
                screen.blit(quit_surface, (new_board.width + 40, 60))

            else:
                pygame.draw.rect(screen, (255, 255, 255), (new_board.width + 30, 50, 60, 50), 0, 3)
                screen.blit(quit_surface, (new_board.width + 40, 60))

            if event.type == pygame.MOUSEBUTTONDOWN and \
                    pygame.mouse.get_pos()[0] < new_board.width - 20:

                pygame.draw.rect(screen, BLACK, (0, 0, new_board.width, SQUARESIZE))

                # print(event.pos)
                # Check if it's player 1's turn
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))
                    row = new_board.get_next_open_row(col)

                    if (row, col) in new_board.get_valid_moves():
                        new_board.drop_piece(row, col, 1)
                        pygame.display.update()

                        # Play the drop piece sound effect
                        sound_obj = pygame.mixer.Sound('drop_sound.wav')
                        sound_obj.set_volume(0.4)
                        sound_obj.play()

                        if new_board.winning_move(1):
                            label = myfont.render("Player 1 wins!!", True, RED)
                            screen.blit(label, (10, 10))
                            new_board.draw_board(screen)
                            pygame.time.wait(1000)
                            pygame.mixer.music.set_volume(0.5)
                            return 1

                        # If we know that the the top row is filled and
                        # the winner is not declared, then it must be a tie
                        elif new_board.get_valid_moves() == []:
                            label = myfont.render("Tie!", True, (255, 255, 255))
                            screen.blit(label, (10, 10))
                            new_board.draw_board(screen)
                            pygame.time.wait(1000)
                            pygame.mixer.music.set_volume(0.5)
                            return 0

                # Ask for Player 2 Input
                else:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))
                    row = new_board.get_next_open_row(col)

                    if (row, col) in new_board.get_valid_moves():
                        row = new_board.get_next_open_row(col)
                        new_board.drop_piece(row, col, 2)
                        pygame.display.update()

                        sound_obj = pygame.mixer.Sound('drop_sound.wav')
                        sound_obj.set_volume(0.4)
                        sound_obj.play()

                        if new_board.winning_move(2):
                            label = myfont.render("Player 2 wins!!", True, YELLOW)
                            screen.blit(label, (10, 10))
                            new_board.draw_board(screen)
                            pygame.time.wait(1000)
                            pygame.mixer.music.set_volume(0.5)
                            return 2

                        elif new_board.get_winner() == 'Draw':
                            label = myfont.render("Tie!", True, (255, 255, 255))
                            new_board.draw_board(screen)
                            screen.blit(label, (10, 10))
                            pygame.time.wait(1000)
                            pygame.mixer.music.set_volume(0.5)
                            return 0

                new_board.draw_board(screen)

                turn = (turn + 1) % 2

                if game_over:
                    pygame.time.wait(2000)

                    # Set the pygame window back to its original dimensions
                    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

            # Checks if the Quit button was pressed
            elif event.type == pygame.MOUSEBUTTONDOWN and \
                    (new_board.width + 30 <= pygame.mouse.get_pos()[0] <= new_board.width + 90
                     and 50 <= pygame.mouse.get_pos()[1] <= 100):

                pygame.time.wait(500)
                pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                pygame.mixer.music.set_volume(0.5)
                return 3


def main_with_ai(game_size: int, p1_wins: int, p2_wins: int, draws: int, ai: str) -> int:
    """A run function that starts the Connect 4 game loop (playing against AI)

    The return value of this main will let the game know how to update the
    Win/Loss/Draw ratios being displayed
    """
    # Initialize the game board and state
    new_board = Board(game_size)
    previous_move = '*'
    game_over = False
    number_of_mc_sims = 200

    # initialize the ai
    if ai == 'Random':
        ai_player = RandomPlayer()

    elif ai == 'Exploring':
        exploring_tree = tree_generation.run_learning_algorithm(PROBABILITIES, game_size)[0]
        ai_player = ExploringPlayer(exploring_tree, 1.0)

    elif ai == 'Sabotage':
        ai_player = SabotagePlayer()

    else:
        ai_player = MonteCarloFreeVersion()

    # Initialize the pygame screen for the game
    size = (new_board.width + 300, new_board.height)
    screen = pygame.display.set_mode(size)
    screen.fill(BLACK)

    new_board.draw_board(screen)

    # Draw the quit button and Win/Loss/Draw ratios for each player
    myfont = pygame.font.SysFont('monospace', 17)
    quit_font = pygame.font.SysFont('monospace', 17)
    quit_surface = quit_font.render('Quit', True, (0, 0, 0))

    pygame.draw.rect(screen, (255, 255, 255), (new_board.width + 30, 50, 60, 50), 0, 3)
    screen.blit(quit_surface, (new_board.width + 40, 60))

    # Draw the Win/Loss/Draw ratios for each player
    text_surface = myfont.render(f'P1 (Win/Loss/Draw): {p1_wins}/{p2_wins}/{draws}',
                                 True, (255, 0, 0))
    screen.blit(text_surface, (new_board.width + 20, 120))

    text_surface = myfont.render(f'P2 (Win/Loss/Draw): {p2_wins}/{p1_wins}/{draws}',
                                 True, (255, 255, 0))
    screen.blit(text_surface, (new_board.width + 20, 160))

    if ai == 'Conte Marlo':
        # Since the AI will always go first, we draw the calculating move text
        # As well as the buttons to modify the number if simulations
        text_surface = myfont.render('Calculating Move...', True, (255, 255, 255))
        screen.blit(text_surface, (new_board.width + 20, 200))

        pygame.draw.rect(screen, (0, 255, 0), (new_board.width + 30, 280, 30, 30), 0, 3)
        pygame.draw.rect(screen, (255, 0, 0), (new_board.width + 90, 280, 30, 30), 0, 3)

        text_surface = myfont.render(f'Number of Simulations: {number_of_mc_sims}', True,
                                     (255, 255, 255))
        screen.blit(text_surface, (new_board.width + 20, 240))

        text_surface = myfont.render('+', True, (0, 0, 0))
        screen.blit(text_surface, (new_board.width + 30, 280))
        text_surface = myfont.render('-', True, (0, 0, 0))
        screen.blit(text_surface, (new_board.width + 90, 280))

    pygame.mixer.music.set_volume(0.5)
    while not game_over:
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Redraw the piece to be dropped when the user moves their mouse
            if event.type == pygame.MOUSEMOTION and \
                    pygame.mouse.get_pos()[0] < new_board.width - 20:
                pygame.draw.rect(screen, BLACK, (0, 0, new_board.width, SQUARESIZE))
                posx = event.pos[0]
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

            # Change the color of the quit button to red when the user hovers over it
            # Keep the color white otherwise
            if event.type == pygame.MOUSEMOTION and \
                    (new_board.width + 30 <= pygame.mouse.get_pos()[0] <= new_board.width + 90
                     and 50 <= pygame.mouse.get_pos()[1] <= 100):

                pygame.draw.rect(screen, (255, 0, 0), (new_board.width + 30, 50, 60, 50), 0, 3)
                screen.blit(quit_surface, (new_board.width + 40, 60))

            else:
                pygame.draw.rect(screen, (255, 255, 255), (new_board.width + 30, 50, 60, 50), 0, 3)
                screen.blit(quit_surface, (new_board.width + 40, 60))

            if not new_board.is_red_active:

                # Check if the user wants to drop their piece
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        pygame.mouse.get_pos()[0] < new_board.width - 20:

                    pygame.draw.rect(screen, BLACK, (0, 0, new_board.width, SQUARESIZE))

                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))
                    row = new_board.get_next_open_row(col)

                    if (row, col) in new_board.get_valid_moves():
                        new_board.drop_piece(row, col, 2)
                        previous_move = (row, col)
                        pygame.display.update()
                        sound_obj = pygame.mixer.Sound('drop_sound.wav')
                        sound_obj.set_volume(0.4)
                        sound_obj.play()

                        if new_board.winning_move(2):
                            label = myfont.render("Player 2 wins!!", True, YELLOW)
                            screen.blit(label, (10, 10))
                            new_board.draw_board(screen)
                            pygame.time.wait(1000)
                            pygame.mixer.music.set_volume(0.5)
                            return 2

                        # If we know that the the top row is filled and
                        # the winner is not declared, then it must be a tie
                        elif new_board.get_winner() == 'Draw':
                            label = myfont.render("Tie!", True, (255, 255, 255))
                            new_board.draw_board(screen)
                            screen.blit(label, (10, 10))
                            pygame.time.wait(1000)
                            pygame.mixer.music.set_volume(0.5)
                            return 0

                    new_board.draw_board(screen)

                    # Once the user the drops their piece, it will be the AI's turn
                    # We draw the text 'Calculating Move' for Monte Carlo to make it clear
                    # that it takes some time
                    if ai == 'Conte Marlo':
                        text_surface2 = myfont.render('Calculating Move...', True, (255, 255, 255))
                        screen.blit(text_surface2, (new_board.width + 20, 200))

                    if game_over:
                        pygame.time.wait(2000)

                        # Set the pygame window back to its original dimensions
                        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

                # Checks if the Quit button was pressed
                elif event.type == pygame.MOUSEBUTTONDOWN and \
                        (new_board.width + 30 <= pygame.mouse.get_pos()[0] <= new_board.width + 90
                         and 50 <= pygame.mouse.get_pos()[1] <= 100):

                    pygame.time.wait(500)
                    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    pygame.mixer.music.set_volume(0.5)
                    return 3

                # Check if the user wants to increase the number of simulations for
                # Monte Carlo and then redraw the screen
                elif event.type == pygame.MOUSEBUTTONDOWN and ai == 'Conte Marlo' and \
                        (new_board.width + 30 <= pygame.mouse.get_pos()[0] <= new_board.width + 60
                         and 280 <= pygame.mouse.get_pos()[1] <= 310):
                    number_of_mc_sims += 10
                    redraw_screen_mc(myfont, new_board, screen, p1_wins, p2_wins, draws,
                                     quit_surface, number_of_mc_sims)

                # Check if the user wants to decrease the number of simulations for
                # Monte Carlo and then redraw the screen
                elif event.type == pygame.MOUSEBUTTONDOWN and ai == 'Conte Marlo' and \
                        (new_board.width + 90 <= pygame.mouse.get_pos()[0] <= new_board.width + 120
                         and 280 <= pygame.mouse.get_pos()[1] <= 310) and number_of_mc_sims != 10:
                    number_of_mc_sims -= 10
                    redraw_screen_mc(myfont, new_board, screen, p1_wins, p2_wins, draws,
                                     quit_surface, number_of_mc_sims)

            else:
                # If the AI being played against is Monte Carlo, pass in the number of
                # simulations to be played
                if ai == 'Conte Marlo':
                    ai_move = ai_player.make_move(new_board, previous_move, number_of_mc_sims)
                else:
                    ai_move = ai_player.make_move(new_board, previous_move)
                previous_move = ai_move
                new_board.drop_piece(previous_move[0], previous_move[1], 1)

                # If the AI being played against is Monte Carlo, we need to redraw
                # the pygame screens a bit differently
                if ai == 'Conte Marlo':
                    redraw_screen_mc(myfont, new_board, screen, p1_wins, p2_wins, draws,
                                     quit_surface, number_of_mc_sims)

                else:
                    screen.fill(BLACK)
                    new_board.draw_board(screen)
                    pygame.draw.rect(screen, (255, 255, 255), (new_board.width + 30, 50, 60, 50), 0,
                                     3)
                    screen.blit(quit_surface, (new_board.width + 40, 60))

                    text_surface = myfont.render(f'P1 (Win/Loss/Draw): {p1_wins}/{p2_wins}/{draws}',
                                                 True, (255, 0, 0))
                    screen.blit(text_surface, (new_board.width + 20, 120))

                    text_surface = myfont.render(f'P2 (Win/Loss/Draw): {p2_wins}/{p1_wins}/{draws}',
                                                 True,
                                                 (255, 255, 0))
                    screen.blit(text_surface, (new_board.width + 20, 160))

                sound_obj = pygame.mixer.Sound('drop_sound.wav')
                sound_obj.set_volume(0.4)
                sound_obj.play()

                if new_board.winning_move(1):
                    label = myfont.render("Player 1 wins!!", True, RED)
                    screen.blit(label, (10, 10))
                    new_board.draw_board(screen)
                    pygame.time.wait(1000)
                    pygame.mixer.music.set_volume(0.5)
                    return 1


def redraw_screen_mc(myfont: pygame.font.SysFont, new_board: Board, screen: pygame.Surface,
                     p1_wins: int, p2_wins: int, draws: int, quit_surface: pygame.Surface,
                     number_of_mc_sims: int) -> None:
    """Redraw the entire screen if the ai being played against is Monte Carlo"""
    screen.fill(BLACK)
    new_board.draw_board(screen)

    # Redraw the quit button
    pygame.draw.rect(screen, (255, 255, 255), (new_board.width + 30, 50, 60, 50), 0, 3)
    screen.blit(quit_surface, (new_board.width + 40, 60))

    # Redraw the Win/Loss/Draw ratios for both players
    text_surface = myfont.render(f'P1 (Win/Loss/Draw): {p1_wins}/{p2_wins}/{draws}', True,
                                 (255, 0, 0))
    screen.blit(text_surface, (new_board.width + 20, 120))

    text_surface = myfont.render(f'P2 (Win/Loss/Draw): {p2_wins}/{p1_wins}/{draws}', True,
                                 (255, 255, 0))
    screen.blit(text_surface, (new_board.width + 20, 160))

    # Redraw the buttons for modifying the number of simulations and the text
    # displaying the number of simulations
    pygame.draw.rect(screen, (0, 255, 0), (new_board.width + 30, 280, 30, 30), 0, 3)
    pygame.draw.rect(screen, (255, 0, 0), (new_board.width + 90, 280, 30, 30), 0, 3)

    text_surface = myfont.render(f'Number of Simulations: {number_of_mc_sims}', True,
                                 (255, 255, 255))
    screen.blit(text_surface, (new_board.width + 20, 240))

    text_surface = myfont.render('+', True, (0, 0, 0))
    screen.blit(text_surface, (new_board.width + 30, 280))
    text_surface = myfont.render('-', True, (0, 0, 0))
    screen.blit(text_surface, (new_board.width + 90, 280))


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
