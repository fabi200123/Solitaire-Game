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

# Fan out cards stacked on each other
CARD_VERTICAL_OFFSET = CARD_HEIGHT * CARD_SCALE * 0.3

# Constants for the piles for the game
PILE_COUNT = 13
BOTTOM_FACE_DOWN_PILE = 0
BOTTOM_FACE_UP_PILE = 1
PLAY_PILE_1 = 2
PLAY_PILE_2 = 3
PLAY_PILE_3 = 4
PLAY_PILE_4 = 5
PLAY_PILE_5 = 6
PLAY_PILE_6 = 7
PLAY_PILE_7 = 8
TOP_PILE_1 = 9
TOP_PILE_2 = 10
TOP_PILE_3 = 11
TOP_PILE_4 = 12

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

        # Create a list of lists, each holds a pile of cards
        self.piles = None
    
    def setup(self):
        '''Set up the game and also restart the game'''

        # Sprite list with all the cards
        self.held_cards = []

        # Original location of cards we are dragging
        # They might need to get back
        self.held_cards_original_position = []

        # --- Create the small mats that the cards go on

        # Sprite list with all the mats the cards lay on
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        # Create the mats for the bottom face down and face up piles
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = START_X, BOTTOM_Y
        self.pile_mat_list.append(pile)

        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = START_X + X_SPACING, BOTTOM_Y
        self.pile_mat_list.append(pile)
        
        # Create the seven middle piles
        for i in range(7):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i * X_SPACING, MIDDLE_Y
            self.pile_mat_list.append(pile)

        # Create the top "play" piles
        for i in range(4):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i * X_SPACING, TOP_Y
            self.pile_mat_list.append(pile)

        # --- Create, shuffle, and deal the cards

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
            self.card_list.swap(pos1, pos2)

        # Create a list of lists, each holds a pile of cards.
        self.piles = [[] for _ in range(PILE_COUNT)]

        # Put all the cards in the bottom face down pile
        for card in self.card_list:
            self.piles[BOTTOM_FACE_DOWN_PILE].append(card)

        # --- Deal out the cards

        # Loop for each pile
        for pile_no in range(PLAY_PILE_1, PLAY_PILE_7 + 1):
            # Deal the right number of cards
            for i in range(pile_no - PLAY_PILE_1 + 1):
                # Pop the card off the deck we are dealing from
                card = self.piles[BOTTOM_FACE_DOWN_PILE].pop()
                # Add the card to the pile we are dealing to
                self.piles[pile_no].append(card)
                # Move card to the same position as the pile
                card.position = self.pile_mat_list[pile_no].position
                # Put on top in draw order
                self.pull_to_top(card)

            # Flip up the top cards
            self.piles[pile_no][-1].face_up()

    def on_draw(self):
        '''Render the screen'''
        # Clear the screen
        self.clear()

        # Draw the mats the cards go on to
        self.pile_mat_list.draw()
        
        # Draw the sprites
        self.card_list.draw()

    def pull_to_top(self, card: arcade.Sprite):
        '''Pull card to top of rendering order'''

        # Remove card from list
        self.card_list.remove(card)

        # Add card to end of list
        self.card_list.append(card)

    def on_mouse_press(self, x, y, button, key_modifiers):
        '''Handle mouse click events'''
        
        # Get list of cards that were clicked
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # If we clicked on a card, grab it
        if len(cards) > 0:
            
            # Get the top card (might be a stack of cards)
            top_card = cards[-1]
            # Figure out which pile the card is in
            pile_index = self.get_pile_for_card(top_card)

            if top_card.is_face_down:
                # Flip up the card
                top_card.face_up()
            else:
                # All other cases, grab the face-up card we are clicking on
                self.held_cards = [top_card]
                self.held_cards_original_position = [self.held_cards[0].position]
                self.pull_to_top(self.held_cards[0])

                # Check if there is a stack of cards, and grab those too
                index = self.piles[pile_index].index(top_card)
                for i in range(index + 1, len(self.piles[pile_index])):
                    card = self.piles[pile_index][i]
                    self.held_cards.append(card)
                    self.held_cards_original_position.append(card.position)
                    self.pull_to_top(card)

    def remove_card_from_pile(self, card):
        '''Remove the card from the pile'''
        for pile in self.piles:
            if card in pile:
                pile.remove(card)
                break

    def get_pile_for_card(self, card):
        '''Get the pile for the card'''
        for index, pile in enumerate(self.piles):
            if card in pile:
                return index

        return None

    def move_card_to_new_pile(self, card, new_pile):
        '''Move the card to a new pile'''
        self.remove_card_from_pile(card)
        self.piles[new_pile].append(card)

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

            # Get the index of the pile we are over
            pile_index = self.pile_mat_list.index(pile)

            # If we are over the same pile
            if pile_index == self.get_pile_for_card(self.held_cards[0]):
                pass

            # If we are on a middle play pile
            elif pile_index >= PLAY_PILE_1 and pile_index <= PLAY_PILE_7:
                # Check if there are no cards in the pile
                if len(self.piles[pile_index]) > 0:
                    # Move cards to proper position
                    top_card = self.piles[pile_index][-1]
                    for i, dropped_card in enumerate(self.held_cards):
                        dropped_card.position = top_card.center_x, \
                                                top_card.center_y - CARD_VERTICAL_OFFSET * (i + 1)
                else:
                    # Are there no cards in the middle play pile?
                    for i, dropped_card in enumerate(self.held_cards):
                        # Move cards to proper position
                        dropped_card.position = pile.center_x, \
                                                pile.center_y - CARD_VERTICAL_OFFSET * i

                for card in self.held_cards:
                    # Cards are in the right position, but we need to move them to the right list
                    self.move_card_to_new_pile(card, pile_index)

                # Success, don't reset position of cards
                reset_position = False
            # If we are on a top play pile
            elif pile_index >= TOP_PILE_1 and pile_index <= TOP_PILE_4 and len(self.held_cards) == 1:
                # Move position of card to pile
                self.held_cards[0].position = pile.position
                # Move card to card list
                for card in self.held_cards:
                    self.move_card_to_new_pile(card, pile_index)

                reset_position = False
        if reset_position:
            # We didn't drop the card on a mat. Reset its position
            for i, card in enumerate(self.held_cards):
                # Move card to original position
                card.position = self.held_cards_original_position[i]

        # We are no longer holding cards
        self.held_cards = []

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """

        # If we are holding cards, move them with the mouse
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy

    def on_key_press(self, symbol: int, modifiers: int):
        '''Handle key press events'''
        if symbol == arcade.key.R:
            # Restart the game
            self.setup()

def main():
    '''Main function to run the game'''
    window = Solitaire()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()