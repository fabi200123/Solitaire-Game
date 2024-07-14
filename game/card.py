'''
Card class for Solitaire Game
'''

import arcade

# Constants
CARD_SCALE = 0.6

# DIMENSIONS
CARD_WIDTH = 140 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE

# MAT SIZE
OVERSIZE_PERCENTAGE = 1.25
MAT_WIDTH = int(CARD_WIDTH * OVERSIZE_PERCENTAGE)
MAT_HEIGHT = int(CARD_HEIGHT * OVERSIZE_PERCENTAGE)

# GAP SPACE BETWEEN MATS
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

# The Y of the bottom row (2 piles)
BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The X of where to start putting things on the left side
START_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# CARD CONSTANTS
CARD_VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
CARD_SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

class Card(arcade.Sprite):
    '''Card class for Solitaire Game'''
    
    def __init__(self, suit, value, scale=1):
        '''Initialize the card'''

        self.suit = suit
        self.value = value

        # Image to use for the sprite when face up
        self.image_file_name = f"sprites/{self.suit}/{self.value}.jpg"
        
        # Call the parent class's init function
        super().__init__(self.image_file_name, scale, hit_box_algorithm='None')