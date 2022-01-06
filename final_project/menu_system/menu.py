"""CSC111 Winter 2021 Project, Game Menu file

This file contains all the different menu classes
that are used in the construction of the main menu system

Copyright and Usage Information
===============================

Base Code was retrieved from: https://github.com/ChristianD37/YoutubeTutorials
Corresponding Youtube Tutorial: https://www.youtube.com/watch?v=a5JWrd7Y_14&t=908s

This file is Copyright (c) 2021 Greg Sherman, Ismail Ahmed,
Kevin Vaidyan, and Akash Illangovan."""
from __future__ import annotations

import sys
import pygame

from constants import BLACK


class Menu:
    """A base class for a menu from which other types of menus
    be created

    Instance Attributes:
        - game: A Game instance
        - mid_w, mid_h: half of the display width and display height respectively
        - run_display: A bool indicating whether to display the current menu
        - cursor_rect: A rect object that corresponds to where the cursor will be drawn
        - offset: An int

    Representation Invariants:
        -
    """
    mid_w: float
    mid_h: float
    run_display: bool
    cursor_rect: pygame.Rect
    offset: int

    def __init__(self, game) -> None:
        """Initialize the current menu"""
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self) -> None:
        """Draw the cursor onto the game window"""
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self) -> None:
        """Blit the games display onto the game window"""
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    """A representation of a main menu for the full game

    Instance Attributes:
        - state: A string representing which menu option
        is currently selected
        - start_x, start_y: Coordinates for where the cursor is located
        when 'Start' is selected
        - credits_x, credits_y: Coordinates for where the cursor is located
        when 'Credits' is selected
        - quit_x, quit_y: Coordinates for where the cursor is located
        when 'Quit' is selected

    Representation Invariants:
        -
    """
    state: str
    start_x: float
    start_y: float
    credits_x: float
    credits_y: float
    quit_x: float
    quit_y: float
    size_x: float
    size_y: float

    def __init__(self, game) -> None:
        """Initialize the main menu for Connect X"""
        Menu.__init__(self, game)
        self.state = 'Start'
        self.start_x, self.start_y = self.mid_w, self.mid_h + 30
        self.credits_x, self.credits_y = self.mid_w, self.mid_h + 50
        self.quit_x, self.quit_y = self.mid_w, self.mid_h + 70
        self.size_x, self.size_y = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)

    def display_menu(self) -> None:
        """Display the main menu onto the game window"""
        self.run_display = True
        # Start the music and have it play in a loop
        pygame.mixer.music.load('game_music.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)
        self.game.display.fill(BLACK)
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(BLACK)
            self.game.draw_text('CSC111 Connect X', 20, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("Start Game", 20, self.start_x, self.start_y)
            self.game.draw_text("Credits", 20, self.credits_x, self.credits_y)
            self.game.draw_text("Quit", 20, self.quit_x, self.quit_y)
            self.game.draw_text("Gamesize", 20, self.size_x, self.size_y)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self) -> None:
        """Change the location of the cursor based which
        key was pressed.
        """
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.credits_x + self.offset - 5, self.credits_y)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.quit_x + self.offset, self.quit_y)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.size_x + self.offset, self.size_y)
                self.state = 'Gamesize'
            elif self.state == 'Gamesize':
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = 'Start'

        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.size_x + self.offset, self.size_y)
                self.state = 'Gamesize'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.start_x + self.offset - 5, self.start_y)
                self.state = 'Start'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = 'Credits'
            elif self.state == 'Gamesize':
                self.cursor_rect.midtop = (self.quit_x + self.offset, self.quit_y)
                self.state = 'Quit'

    def check_input(self) -> None:
        """Check which menu the user selected and
        change self.curr_menu accordingly
        """
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.curr_menu = self.game.player_menu
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Gamesize':
                self.game.curr_menu = self.game.size_menu
            else:
                sys.exit()
            self.run_display = False


