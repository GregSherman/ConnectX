"""CSC111 Winter 2021 Project, Main file

This file is for running the whole project. Upon running
this file, you will be taken to the main menu where you can
play a game, adjust board size etc.

Copyright and Usage Information
===============================

Base Code was retrieved from: https://github.com/ChristianD37/YoutubeTutorials
Corresponding Youtube Tutorial: https://www.youtube.com/watch?v=a5JWrd7Y_14&t=908s

This file is Copyright (c) 2021 Greg Sherman, Ismail Ahmed,
Kevin Vaidyan, and Akash Illangovan."""

from game import Game


def main() -> None:
    """Run the full game"""
    g = Game()

    while g.running:
        g.curr_menu.display_menu()
        g.game_loop()


if __name__ == '__main__':
    main()
