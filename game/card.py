'''
Card class for Solitaire Game
'''

import arcade
import os
import sys

# Function to get the correct path to resources
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

FACE_DOWN_IMAGE = resource_path("sprites/cover/cover.jpg")

class Card(arcade.Sprite):
    '''Card class for Solitaire Game'''
    
    def __init__(self, suit, value, scale: float = 1):
        '''Initialize the card'''
        self.suit = suit
        self.value = value
        self.colour = 'red' if suit in ['Hearts', 'Diamonds'] else 'black'

        # Image to use for the sprite when face up
        self.image_file_name = resource_path(f"sprites/{self.suit}/{self.value}.jpg")
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