class CreditsMenu(Menu):
    """A representation of a simple credits screen showing
    names of all group members

    Instance Attributes:
        - All instance attributes of Menu

    Representation Invariants
        -
    """
    def __init__(self, game) -> None:
        """Initialize the credits menu"""
        Menu.__init__(self, game)

    def display_menu(self) -> None:
        """Display the current credits menu on the game window"""
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(BLACK)
            self.game.draw_text('Credits', 20, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Ismail Ahmed', 15, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 + 10)
            self.game.draw_text('Greg Sherman', 15, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 + 30)
            self.game.draw_text('Akash Illangovan', 15, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 + 50)
            self.game.draw_text('Kevin Vaidyan', 15, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 + 70)
            self.blit_screen()


class DifficultyMenu(Menu):
    """A representation of a difficulty menu for Connect X

    Instance Attributes:
        - state: The current difficulty selected
        - rand_x: The x coordinate where the 'Random' text appears
        on the screen
        - rand_y: The y coordinate where the 'Random' text appears on
        the screen
        - explore_x: The x coordinate where the 'Exploring' text appears
        on the screen
        - explore_y: The y coordinate where the 'Exploring' text appears on
        the screen
        - sabo_x: The x coordinate where the 'Sabotage' text appears
        on the screen
        - sabo_y: The y coordinate where the 'Sabotage' text appears on
        the screen
        - cm_x: The x coordinate where the 'Conte Marlo' text appears on
        the screen
        - cm_y: The y coordinate where the 'Conte Marlo' text appears on
        the screen

    Representation Invariants:
        - self.state in {'Random', 'Exploring', 'Sabotage', 'Conte Marlo'}
    """
    state: str
    rand_x: float
    rand_y: float
    explore_x: float
    explore_y: float
    sabo_x: float
    sabo_y: float
    cm_x: float
    cm_y: float

    def __init__(self, game) -> None:
        """Initialize the current Difficulty menu"""
        Menu.__init__(self, game)
        self.state = 'Random'
        self.rand_x, self.rand_y = self.mid_w, self.mid_h + 20
        self.explore_x, self.explore_y = self.mid_w, self.mid_h + 40
        self.sabo_x, self.sabo_y = self.mid_w, self.mid_h + 60
        self.cm_x, self.cm_y = self.mid_w, self.mid_h + 80
        self.cursor_rect.midtop = (self.rand_x + self.offset, self.rand_y)

    def display_menu(self) -> None:
        """Display the current menu"""
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Select Your AI', 20, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("Random", 15, self.rand_x, self.rand_y)
            self.game.draw_text("Exploring", 15, self.explore_x, self.explore_y)
            self.game.draw_text("Sabotage", 15, self.sabo_x, self.sabo_y)
            self.game.draw_text("Conte Marlo", 15, self.cm_x, self.cm_y)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self) -> None:
        """Check the user's inputs within the difficulty menu
        and update the game window accordingly
        """
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY:
            if self.state == 'Random':
                self.state = 'Conte Marlo'
                self.cursor_rect.midtop = (self.cm_x + self.offset, self.cm_y)
            elif self.state == 'Exploring':
                self.state = 'Random'
                self.cursor_rect.midtop = (self.rand_x + self.offset, self.rand_y)
            elif self.state == 'Sabotage':
                self.state = 'Exploring'
                self.cursor_rect.midtop = (self.explore_x + self.offset, self.explore_y)
            elif self.state == 'Conte Marlo':
                self.state = 'Sabotage'
                self.cursor_rect.midtop = (self.sabo_x + self.offset, self.sabo_y)

        elif self.game.DOWN_KEY:
            if self.state == 'Random':
                self.state = 'Exploring'
                self.cursor_rect.midtop = (self.explore_x + self.offset, self.explore_y)
            elif self.state == 'Exploring':
                self.state = 'Sabotage'
                self.cursor_rect.midtop = (self.sabo_x + self.offset, self.sabo_y)
            elif self.state == 'Sabotage':
                self.state = 'Conte Marlo'
                self.cursor_rect.midtop = (self.cm_x + self.offset, self.cm_y)
            elif self.state == 'Conte Marlo':
                self.state = 'Random'
                self.cursor_rect.midtop = (self.rand_x + self.offset, self.rand_y)

        elif self.game.START_KEY:
            self.game.playing = True
            self.run_display = False


class GameSizeMenu(Menu):
    """A representation of a menu where the user
    can change the board size

    Instance Attributes:
        - dimension_x, dimension_y: Coordinates for where the cursor is drawn
        for the text
    """
    dimension_x: float
    dimension_y: float

    def __init__(self, game) -> None:
        """Initialize the current menu"""
        Menu.__init__(self, game)
        # position of displaying game size
        self.dimension_x, self.dimension_y = self.mid_w, self.mid_h + 20
        self.cursor_rect.midtop = (self.dimension_x + self.offset, self.dimension_y)

    def display_menu(self) -> None:
        """Display the current menu"""
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Board is n x n', 20,
                                self.mid_w, self.mid_h - 50)
            self.game.draw_text('Use left and right arrow keys to decrease or increase', 10,
                                self.mid_w, self.mid_h + 100)
            self.game.draw_text('n is ' + str(self.game.board_size), 15,
                                self.dimension_x, self.dimension_y)
            self.blit_screen()

    def check_input(self) -> None:
        """Check if the user wants to exit this menu"""
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False


class PlayerMenu(Menu):
    """A representation of the menu where the player can choose to
    play against another person or an AI

    Instance Attributes:
        - state: A string representing whether the user wants
        to play with another person or an AI
        - two_player_x, two_player_y: coordinates for where cursor is drawn
        when '2P' is selected
        - ai_x, ai_y: Coordinates for where cursor is drawn when 'AI'  is selected

    Representation Invariants:
        - self.state in {'2P', 'AI'}
    """
    state: str
    two_player_x: float
    two_player_y: float
    ai_x: float
    ai_y: float

    def __init__(self, game) -> None:
        """Initialize the current menu"""
        Menu.__init__(self, game)
        self.state = '2P'
        self.two_player_x, self.two_player_y = self.mid_w, self.mid_h + 20
        self.ai_x, self.ai_y = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.two_player_x + self.offset, self.two_player_y)

    def display_menu(self) -> None:
        """Display the current menu"""
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Select 2P or AI', 20, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("2P", 15, self.two_player_x, self.two_player_y)
            self.game.draw_text("AI", 15, self.ai_x, self.ai_y)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self) -> None:
        """Check if the user wants to exit this menu"""
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY:
            if self.state == '2P':
                self.state = 'AI'
                self.cursor_rect.midtop = (self.ai_x + self.offset, self.ai_y)
            else:
                self.state = '2P'
                self.cursor_rect.midtop = (self.two_player_x + self.offset, self.two_player_y)

        elif self.game.DOWN_KEY:
            if self.state == '2P':
                self.state = 'AI'
                self.cursor_rect.midtop = (self.ai_x + self.offset, self.ai_y)
            else:
                self.state = '2P'
                self.cursor_rect.midtop = (self.two_player_x + self.offset, self.two_player_y)

        elif self.game.START_KEY:
            self.run_display = False
            if self.state == '2P':
                # If we're just playing against another human, we can just
                # immediately start the game
                self.game.playing = True
            else:
                # If we're playing against an AI, we must change to the
                # corresponding menu
                self.game.curr_menu = self.game.difficulty


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
