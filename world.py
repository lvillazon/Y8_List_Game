from math import copysign
import characters
from config import *
from console_messages import console_msg
from dummy_session import DummySession
from panel import Panel
import point
from terrain import Terrain
from talking_head import TalkingHead
from farm_editor import FarmCodeWindow


class World:
    def __init__(self, screen):
        console_msg('Initialising world', 0)
        self.display = screen
        self.zoom = 0.6
        self.terrain = Terrain(screen, 5, 8, self.zoom)
        self.viewpoint = Point(screen.get_width() // 2,
                               screen.get_height() // 2)
        self.old_viewpoint = Point(0,0)
        self.drag_start = Point(0,0)

        # UI panels
        self.talking_head = TalkingHead(screen, Point(0,0), Point(700, 200))
        self.basket = Panel(screen,
                            Point(screen.get_width()-200,0),
                            Point(200, screen.get_height())
                            )

        # Characters
        self.farmer = characters.Robot("Bob",
                                       self,
                                       "assets\\green_bears_left.png",
                                       Point(2,4),
                                       self.zoom)

        # load fonts
        if pygame.font.get_init() is False:
            pygame.font.init()
            console_msg("Font system initialised", 2)
        # we're not using the built-in SysFont any more
        # so that the TTF file can be bundled to run on other PCs
        self.code_font = pygame.font.Font(CODE_FONT_FILE, 18)
        console_msg("Deja Vu Sans Mono font loaded", 3)

        self.dummy_session = DummySession()
        self.editor = FarmCodeWindow(screen,
                                 300,
                                 self.code_font,
                                 self.farmer, # where the code is hosted
                                 self.dummy_session,
                                 width=(self.display.get_width()
                                        - self.basket.size.x))
        self.editor_position = (0, WINDOW_SIZE.y - self.editor.height)

        self.running = True
        self.frame_counter = 0
        self.clock = pygame.time.Clock()

    def blit_alpha(self, target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)

    def update(self):
        # handle mouse and keyboard events
        self.check_keyboard_and_mouse()

        # render all onscreen objects
        self.display.fill(SKY_BLUE)
        landscape = self.terrain.update(self.viewpoint)
        offset_position = Point(self.display.get_width()
                                - landscape.get_width() // 2
                                - self.viewpoint.x,
                                self.display.get_height()
                                - landscape.get_height() // 2
                                - self.viewpoint.y)

        self.display.blit(landscape, offset_position)
        # calculate the pixel coords of the farmer's grid tile
        sprite = self.farmer.get_sprite()
        raw_ground_position = self.terrain.get_ground_coords(self.farmer.position)
        # offset this position so the sprite appears to be standing
        # in the middle of the tile
        sprite_position = Point((raw_ground_position.x
                                  #- self.terrain.get_tile_increment().x#//2
                                  - sprite.get_width()//2
                                  ),
                                 (raw_ground_position.y
                                  - sprite.get_height()
                                  + self.terrain.get_tile_increment().y * 1.5
                                  )
                                 )
        # add the viewpoint offset
        final_position = point.add_points(sprite_position, offset_position)
        # self.display.blit(sprite, position,
        #                   special_flags=pygame.BLEND_MULT)
        self.blit_alpha(self.display, sprite, final_position, 255)
        # DEBUG bounding box
        if BOUNDING_BOX:  # used for debug
            box = pygame.Rect(final_position,
                              (sprite.get_width(), sprite.get_height()))
            pygame.draw.rect(self.display, "red", box, 2)

        # draw any speech bubbles
        if self.farmer.speaking:
            position = point.add_points(final_position,
                                        self.farmer.get_speech_bubble_offset())

            # if self.farmer.facing_right:
            #     position[X] += ???  # to put the callout spike next to his mouth
            self.display.blit(self.farmer.get_speech_bubble(), position)

        #self.talking_head.update()
        self.basket.update()
        self.editor.draw()
        self.display.blit(self.editor.surface, self.editor_position)
        pygame.display.update()

        self.clock.tick()
        self.frame_counter += 1
        if self.frame_counter > 200:  # to avoid slowdown due to fps spam
            #print(int(self.clock.get_fps()))
            self.frame_counter = 0

    def mouse_over_editor(self) -> bool:
        # returns true if the mouse pointer is anywhere within the code pane
        editor_rect = pygame.Rect(self.editor_position,
                                  (self.editor.width, self.editor.height)
                                  )
        return editor_rect.collidepoint(pygame.mouse.get_pos())

    def check_keyboard_and_mouse(self):
        # check for context switch between game area and code editor
        # this is done by peeking the events so that we don't empty the
        # event queue and it can still be handled by whichever context
        # is active
        if pygame.event.peek(pygame.MOUSEBUTTONDOWN):
            if self.mouse_over_editor():
                self.editor.active = True
            else:
                self.editor.active = False

        # handle events in the appropriate context
        if self.editor.is_active():
            self.editor.update()
        else:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:  # LMB
                        if self.talking_head.mouse_over():
                            self.talking_head.cycle_head()
                        else:
                            # terrain window, so we are dragging
                            self.drag_start = Point(*pygame.mouse.get_pos())
                            self.old_viewpoint = self.viewpoint
                    elif pygame.mouse.get_pressed()[2]:  # right button
                        self.terrain.rotate()
                elif event.type == pygame.MOUSEWHEEL:
                    if not self.editor.is_active():
                        min_zoom = .1
                        max_zoom = 10
                        # adjust zoom level by +/- 10%
                        self.zoom *= 1 + .1 * copysign(1, event.y)
                        # constrain zoom between min_ and max_
                        self.zoom = min(max(self.zoom, min_zoom), max_zoom)
                        self.terrain.change_zoom(self.zoom)
                        self.farmer.change_zoom(self.zoom)

            # check for ongoing mouse-drag
            if pygame.mouse.get_pressed()[0]:  # LMB held down
                if not self.talking_head.mouse_over() and self.drag_start:
                    drag_x = self.drag_start.x - pygame.mouse.get_pos()[0]
                    drag_y = self.drag_start.y - pygame.mouse.get_pos()[1]
                    self.viewpoint = Point(self.old_viewpoint.x + drag_x,
                                           self.old_viewpoint.y + drag_y)

    def busy(self):
        """ returns true if there is anything happening that must complete
        before the interpreter continues running the player's code.
        This allows us to halt code execution while certain animations
        complete for example.

        At the moment nothing triggers the busy state, but we
        will probably want to set it when the farmer is completing an action
        eg moving
        """

        return False