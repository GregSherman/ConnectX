"""CSC111 Winter 2021 Project, Data file

This file contains many of the constants that will
be used throughout the project

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Greg Sherman, Ismail Ahmed,
Kevin Vaidyan, and Akash Illangovan."""
# Colour constants
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Dimensions
SQUARESIZE = 50

RADIUS = int(SQUARESIZE / 2 - 5)

# Screen
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 650

# Learning list for ExploringPlayer
PROBABILITIES = [1 - i / 400 for i in range(400)] + [0] * 600
