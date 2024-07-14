'''
Solitaire Game written in Python
'''

import arcade
from card import Card, CARD_SUITS, CARD_VALUES, CARD_SCALE, START_X, BOTTOM_Y

# Screen dimensions
WIDTH = 1024
HEIGHT = 768
TITLE = "Solitaire Game"

class Solitaire(arcade.Window):
    '''Main Solitaire Game class'''

    def __init__(self):
        '''Initialize the game'''
        super().__init__(WIDTH, HEIGHT, TITLE)

        # Sprite list with all the cards
        self.card_list = None

        arcade.set_background_color(arcade.color.AMAZON) # Set background color to Card Table Green (Amazon)

        # List of cards that we will drag with the mouse
        self.held_cards = None

        # Original location of cards we are dragging
        # They might need to get back
        self.held_cards_original_position = None
    
    def setup(self):
        '''Set up the game and also restart the game'''

        # Sprite list with all the cards
        self.card_list = []

        # Original location of cards we are dragging
        # They might need to get back
        self.held_cards_original_position = []
        
        # Sprite list with all the cards
        self.card_list = arcade.SpriteList()

        # Create the cards
        for suit in CARD_SUITS:
            for value in CARD_VALUES:
                card = Card(suit, value, CARD_SCALE)
                card.position = START_X, BOTTOM_Y
                self.card_list.append(card)

    def on_draw(self):
        '''Render the screen'''
        # Clear the screen
        self.clear()
        
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