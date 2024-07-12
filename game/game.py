'''
Solitaire Game written in Python
'''

import arcade

# Screen dimensions
WIDTH = 1024
HEIGHT = 768
TITLE = "Solitaire Game"

class Solitaire(arcade.Window):
    '''Main Solitaire Game class'''

    def __init__(self):
        '''Initialize the game'''
        super().__init__(WIDTH, HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.AMAZON) # Set background color to Card Table Green (Amazon)
    
    def setup(self):
        '''Set up the game and also restart the game'''
        pass

    def on_draw(self):
        '''Render the screen'''
        # Clear the screen
        self.clear()
        # arcade.start_render()
    
    def on_mouse_press(self, x, y, button, key_modifiers):
        '''Handle mouse click events'''
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        '''Handle mouse motion events'''
        pass

def main():
    '''Main function to run the game'''
    window = Solitaire()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()