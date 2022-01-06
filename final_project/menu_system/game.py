"""CSC111 Winter 2021 Project, Game file

Copyright and Usage Information
===============================

Base Code was retrieved from: https://github.com/ChristianD37/YoutubeTutorials
Corresponding Youtube Tutorial: https://www.youtube.com/watch?v=a5JWrd7Y_14&t=908s

This file is Copyright (c) 2021 Greg Sherman, Ismail Ahmed,
Kevin Vaidyan, and Akash Illangovan."""
from menu import *
from connect_x_game import connectX


class Game:
    """A representation of the full connect 4 game
    that includes the menus, font type and game window

    Instance Attributes:
        - running: A bool indicating whether the full program is running
        - playing: A bool indicating whether the game itself is running
        - UP_KEY, DOWN_KEY, START_KEY, BACK_KEY: booleans indicating whether
        the corresponding arrow keys are pressed
        - display:
        - window:
        - font_name: A string for the file name containing the font type
        (should be in same directory)
        - main_menu, difficulty, stats, credits, size_menu, player_menu: Menu instances that
        correspond to the different Menu subclasses
        - curr_menu: The current active Menu instance
        - board_size: An int representing the side length of the square board

    Representation Invariants:
        - self.board_size >= 7
    """
    running: bool
    playing: bool
    UP_KEY: bool
    DOWN_KEY: bool
    START_KEY: bool
    BACK_KEY: bool
    DISPLAY_W: int
    DISPLAY_H: int
    display: pygame.Surface
    window: pygame.Surface
    font_name: str
    main_menu: MainMenu
    difficulty: DifficultyMenu
    size_menu: GameSizeMenu
    player_menu: PlayerMenu
    board_size: int
    curr_menu: Menu

    def __init__(self) -> None:
        """Initialize the current Game class"""
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 700, 700
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))

        # Font type
        self.font_name = '8-BIT WONDER.TTF'

        # Initialize the menus
        self.main_menu = MainMenu(self)
        self.difficulty = DifficultyMenu(self)
        self.credits = CreditsMenu(self)
        self.size_menu = GameSizeMenu(self)
        self.player_menu = PlayerMenu(self)
        self.curr_menu = self.main_menu

        self.board_size = 7

    def game_loop(self) -> None:
        """Initialize the current game loop"""
        p1_wins = 0
        p2_wins = 0
        draws = 0
        while self.playing:
            if self.player_menu.state == 'AI':
                # Pass in the state of the difficulty menu which holds the
                # the category AI the user wants to play against
                result = connectX.main_with_ai(self.board_size, p1_wins, p2_wins, draws,
                                               self.difficulty.state)
            else:
                # pass in the wins and draws to be displayed in game
                result = connectX.main(self.board_size, p1_wins, p2_wins, draws)
            if result == 0:
                draws += 1
            elif result == 1:
                p1_wins += 1
            elif result == 2:
                p2_wins += 1
            else:
                self.playing = False
                self.curr_menu = self.main_menu

    def check_events(self) -> None:
        """Check the events and update the instance attributes
         accordingly
         """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    if self.curr_menu == self.size_menu and self.board_size != 7:
                        self.board_size -= 2
                elif event.key == pygame.K_RIGHT:
                    if self.curr_menu == self.size_menu:
                        self.board_size += 2

    def reset_keys(self) -> None:
        """Reset the keys so that the game doesn't see them as pressed"""
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text: str, size: int, x: float, y: float) -> None:
        """Draw the given text onto the self.display pygame window"""
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)


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
