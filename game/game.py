'''
Solitaire Game written in Python
'''

import arcade
import random
from card import Card


# Constants
CARD_SCALE = 0.6

# CARD CONSTANTS
CARD_VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
CARD_SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

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

# Screen dimensions
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
TITLE = "Solitaire Game"

# The Y of the top row (4 piles)
TOP_Y = SCREEN_HEIGHT - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The Y of the middle row (7 piles)
MIDDLE_Y = TOP_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# How far apart each pile goes
X_SPACING = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

class Solitaire(arcade.Window):
    '''Main Solitaire Game class'''

    def __init__(self):
        '''Initialize the game'''
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)

        # Sprite list with all the cards
        self.card_list = None

        arcade.set_background_color(arcade.color.AMAZON) # Set background color to Card Table Green (Amazon)

        # List of cards that we will drag with the mouse
        self.held_cards = None

        # Original location of cards we are dragging
        # They might need to get back
        self.held_cards_original_position = None

        # Sprite list with all the mats the cards lay on
        self.pile_mat_list = None
    
    def setup(self):
        '''Set up the game and also restart the game'''

        # Sprite list with all the cards
        self.card_list = []

        # Original location of cards we are dragging
        # They might need to get back
        self.held_cards_original_position = []

        # Create the small mats that the cards go on

        # Sprite list with all the mats the cards lay on
        self.pile_mat_list = arcade.SpriteList()

        # Create the mats for the bottom face down and face up piles
        for i in range(2):
            pile_mat = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile_mat.position = START_X + i * X_SPACING, BOTTOM_Y
            self.pile_mat_list.append(pile_mat)
        
        # Create the seven middle piles
        for i in range(7):
            pile_mat = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile_mat.position = START_X + i * X_SPACING, MIDDLE_Y
            self.pile_mat_list.append(pile_mat)

        # Create the top "play" piles
        for i in range(4):
            pile_mat = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile_mat.position = START_X + i * X_SPACING, TOP_Y
            self.pile_mat_list.append(pile_mat)
        
        # Sprite list with all the cards
        self.card_list = arcade.SpriteList()

        # Create the cards
        for suit in CARD_SUITS:
            for value in CARD_VALUES:
                card = Card(suit, value, CARD_SCALE)
                card.position = START_X, BOTTOM_Y
                self.card_list.append(card)

        # Shuffle the cards
        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list[pos1], self.card_list[pos2] = self.card_list[pos2], self.card_list[pos1]

    def on_draw(self):
        '''Render the screen'''
        # Clear the screen
        self.clear()

        # Draw the mats the cards go on to
        self.pile_mat_list.draw()
        
        # Draw the sprites
        self.card_list.draw()
    
    def on_mouse_press(self, x, y, button, key_modifiers):
        '''Handle mouse click events'''
        
        # Save the position of where we clicked
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # If we clicked on a card, grab it
        if len(cards) > 0:
            
            # Get the top card (might be a stack of cards)
            top_card = cards[-1]

            # All other cases, grab the face-up card we are clicking on
            self.held_cards = [top_card]
            self.held_cards_original_position = [self.held_cards[0].position]
            self.pull_to_top(self.held_cards[0])

    def on_mouse_motion(self, x, y, dx, dy):
        '''Handle mouse motion events'''
        
        # If we are holding cards, move them with the mouse
        if self.held_cards is not None:
            for card in self.held_cards:
                card.center_x += dx
                card.center_y += dy

    def on_mouse_release(self, x, y, button, key_modifiers):
        '''Handle mouse release events'''
        
        # If we are holding cards, see if they are over a mat
        if len(self.held_cards) == 0:
            return

        # Find the closest mat that the card is over 
        # (in case there are more)
        pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
        reset_position = True

        # Check if we are in contact with the closest mat
        if arcade.check_for_collision(self.held_cards[0], pile):
            # For each held card, move it to the pile we dropped it on
            for i, card in enumerate(self.held_cards):
                # Move card to the pile
                card.position = pile.position
            
            # Success, don't reset position of cards
            reset_position = False

        if reset_position:
            # We didn't drop the card on a mat. Reset its position
            for i, card in enumerate(self.held_cards):
                # Move card to original position
                card.position = self.held_cards_original_position[i]

        # We are no longer holding cards
        self.held_cards = []

    def pull_to_top(self, card: arcade.Sprite):
        '''Pull card to top of rendering order'''

        # Remove card from list
        self.card_list.remove(card)

        # Add card to end of list
        self.card_list.append(card)

def main():
    '''Main function to run the game'''
    window = Solitaire()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()