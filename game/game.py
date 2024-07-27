'''
Solitaire Game written in Python
'''

import arcade
import arcade.gui as gui
import random
import time
from card import Card, resource_path
from fireworks import Firework, create_firework

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

# Styles for the buttons
unselected = {
    "font_name": "Arial",
    "font_size": 12,
    "font_color": arcade.color.WHITE,
    "bg_color": (21, 20, 20, 255),
    "border_color": arcade.color.WHITE,
    "border_width": 2,
    "border_radius": 10,
}

selected = {
    "font_name": "Arial",
    "font_size": 12,
    "font_color": arcade.color.BLACK,
    "bg_color": arcade.color.LIGHT_GREEN,
    "border_color": arcade.color.WHITE,
    "border_width": 2,
    "border_radius": 10,
}

# Screens background
START_SCREEN = resource_path("sprites/screens/starting_screen.jpg")
WINNING_SCREEN = resource_path("sprites/screens/starting_screen.jpg")

class StartView(arcade.View):
    '''Start Screen'''

    def __init__(self):
        '''Initialize the view'''
        super().__init__()
        self.hard = False
        self.background = arcade.load_texture(START_SCREEN)
        self.ui_manager = gui.UIManager()
        self.language = "EN"  # Default language

        self.selected = selected
        self.unselected = unselected

        # Define the 2 buttons
        self.en_button = gui.UIFlatButton()
        self.ro_button = gui.UIFlatButton()
    
    def setup(self, en_style=selected, ro_style=unselected):
        # Create a new UIManager instance
        self.ui_manager = gui.UIManager()
        self.ui_manager.enable()

        # Create buttons
        self.en_button = gui.UIFlatButton(text="EN", width=100, height=50, style=en_style)
        self.en_button.on_click = self.on_click_en

        self.ro_button = gui.UIFlatButton(text="RO", width=100, height=50, style=ro_style)
        self.ro_button.on_click = self.on_click_ro

        # Position buttons using UIAnchorWidget
        self.en_button_anchor = gui.UIAnchorWidget(
            anchor_x="center_x", anchor_y="bottom", child=self.en_button, align_x=-60, align_y=50
        )
        self.ro_button_anchor = gui.UIAnchorWidget(
            anchor_x="center_x", anchor_y="bottom", child=self.ro_button, align_x=60, align_y=50
        )

        # Add buttons to UIManager
        self.ui_manager.add(self.en_button_anchor)
        self.ui_manager.add(self.ro_button_anchor)

    def on_click_en(self, event):
        self.language = "EN"
        self.setup(self.selected, self.unselected)

    def on_click_ro(self, event):
        self.language = "RO"
        self.setup(self.unselected, self.selected)

    def on_show_view(self):
        '''Called when view is activated'''
        self.setup()
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
    
    def on_hide_view(self):
        self.ui_manager.disable()

    def on_update(self, delta_time):
        self.ui_manager.on_update(delta_time)
    
    def on_draw(self):
        '''Draw the view'''
        self.clear()
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        # Draw the background image
        arcade.draw_lrwh_rectangle_textured(0, 0, self.window.width, self.window.height, self.background)

        # Draw the title
        arcade.draw_text("Solitaire", self.window.width / 2, self.window.height / 2 + 100,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

        # Draw mode selection instructions
        if self.language == "RO":
            arcade.draw_text("Apasa N pentru a selecta Modul Normal", self.window.width / 2, self.window.height / 2 + 50,
                             arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")
            arcade.draw_text("Apasa H pentru a selecta Modul Greu", self.window.width / 2, self.window.height / 2,
                             arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")
            arcade.draw_text("Apasa Space pentru a incepe", self.window.width / 2, self.window.height / 2 - 50,
                             arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")
        elif self.language == "EN":
            arcade.draw_text("Press N for Normal Mode", self.window.width / 2, self.window.height / 2 + 50,
                            arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")
            arcade.draw_text("Press H for Hard Mode", self.window.width / 2, self.window.height / 2,
                            arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")
            arcade.draw_text("Press Space to Start", self.window.width / 2, self.window.height / 2 - 50,
                            arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")

        # Show selected mode
        if self.hard:
            if self.language == "RO":
                arcade.draw_text("Mod Greu Selectat", self.window.width / 2, self.window.height / 2 - 100,
                             arcade.color.RED, font_size=20, anchor_x="center")
                arcade.draw_text("Explicatie: In Modul Greu, vei avea 3 carti schimbate la apasarea pachetului de jos.", self.window.width / 2, self.window.height / 2 - 200,
                             arcade.color.LIGHT_GRAY, font_size=14, anchor_x="center", multiline=True, width=self.window.width - 220)
            elif self.language == "EN":
                arcade.draw_text("Hard Mode Selected", self.window.width / 2, self.window.height / 2 - 100,
                                arcade.color.RED, font_size=20, anchor_x="center")
                arcade.draw_text("Explanation: In Hard Mode, you will have 3 cards swapped on click from the bottom pile.", self.window.width / 2, self.window.height / 2 - 200,
                                arcade.color.LIGHT_GRAY, font_size=14, anchor_x="center", multiline=True, width=self.window.width - 220)
        else:
            if self.language == "RO":
                arcade.draw_text("Mod Normal Selectat", self.window.width / 2, self.window.height / 2 - 100,
                             arcade.color.GREEN, font_size=20, anchor_x="center")
                arcade.draw_text("Explicatie: In Modul Normal, vei avea 1 carte schimbata la apasarea pachetului de jos.", self.window.width / 2, self.window.height / 2 - 200,
                             arcade.color.LIGHT_GRAY, font_size=14, anchor_x="center", multiline=True, width=self.window.width - 220)
            elif self.language == "EN":
                arcade.draw_text("Normal Mode Selected", self.window.width / 2, self.window.height / 2 - 100,
                                arcade.color.GREEN, font_size=20, anchor_x="center")
                arcade.draw_text("Explanation: In Normal Mode, you will have 1 card swapped on click from the bottom pile.", self.window.width / 2, self.window.height / 2 - 200,
                                arcade.color.LIGHT_GRAY, font_size=14, anchor_x="center", multiline=True, width=self.window.width - 220)

        # Draw UI elements (buttons)
        self.ui_manager.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        """ Handle key press events """
        if symbol == arcade.key.SPACE:
            game_view = SolitaireView()
            game_view.setup(hard_mode=self.hard, language=self.language)
            self.window.show_view(game_view)
        elif symbol == arcade.key.N:
            self.hard = False
        elif symbol == arcade.key.H:
            self.hard = True

class WinningView(arcade.View):
    '''Winning Screen'''

    def __init__(self, time_taken: int = 0, moves: int = 0, language: str = "EN"):
        '''Initialize the view'''
        super().__init__()
        self.background = arcade.load_texture(WINNING_SCREEN)
        self.time_taken = time_taken
        self.moves = moves
        self.language = language
        self.fireworks_list = []
        self.next_firework_time = 0

    def on_show_view(self, language = "EN"):
        '''Called when view is activated'''
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self, language = "EN"):
        '''Draw the view'''
        language = self.language
        self.clear()
        self.language = language
        # Draw the timer inside a gray rectangle
        minutes = int(self.time_taken // 60)
        seconds = int(self.time_taken % 60)
        timer_text = f"{minutes:02d}:{seconds:02d}"

        # Draw the background image
        arcade.draw_lrwh_rectangle_textured(0, 0, self.window.width, self.window.height, self.background)

        if self.language == "RO":
            arcade.draw_text("Felicitari! Ai castigat!", self.window.width / 2, self.window.height / 2 + 100,
                         arcade.color.WHITE, font_size=40, anchor_x="center")
            arcade.draw_text("Ai reusit sa termini jocul...", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=40, anchor_x="center")
            arcade.draw_text("Ai pierdut cu succes...", self.window.width / 2, self.window.height / 2 - 50,
                        arcade.color.WHITE, font_size=30, anchor_x="center")
            # Show the time taken to win the game
            arcade.draw_text("Timp: ", self.window.width / 2, self.window.height / 2 - 100,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
            arcade.draw_text(timer_text, self.window.width / 2 + 140, self.window.height / 2 - 100,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
            # Show the number of moves to win the game
            arcade.draw_text("Miscari: ", self.window.width / 2, self.window.height / 2 - 150,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
            arcade.draw_text(str(self.moves), self.window.width / 2 + 140, self.window.height / 2 - 150,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
            arcade.draw_text("Nota: Apasa R pentru a reveni la meniul de inceput", self.window.width / 2, self.window.height / 2 - 350,
                        arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")
        elif self.language == "EN":
            arcade.draw_text("You have finished the game...", self.window.width / 2, self.window.height / 2,
                            arcade.color.WHITE, font_size=40, anchor_x="center")
            arcade.draw_text("You have successfully wasted...", self.window.width / 2, self.window.height / 2 - 50,
                            arcade.color.WHITE, font_size=30, anchor_x="center")
            # Show the time taken to win the game
            arcade.draw_text("Time: ", self.window.width / 2, self.window.height / 2 - 100,
                            arcade.color.WHITE, font_size=30, anchor_x="center")
            arcade.draw_text(timer_text, self.window.width / 2 + 140, self.window.height / 2 - 100,
                            arcade.color.WHITE, font_size=30, anchor_x="center")
            # Show the number of moves to win the game
            arcade.draw_text("Moves: ", self.window.width / 2, self.window.height / 2 - 150,
                            arcade.color.WHITE, font_size=30, anchor_x="center")
            arcade.draw_text(str(self.moves), self.window.width / 2 + 140, self.window.height / 2 - 150,
                            arcade.color.WHITE, font_size=30, anchor_x="center")
            arcade.draw_text("Note: Press R to get to Start", self.window.width / 2, self.window.height / 2 - 350,
                            arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")

        # Draw fireworks
        for fireworks in self.fireworks_list:
            fireworks.draw()

    def on_update(self, delta_time):
        '''Update the view'''
        current_time = time.time()
        if current_time > self.next_firework_time:
            self.next_firework_time = current_time + random.uniform(0.5, 1.5)
            firework_x = random.randint(100, self.window.width - 100)
            firework_y = random.randint(200, self.window.height - 100)
            self.fireworks_list.append(create_firework(firework_x, firework_y))

        for fireworks in self.fireworks_list:
            fireworks.update()
        self.fireworks_list = [fireworks for fireworks in self.fireworks_list if len(fireworks) > 0]

    def on_key_press(self, symbol: int, modifiers: int):
        """ If the user presses the mouse button, start the game. """
        if symbol == arcade.key.R:
            game_view = StartView()
            self.window.show_view(game_view)

class SolitaireView(arcade.View):
    '''Main Solitaire Game class'''

    def __init__(self, language="EN"):
        '''Initialize the game'''
        super().__init__()

        # Sprite list with all the cards
        self.card_list = None

        self.language = language

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

        # Last click time for double-click detection
        self.last_click_time = 0

    
    def setup(self, hard_mode: bool, language="EN"):
        '''Set up the game and also restart the game'''

        # Sprite list with all the cards
        self.held_cards = []

        # Set the language
        self.language = language
        
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
        if self.language == "RO":
            arcade.draw_text("Timp", rect_x-90, rect_y,
                         arcade.color.BLACK, 20, anchor_x="center", anchor_y="center")
        elif self.language == "EN":
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
        if self.language == "RO":
            arcade.draw_text("Miscari", points_rect_x-90, points_rect_y,
                         arcade.color.BLACK, 20, anchor_x="center", anchor_y="center")
        elif self.language == "EN":
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

        curr_time = time.time()
        double_click = curr_time - self.last_click_time < 0.3
        self.last_click_time = curr_time

        # Get list of cards that were clicked
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # If we clicked on a card, grab it
        if len(cards) > 0:

            # Get the top card (might be a stack of cards)
            top_card = cards[-1]

            # Figure out which pile the card is in
            pile_index = self.get_pile_for_card(top_card)

            # If we double-clicked, try to move the card to a top pile
            if double_click and top_card.is_face_up:
                for top_pile_index in range(TOP_PILE_1, TOP_PILE_4 + 1):
                    # If the card is the top card of the pile
                    if self.can_add_to_top_pile(top_card, top_pile_index):
                        self.move_card_to_new_pile(top_card, top_pile_index)
                        top_card.position = self.pile_mat_list[top_pile_index].position
                        top_card.is_face_up = True
                        self.pull_to_top(top_card)  # Adjust z-order
                        self.moves += 1
                        # --- Win check
                        self.check_winning()
                        return
            elif pile_index == BOTTOM_FACE_DOWN_PILE:
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

    def can_add_to_top_pile(self, card, pile_index):
        '''Check if a card can be added to a top pile'''
        if len(self.piles[pile_index]) == 0:
            return card.value == 'A'
        top_card = self.piles[pile_index][-1]
        return top_card.suit == card.suit and CARD_VALUES.index(top_card.value) + 1 == CARD_VALUES.index(card.value)

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

        # Check if we are in contact with the closest mat or the cards in it
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
        else:
            # Check if we are over a card pile
            for pile_index in range(PILE_COUNT):
                if len(self.piles[pile_index]) > 0:
                    top_card = self.piles[pile_index][-1]
                    if arcade.check_for_collision(self.held_cards[0], top_card):
                        if pile_index >= PLAY_PILE_1 and pile_index <= PLAY_PILE_7:
                            if top_card.colour != self.held_cards[0].colour and \
                                    CARD_VALUES.index(top_card.value) - 1 == CARD_VALUES.index(self.held_cards[0].value):
                                # Move cards to proper position
                                for i, dropped_card in enumerate(self.held_cards):
                                    dropped_card.position = top_card.center_x, \
                                                            top_card.center_y - CARD_VERTICAL_OFFSET * (i + 1)
                                reset_position = False
                                self.moves += 1
                                for card in self.held_cards:
                                    self.move_card_to_new_pile(card, pile_index)
                                break
                        elif pile_index >= TOP_PILE_1 and pile_index <= TOP_PILE_4 and len(self.held_cards) == 1:
                            if top_card.suit == self.held_cards[0].suit and \
                                    CARD_VALUES.index(top_card.value) + 1 == CARD_VALUES.index(self.held_cards[0].value):
                                self.move_card_to_new_pile(self.held_cards[0], pile_index)
                                self.held_cards[0].position = top_card.position
                                reset_position = False
                                self.moves += 1
                                break
        if reset_position:
            # Reset position of the cards
            for i, card in enumerate(self.held_cards):
                card.position = self.held_cards_original_position[i]

        # We are no longer holding cards
        self.held_cards = []

        # --- Win check
        self.check_winning()

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
                return
        # Show the winning window
        view = WinningView(self.elapsed_time, self.moves, language=self.language)
        self.window.show_view(view)

def main():
    '''Main function to run the game'''
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()