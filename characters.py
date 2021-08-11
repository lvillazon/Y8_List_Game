import contextlib
import io
import string
import pygame

import farm_interpreter
import spritesheet
from config import *
from console_messages import console_msg
from farm_interpreter import VirtualMachine
from terrain import Terrain
from text_panel import SpeechBubble


class Character:
    # sprites that animate around the grid
    # currently just the farmer
    def __init__(self, name, world, image_file: string,
                 start_position: Point, zoom):
        self.name = name
        self.world = world
        raw_sprites = spritesheet.SpriteSheet(image_file, 1, 3, 1)
        self._sprite = raw_sprites.sprites[1][0]
        self._zoomed_sprite = None
        self._magnification = 1.0
        self.change_zoom(zoom)
        self.position = start_position  # grid coords on the terrain
        self.facing = "left"

    def change_zoom(self, zoom):
        # appply a fixed conversion factor so that the sprite looks
        # right for the terrain tiles. This will change if the characters
        # are redrawn at a different resolution
        new_magnification = zoom * 0.5
        print("zoom=",zoom)
        if (self._magnification != new_magnification
            or self._zoomed_sprite == None):
            self._magnification = new_magnification
            if zoom < SMOOTH_ZOOM_THRESHOLD:
                self._zoomed_sprite = pygame.transform.smoothscale(
                    self._sprite,
                    (
                        int(self._sprite.get_width() * self._magnification),
                        int(self._sprite.get_height() * self._magnification)
                    )
                )
            else:
                self._zoomed_sprite = pygame.transform.scale(
                    self._sprite,
                    (
                        int(self._sprite.get_width() * self._magnification),
                        int(self._sprite.get_height() * self._magnification)
                    )
            )

    def get_sprite(self):
        if self._zoomed_sprite != None:
            return self._zoomed_sprite
        else:
            return self._sprite

class Robot(Character):
    ''' an agent capable of running programs
    In Thingummy farm, currently only the farmer bear can do this
    but other objects might include this ability later '''

    def __init__(self, name, world, image_file: string,
                 start_position: Point, zoom):
        super().__init__(name, world, image_file, start_position, zoom)
        self.speaking = False
        self.speech_bubble = None
        self.python_interpreter = VirtualMachine(self)
        console_msg(name + " command interpreter initialised", 2)
        self.source_code = []
        self.output = []
        self.x = 67
        # this dictionary contains all the special variables that
        # can be used in player programs, together with the variable
        # or property that they access. This dictionary is used to
        # update the locals and globals dicts in the interpreter,
        # so make sure you don't have magic variables called
        # __builtins__, __name__, __main__, __doc__ or __package__
        # or you will overwrite the existing ones with unpredictable effects
        # if we want to reinstate sync_world_variables in Interpreter,
        # each magic_variable entry should be a tuple, with getter and setter
        # references for each one. But maybe we need a more sophisticated
        # system anyway to handle all the list methods...
        self.magic_variables = {
            'bob_x': self.x,
        }
        # read/write variables need special treatment,
        # so we track them separately
        self.writable_names = [] #['bit_x', 'bit_y']  # , 'data']

    def set_source_code(self, text):
        pass

    def run_program(self):
        """ pass the text in the editor to the interpreter"""
        # run_enabled is set false on each run
        # and cleared using the reset button
        if self.python_interpreter.run_enabled:
            self.clear_all_output()
            p = self.python_interpreter  # for brevity
            p.load(self.get_source_code())
            result, errors = p.compile()
            if result is False:  # check for syntax errors
                # TODO display these using in-game dialogs
                if p.compile_time_error:
                    error_msg = p.compile_time_error['error']
                    error_line = p.compile_time_error['line']
                    console_msg(self.name + ' SYNTAX ERROR:', 5)
                    msg = error_msg + " on line " + str(error_line)
                    console_msg(msg, 5)
            else:
                result, errors = p.run()  # set the program going
            return result, errors
        return False, "RUN NOT ENABLED"

    def halt_program(self):
        pass

    def validate_attempt(self):
        return True

    def say(self, *t):
        # show the message t in a speak-bubble above the character
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            print(*t, end='')  # TODO use a different way of suppressing ugly chars for carriage returns, that allows the user programs to still use the end= keyword
            speech = f.getvalue()
            self.output.append(speech)

        self.create_speech_bubble(speech,
                                 self.world.editor.get_fg_color(),
                                 self.world.editor.get_bg_color())

    def error(self, msg, type="Syntax error!"):
        # show the error in a speak-bubble above the character
        self.create_speech_bubble(type + msg,
                                  (0, 0, 0),
                                  (254, 0, 0))  # red, but not 255 because that's the alpha

    def input(self, msg=''):
        # get input from the user in a separate editor window
        self.world.input.activate('input:' + msg)
        while self.world.input.is_active():
            self.world.update(self)
        result = self.world.input.convert_to_lines()[0]
        console_msg("input:" + str(result), 8)
        return result

    def clear_all_output(self):
        # blanks the speech bubble, if present
        # and also the internal record of the program output
        if self.speech_bubble:
            self.speech_bubble.clear()
            self.speaking = False
        self.output=[]

    def clear_speech_bubble(self):
        self.speech_bubble = None
        self.speaking = False

    def create_speech_bubble(self, text, fg_col, bg_col):
        # show a speak-bubble above the character with the text in it
        new_text = str(text)
        # make sure speech bubble has at least 1 character width
        # non-printing chars or empty strings make the bubble look weird
        if (self.world.code_font.size(new_text)[X]
            < self.world.code_font.size(" ")[X]):
            new_text = new_text + " "
        if self.speech_bubble:
            self.speech_bubble.append(new_text)
        else:
            self.speech_bubble = SpeechBubble(text, fg_col, bg_col, self.world.code_font)
        self.speaking = True

    def get_speech_bubble(self):
        if self.facing == "right":
            return self.speech_bubble.rendered(mirror=False)
        else:
            return self.speech_bubble.rendered(mirror=True)

    def get_speech_bubble_offset(self):
        # returns the x,y offset to position the speech callout spike
        # in the correct location for the character facing
        if self.facing == "right":
            return Point(self.get_sprite().get_width(), 0)
        else:
            return Point(-self.speech_bubble.get_outline_rect().width, 0)

    def speech_position(self):
        # position the tip of the speak bubble at the middle
        # of the top edge of the sprite box
        position = (800,200)
        #position = [self.location.x, self.location.y
        # - self.speech_bubble.get_rendered_text_height() / SCALING_FACTOR - 8]
        # the -8 is a fudge factor to put the speech bubble
        # just above the sprite
        return position

    def get_source_code(self):
        # convert code from a list of lists of chars (as supplied by code editor)
        # to a list of strings (as required by the interpreter)
        return farm_interpreter.convert_to_lines(self.source_code)

    def set_source_code(self, statement_list):
        self.source_code = statement_list

    def add_magic_variable(self):
        # update the magic_variables dictionary
        # this can't be done by manipulating the variable directly,
        # because this wouldn't update the
        pass

class Farmer(Robot):
    """ a farmer is a programmable entity who is also able to till the soil.
    This means they have access to the list of furrows from the World
    object. Currently Farmer Bob is the only farmer."""

    def __init__(self, name, world, image_file: string,
                 start_position: Point, zoom, furrows):
        super().__init__(name, world, image_file, start_position, zoom)
        self.furrows = furrows
        self.magic_variables['row1'] = self.furrows[0]
        #self.add_magic_variable('furrows', self.furrows)

