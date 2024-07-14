'''
Card class for Solitaire Game
'''

import arcade

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