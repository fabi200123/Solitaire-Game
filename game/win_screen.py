'''
Winning Screen
'''

import arcade.gui

class WinScreen(arcade.Window):
    '''Winning Screen'''

    def __init__(self, width, height, title):
        '''Initialize the screen'''
        super().__init__(width, height, title)
        self.width = width
        self.height = height
        arcade.set_background_color(arcade.color.GRAY)
    
    def on_draw(self):
        '''Draw the screen'''
        arcade.start_render()
        arcade.draw_text("You Win!", self.width/2, self.height/2,
                         arcade.color.BLACK, 20, anchor_x="center")