'''
Solitaire Game written in Python
'''

import arcade
import random
import time
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
SCREEN_HEIGHT = 980
TITLE = "Solitaire Game"

# The Y of the top row (4 piles)
TOP_Y = SCREEN_HEIGHT - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The Y of the middle row (7 piles)
MIDDLE_Y = TOP_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# How far apart each pile goes
X_SPACING = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# Fan out cards stacked on each other
CARD_VERTICAL_OFFSET = CARD_HEIGHT * CARD_SCALE * 0.5

# Fan out cards stacked on each other that are face down
CARD_VERTICAL_OFFSET_UNTURNED = CARD_HEIGHT * CARD_SCALE * 0.3

# Fan out cards stacked on each other from the bottom pile
CARD_HORIZONTAL_OFFSET = CARD_WIDTH * CARD_SCALE


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

class StartView(arcade.View):
    '''Start Screen'''

    def __init__(self):
        '''Initialize the view'''
        super().__init__()
        self.hard = False

    def on_show_view(self):
        '''Called when view is activated'''
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
    
    def on_draw(self):
        '''Draw the view'''
        self.clear()
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        # Draw the title
        arcade.draw_text("Solitaire Game", self.window.width / 2, self.window.height / 2 + 100,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

        # Draw mode selection instructions
        arcade.draw_text("Press N for Normal Mode", self.window.width / 2, self.window.height / 2 + 50,
                         arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Press H for Hard Mode", self.window.width / 2, self.window.height / 2,
                         arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Press Space to Start", self.window.width / 2, self.window.height / 2 - 50,
                         arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")

        # Show selected mode
        if self.hard:
            arcade.draw_text("Hard Mode Selected", self.window.width / 2, self.window.height / 2 - 100,
                             arcade.color.RED, font_size=20, anchor_x="center")
            arcade.draw_text("Explanation: In Hard Mode, you will have 3 cards swapped on click from the bottom pile.", self.window.width / 2, self.window.height / 2 - 200,
                             arcade.color.LIGHT_GRAY, font_size=14, anchor_x="center", multiline=True, width=self.window.width - 220)
        else:
            arcade.draw_text("Normal Mode Selected", self.window.width / 2, self.window.height / 2 - 100,
                             arcade.color.GREEN, font_size=20, anchor_x="center")
            arcade.draw_text("Explanation: In Normal Mode, you will have 1 card swapped on click from the bottom pile.", self.window.width / 2, self.window.height / 2 - 200,
                             arcade.color.LIGHT_GRAY, font_size=14, anchor_x="center", multiline=True, width=self.window.width - 220)

    def on_key_press(self, symbol: int, modifiers: int):
        """ Handle key press events """
        if symbol == arcade.key.SPACE:
            game_view = SolitaireView()
            game_view.setup(hard_mode=self.hard)
            self.window.show_view(game_view)
        elif symbol == arcade.key.N:
            self.hard = False
        elif symbol == arcade.key.H:
            self.hard = True

class WinningView(arcade.View):
    '''Winning Screen'''

    def on_show_view(self):
        '''Called when view is activated'''
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        '''Draw the view'''
        self.clear()
        arcade.set_background_color(arcade.color.GRAY)
        arcade.draw_text("You Won!", self.window.width / 2, self.window.height / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Press R to restart", self.window.width / 2, self.window.height / 2 - 75,
                        arcade.color.BLACK, font_size=20, anchor_x="center")
    
    def on_key_press(self, symbol: int, modifiers: int):
        """ If the user presses the mouse button, start the game. """
        if symbol == arcade.key.R:
            game_view = StartView()
            self.window.show_view(game_view)

class SolitaireView(arcade.View):
    '''Main Solitaire Game class'''

    def __init__(self):
        '''Initialize the game'''
        super().__init__()

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

        # Timer to check how long the game has been running
        self.elapsed_time = 0

        # Create a list of lists, each holds a pile of cards
        self.piles = None

        # Create a variable for winning state
        self.won = False

        # Timer to check how long the game has been running
        self.start_time = time.time()

        # Number of points the user has
        self.moves = 0

    
    def setup(self, hard_mode: bool):
        '''Set up the game and also restart the game'''

        # Sprite list with all the cards
        self.held_cards = []

        # Set hard mode
        self.hard_mode = hard_mode

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

        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.color.AMAZON)
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
                if not card.is_face_up:
                    card.position = (self.pile_mat_list[pile_no].center_x, 
                                     self.pile_mat_list[pile_no].center_y - CARD_VERTICAL_OFFSET_UNTURNED * i)
                else:
                    card.position = self.pile_mat_list[pile_no].position
                # Put on top in draw order
                self.pull_to_top(card)

            # Flip up the top cards
            self.piles[pile_no][-1].face_up()
            self.piles[pile_no][-1].position = self.pile_mat_list[pile_no].center_x, self.pile_mat_list[pile_no].center_y - CARD_VERTICAL_OFFSET_UNTURNED * (len(self.piles[pile_no]) - 1)


    def on_draw(self):
        '''Render the screen'''
        # Clear the screen
        self.clear()

        # Draw the mats the cards go on to
        self.pile_mat_list.draw()
        
        # Draw the sprites
        self.card_list.draw()

        # Draw the timer inside a gray rectangle
        minutes = int(self.elapsed_time // 60)
        seconds = int(self.elapsed_time % 60)
        timer_text = f"{minutes:02d}:{seconds:02d}"
        
        # Define the rectangle dimensions
        rect_x = SCREEN_WIDTH - 100
        rect_y = SCREEN_HEIGHT - 40
        rect_width = 80
        rect_height = 30
        
        # Draw the gray rectangle
        arcade.draw_rectangle_filled(rect_x, rect_y, rect_width, rect_height, arcade.color.LIGHT_GRAY)
        
        # Draw the Time text
        arcade.draw_text("Time", rect_x-90, rect_y,
                         arcade.color.BLACK, 20, anchor_x="center", anchor_y="center")

        # Draw the timer text
        arcade.draw_text(timer_text, rect_x, rect_y,
                         arcade.color.BLACK, 20, anchor_x="center", anchor_y="center")
        
        # Define the points rectangle dimensions
        points_rect_x = SCREEN_WIDTH - 100
        points_rect_y = SCREEN_HEIGHT - 80
        points_rect_width = 80
        points_rect_height = 30
        
        # Draw the gray rectangle
        arcade.draw_rectangle_filled(points_rect_x, points_rect_y, points_rect_width, points_rect_height, arcade.color.LIGHT_GRAY)

        # Draw the moves text
        arcade.draw_text("Moves", points_rect_x-90, points_rect_y,
                         arcade.color.BLACK, 20, anchor_x="center", anchor_y="center")
        
        # Draw the moves inside the rectangle
        arcade.draw_text(str(self.moves), points_rect_x, points_rect_y,
                         arcade.color.BLACK, 20, anchor_x="center", anchor_y="center")

    def on_update(self, delta_time: float):
        '''Update the game'''

        # Update the timer
        self.elapsed_time = time.time() - self.start_time

    def pull_to_top(self, card: arcade.Sprite):
        '''Pull card to top of rendering order'''

        # Remove card from list
        self.card_list.remove(card)

        # Add card to end of list
        self.card_list.append(card)

    def on_mouse_press(self, x, y, button, key_modifiers):
        '''Handle mouse click events'''

        if button != arcade.MOUSE_BUTTON_LEFT:
            # Reset position of the cards
            # If not, multiple cards can be selected
            # when right-clicking for example
            for i, card in enumerate(self.held_cards):
                card.position = self.held_cards_original_position[i]
            return
        
        # Get list of cards that were clicked
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # If we clicked on a card, grab it
        if len(cards) > 0:

            # Get the top card (might be a stack of cards)
            top_card = cards[-1]

            # Figure out which pile the card is in
            pile_index = self.get_pile_for_card(top_card)

            if pile_index == BOTTOM_FACE_DOWN_PILE:
                if self.hard_mode:
                    # Move all face up cards to the position of the face up mat pile
                    for card in self.piles[BOTTOM_FACE_UP_PILE]:
                        card.position = self.pile_mat_list[BOTTOM_FACE_UP_PILE].position
                    # Flip 3 cards
                    for i in range(3):
                        # If we run out of cards, stop
                        if len(self.piles[BOTTOM_FACE_DOWN_PILE]) == 0:
                            break
                        # Get the top card
                        card = self.piles[BOTTOM_FACE_DOWN_PILE][-1]
                        # Flip face up
                        card.face_up()
                        # Move card position to bottom-right face up pile
                        card.position = self.pile_mat_list[BOTTOM_FACE_UP_PILE].position
                        card.center_x += CARD_HORIZONTAL_OFFSET * i
                        # Remove card from face down pile
                        self.piles[BOTTOM_FACE_DOWN_PILE].remove(card)
                        # Add card to face up pile
                        self.piles[BOTTOM_FACE_UP_PILE].append(card)
                        # Put on top in draw order
                        self.pull_to_top(card)
                        self.moves += 1
                else:
                    # Flip 1 card
                    # Get the top card
                    card = self.piles[BOTTOM_FACE_DOWN_PILE][-1]
                    # Flip face up
                    card.face_up()
                    # Move card position to bottom-right face up pile
                    card.position = self.pile_mat_list[BOTTOM_FACE_UP_PILE].position
                    # Remove card from face down pile
                    self.piles[BOTTOM_FACE_DOWN_PILE].remove(card)
                    # Add card to face up pile
                    self.piles[BOTTOM_FACE_UP_PILE].append(card)
                    # Put on top in draw order
                    self.pull_to_top(card)
                    self.moves += 1
            elif top_card.is_face_down:
                # Check if the card is the top card of the pile
                if self.piles[pile_index][-1] == top_card:
                    # Flip the card
                    top_card.face_up()
            else:
                # In case of hardmode, select only
                # the top card of the face up card pile
                # if not, return
                if self.get_pile_for_card(top_card) == BOTTOM_FACE_UP_PILE: 
                    if top_card != self.piles[BOTTOM_FACE_UP_PILE][-1]:
                        return
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
        else:
            # If clicked on mat instead of a card
            mats = arcade.get_sprites_at_point((x, y), self.pile_mat_list)

            if len(mats) > 0:
                mat = mats[0]
                mat_index = self.pile_mat_list.index(mat)

                # If there are no cards on the mat
                if mat_index == BOTTOM_FACE_DOWN_PILE and len(self.piles[BOTTOM_FACE_DOWN_PILE]) == 0:
                    # Flip the deck back over so we can restart
                    temp_list = self.piles[BOTTOM_FACE_UP_PILE].copy()
                    self.moves += 1
                    for card in reversed(temp_list):
                        card.face_down()
                        self.piles[BOTTOM_FACE_UP_PILE].remove(card)
                        self.piles[BOTTOM_FACE_DOWN_PILE].append(card)
                        card.position = self.pile_mat_list[BOTTOM_FACE_DOWN_PILE].position

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
                # Reset position of cards
                reset_position = True

            # If we are on a middle play pile
            elif pile_index >= PLAY_PILE_1 and pile_index <= PLAY_PILE_7:
                # Check if there are no cards in the pile
                if len(self.piles[pile_index]) > 0:
                    # Check if the top card is one value higher and a different color
                    top_card = self.piles[pile_index][-1]
                    if top_card.colour != self.held_cards[0].colour and \
                        CARD_VALUES.index(top_card.value) - 1 == CARD_VALUES.index(self.held_cards[0].value) and top_card.suit != self.held_cards[0].suit:
                        # Move cards to proper position
                        for i, dropped_card in enumerate(self.held_cards):
                            dropped_card.position = top_card.center_x, \
                                                    top_card.center_y - CARD_VERTICAL_OFFSET * (i + 1)
                        reset_position = False
                        self.moves += 1
                    else:
                        # Reset position of cards
                        reset_position = True
                else:
                    # If there are no cards in the pile
                    # Move cards only if there is a 'K' card
                    if self.held_cards[0].value == 'K':
                        # Move cards to proper position
                        for i, dropped_card in enumerate(self.held_cards):
                            if i == 0:
                                dropped_card.position = pile.position
                                first_card = dropped_card
                            else:
                                dropped_card.position = first_card.center_x, \
                                                    first_card.center_y - CARD_VERTICAL_OFFSET * i
                        reset_position = False
                        self.moves += 1
                    else:
                        # Reset position of cards
                        reset_position = True
                if not reset_position:
                    for card in self.held_cards:
                        # Cards are in the right position, but we need to move them to the right list
                        self.move_card_to_new_pile(card, pile_index)
            # If we are on a top play pile
            elif pile_index >= TOP_PILE_1 and pile_index <= TOP_PILE_4 and len(self.held_cards) == 1:
                # If the pile is empty, only allow an Ace to be dropped
                if len(self.piles[pile_index]) == 0 and self.held_cards[0].value == 'A':
                    # Move card to card list
                    self.move_card_to_new_pile(self.held_cards[0], pile_index)
                    # Move card to pile
                    self.held_cards[0].position = pile.position
                    reset_position = False
                    self.moves += 1
                # If the pile is not empty, only allow cards of the same suit and one higher value
                elif len(self.piles[pile_index]) > 0:
                    top_card = self.piles[pile_index][-1]
                    if top_card.suit == self.held_cards[0].suit and \
                        CARD_VALUES.index(top_card.value) + 1 == CARD_VALUES.index(self.held_cards[0].value):
                        # Move card to card list
                        self.move_card_to_new_pile(self.held_cards[0], pile_index)
                        # Move card to pile
                        self.held_cards[0].position = pile.position
                        reset_position = False
                        self.moves += 1
                else:
                    # Reset position of cards
                    reset_position = True
        if reset_position:
            # Reset position of the cards
            for i, card in enumerate(self.held_cards):
                card.position = self.held_cards_original_position[i]

        # We are no longer holding cards
        self.held_cards = []

        # --- Win check
        if self.check_winning():
            # Show the winning window
            view = WinningView()
            self.window.show_view(view)

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
            game_view = StartView()
            self.window.show_view(game_view)
            # self.start_time = time.time()
            # self.moves = 0
            # self.setup(self.hard_mode)

    def check_winning(self):
        '''Check if the player has won the game'''
        for pile in self.piles[TOP_PILE_1:]:
            if len(pile) != 13:
                return False
        return True

def main():
    '''Main function to run the game'''
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()