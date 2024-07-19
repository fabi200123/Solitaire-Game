'''
Card class for Solitaire Game
'''

import arcade

FACE_DOWN_IMAGE = "./sprites/cover/cover.jpg"

class Card(arcade.Sprite):
    '''Card class for Solitaire Game'''
    
    def __init__(self, suit, value, scale: float =1):
        '''Initialize the card'''

        self.suit = suit
        self.value = value
        self.colour = 'red' if suit in ['Hearts', 'Diamonds'] else 'black'

        # Image to use for the sprite when face up
        self.image_file_name = f"sprites/{self.suit}/{self.value}.jpg"
        self.is_face_up = False
        
        # Call the parent class's init function
        super().__init__(FACE_DOWN_IMAGE, scale, hit_box_algorithm='None')

    def face_down(self):
        '''Turn the card face down'''
        self.texture = arcade.load_texture(FACE_DOWN_IMAGE)
        self.is_face_up = False

    def face_up(self):
        '''Turn the card face up'''
        self.texture = arcade.load_texture(self.image_file_name)
        self.is_face_up = True

    @property
    def is_face_down(self):
        '''Return True if the card is face down'''
        return not self.is_face_up