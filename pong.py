#!/usr/bin/python3
#
# Tom's Pong
# A simple pong game with realistic physics and AI
# http://www.tomchance.uklinux.net/projects/pong.shtml
#
# Released under the GNU General Public License

VERSION = "0.4"

try:
        import sys
        import random
        import math
        import os
        import getopt
        import pygame
        import pygbutton
        from socket import *
        from pygame.locals import *
except ImportError as err:
        print("couldn't load module. %s" % (err))
        sys.exit(2)

def load_png(name):
        """ Load image and return image object"""
        fullname = os.path.join('data', name)
        try:
                image = pygame.image.load(fullname)
                if image.get_alpha is None:
                        image = image.convert()
                else:
                        image = image.convert_alpha()
        except pygame.error as message:
                print('Cannot load image:', fullname)
                raise SystemExit(message)
        return image, image.get_rect()

class Ball(pygame.sprite.Sprite):
        """A ball that will move across the screen
        Returns: ball object
        Functions: update, calcnewpos
        Attributes: area, vector"""

        def __init__(self, xy, vector):
                pygame.sprite.Sprite.__init__(self)
                self.image, self.rect = load_png('ball.png')
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.vector = vector
                self.hit = 0

        def update(self):
                newpos = self.calcnewpos(self.rect,self.vector)
                self.rect = newpos
                (angle,z) = self.vector

                if not self.area.contains(newpos):
                        tl = not self.area.collidepoint(newpos.topleft)
                        tr = not self.area.collidepoint(newpos.topright)
                        bl = not self.area.collidepoint(newpos.bottomleft)
                        br = not self.area.collidepoint(newpos.bottomright)
                        if tr and tl or (br and bl):
                                angle = -angle
                        if tl and bl:
                                #self.offcourt()
                                angle = math.pi - angle
                        if tr and br:
                                angle = math.pi - angle
                                #self.offcourt()
                else:
                        # Deflate the rectangles so you can't catch a ball behind the bat
                        player1.rect.inflate(-3, -3)
                        player2.rect.inflate(-3, -3)

                        # Do ball and bat collide?
                        # Note I put in an odd rule that sets self.hit to 1 when they collide, and unsets it in the next
                        # iteration. this is to stop odd ball behaviour where it finds a collision *inside* the
                        # bat, the ball reverses, and is still inside the bat, so bounces around inside.
                        # This way, the ball can always escape and bounce away cleanly
                        if self.rect.colliderect(player1.rect) == 1 and not self.hit:
                                angle = math.pi - angle
                                self.hit = not self.hit
                        elif self.rect.colliderect(player2.rect) == 1 and not self.hit:
                                angle = math.pi - angle
                                self.hit = not self.hit
                        elif self.hit:
                                self.hit = not self.hit
                self.vector = (angle,z)

        def calcnewpos(self,rect,vector):
                (angle,z) = vector
                (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
                return rect.move(dx,dy)

class Bat(pygame.sprite.Sprite):
        """Movable tennis 'bat' with which one hits the ball
        Returns: bat object
        Functions: reinit, update, moveup, movedown
        Attributes: which, speed"""

        def __init__(self, side):
                pygame.sprite.Sprite.__init__(self)
                self.image, self.rect = load_png('bat.png')
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.side = side
                self.speed = 10
                self.state = "still"
                self.reinit()

        def reinit(self):
                self.state = "still"
                self.movepos = [0,0]
                if self.side == "left":
                        self.rect.midleft = self.area.midleft
                elif self.side == "right":
                        self.rect.midright = self.area.midright

        def update(self):
                newpos = self.rect.move(self.movepos)
                if self.area.contains(newpos):
                        self.rect = newpos
                pygame.event.pump()

        def moveup(self):
                self.movepos[1] = self.movepos[1] - (self.speed)
                self.state = "moveup"

        def movedown(self):
                self.movepos[1] = self.movepos[1] + (self.speed)
                self.state = "movedown"

 

 
# class GameMenu():
#     def __init__(self, screen, bg_color=(0,0,0)):
 
#         self.screen = screen
#         self.bg_color = bg_color
#         self.clock = pygame.time.Clock()
 
#     def run(self):
#         mainloop = True
#         while mainloop:
#             # Limit frame speed to 50 FPS
#             self.clock.tick(50)
 
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     mainloop = False
 
#             # Redraw the background
#             self.screen.fill(self.bg_color)
#             pygame.display.flip()
 
# if __name__ == "__main__":
#     # Creating the screen
#     screen = pygame.display.set_mode((640, 480), 0, 32)
#     pygame.display.set_caption('Game Menu')
#     gm = GameMenu(screen)
#     gm.run()

def menu():
        screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('Menu')
        background = pygame.image.load("Sather Tower.png")
        backgroundRect = background.get_rect()

        # myfont = pygame.font.SysFont(None, 30)
        # font_color=(255, 255, 255)
        # items = ('Start', 'Quit')
        # menu_items = ()
        # for item in items:
        #     label = self.font.render(item, 1, font_color)
        #     menu_items.append(label)
        StartButton = pygbutton.PygButton(None, 'Start')
        QuitButton = pygbutton.PygButton(None, 'Quit')

        screen.blit(background, (0, 0))
        pygame.display.flip()



        # Initialise clock
        clock = pygame.time.Clock()

        while 1:
        # # Make sure game doesn't run at more than 60 frames per second
        # Limit frame speed to 50 FPS
            clock.tick(50)

            for event in pygame.event.get():

                if event.type == QUIT:
                    return
                else:
                    StartEvent = StartButton.handleEvent(event)
                    QuitEvent = QuitButton.handleEvent(event)
                    for subEvents in StartEvent:
                        if subEvents == 'down':
                            main()
                            return
                    for subEvents in QuitEvent:
                        if subEvents == 'down':
                            return


            screen.blit(background, backgroundRect)
            
            StartButton.draw(screen)
            StartButton._propGetRect().top = 20
            QuitButton.draw(screen)
            QuitButton._propGetRect().top = 120

            pygame.display.flip()



def main():
        # Initialise screen
        # pygame.init()
        screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('Basic Pong')

     
        # Fill background
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))

        # Initialise players
        global player1
        global player2
        player1 = Bat("left")
        player2 = Bat("right")

        # Initialise ball
        speed = 5
        rand = ((0.1 * (random.randint(5,8))))
        ball = Ball((0,0),(0.47,speed))

        # Initialise sprites
        playersprites = pygame.sprite.RenderPlain((player1, player2))
        ballsprite = pygame.sprite.RenderPlain(ball)

        # Blit everything to the screen
        screen.blit(background, (0, 0))
        pygame.display.flip()

        # Initialise clock
        clock = pygame.time.Clock()

        RestartButton = pygbutton.PygButton(None, 'Restart')

        # Event loop
        while 1:
                # Make sure game doesn't run at more than 60 frames per second
                clock.tick(60)

                for event in pygame.event.get():
                        RestartEvent = RestartButton.handleEvent(event)
                        for subEvents in RestartEvent:
                            if subEvents == 'down':
                                main()
                                return
                        if event.type == QUIT:
                                return
                        elif event.type == KEYDOWN:
                                if event.key == K_a:
                                        player1.moveup()
                                if event.key == K_z:
                                        player1.movedown()
                                if event.key == K_UP:
                                        player2.moveup()
                                if event.key == K_DOWN:
                                        player2.movedown()
                        elif event.type == KEYUP:
                                if event.key == K_a or event.key == K_z:
                                        player1.movepos = [0,0]
                                        player1.state = "still"
                                if event.key == K_UP or event.key == K_DOWN:
                                        player2.movepos = [0,0]
                                        player2.state = "still"

                screen.blit(background, ball.rect, ball.rect)
                screen.blit(background, player1.rect, player1.rect)
                screen.blit(background, player2.rect, player2.rect)
                ballsprite.update()
                playersprites.update()
                ballsprite.draw(screen)
                playersprites.draw(screen)
                pygame.display.flip()
                RestartButton.draw(screen)
    


if __name__ == '__main__': menu()
