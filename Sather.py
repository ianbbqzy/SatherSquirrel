import pygame

import pygbutton

pygame.init()
size = width, height = 1024, 768
startPoint = leftbound, noUse = 110, 160
fstartPoint = 110, 450
gameoverPoint = 112, 84
lowerbound, upperbound = 700, 35

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

def load_png(name):
    try:
        image = pygame.image.load(name)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
        image = pygame.transform.scale(image, (68, 25))
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    return image, image.get_rect()

class Squirrel(pygame.sprite.Sprite):

    screen = pygame.display.get_surface()

    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("jumpping squirrel.png")
        self.thisimage = self.image
        self.otherimage, nothing = load_png("up_jumping squirrel.png")
        self.rect.move_ip(startPoint)
        
        from random import uniform
        self.speed = [uniform(2, 20), -1]
        self.alive = True
        self.timeBeforeDisappear = 1000000
        self.type = "Squirrel"

    def getPos(self):
        return [self.rect.top, self.rect.bottom, self.rect.left, self.rect.right]

    def bounce(self):
        self.thisimage = pygame.transform.flip(self.thisimage, True, False)
        self.otherimage = pygame.transform.flip(self.otherimage, True, False)
        self.speed[0] *= -1

    def die(self):
        self.speed = [0, 0]
        self.alive = False
        self.image, noUse = load_png("die.png")
        self.timeBeforeDisappear = 300

    def live(self):
        self.speed = [0, 0]
        self.alive = False

    def flip(self):
        self.image = self.otherimage

    def stay(self):
        self.image = self.thisimage

    def move(self, acceleration):
        self.rect = self.rect.move(self.speed)
        self.speed[1] += acceleration

class FSquirrel(Squirrel):
    def __init__(self):
        Squirrel.__init__(self)
        self.otherimage, nothing = load_png("jumpping fsquirrel.png")
        self.thisimage , nothing = load_png("up_jumping fsquirrel.png")
        self.image = self.thisimage
        self.rect.move_ip(fstartPoint)
        self.timeBeforeDisappear = 6000
    
    def move(self, acceleration):
        self.rect = self.rect.move(self.speed)
        self.speed[1] -= acceleration

class SSquirrel(Squirrel):
    def __init__(self):
        Squirrel.__init__(self)
        self.otherimage, nothing = load_png("jumpping ssquirrel.png")
        self.thisimage , nothing = load_png("dying ssquirrel.png")
        self.image = self.thisimage
        from random import uniform
        x = uniform(220, 700)
        y = uniform(200, 500)
        start = x, y
        self.rect.move_ip(start)
        self.type = "SSquirrel"
        self.timeBeforeDisappear = 2000

    def move(self, acceleration):
        return
        #do nothing


def menu():
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        screen = pygame.display.set_mode((1024, 768))
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
        rect = pygame.Rect(512 - 50, 384, 100, 100)
        rect2 = pygame.Rect(512 - 50, 384 - 100, 100, 100)
        rect3 = pygame.Rect(512 - 50, 384 + 100, 100, 100)
        StartButton = pygbutton.PygButton(rect2, 'Special')
        QuitButton = pygbutton.PygButton(rect3, 'Quit')
        NormalButton = pygbutton.PygButton(rect, 'Normal')     

        screen.blit(background, (0, 0))
        pygame.display.flip()
        pygame.mixer.music.load('DiabloRojo.ogg')


        # Initialise clock
        clock = pygame.time.Clock()

        while 1:
        # # Make sure game doesn't run at more than 60 frames per second
        # Limit frame speed to 50 FPS
            clock.tick(50)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return
                else:
                    StartEvent = StartButton.handleEvent(event)
                    QuitEvent = QuitButton.handleEvent(event)
                    NormalEvent = NormalButton.handleEvent(event)
                    for subEvents in StartEvent:
                        if subEvents == 'down':
                            main()
                            return
                    for subEvents in NormalEvent:
                        if subEvents == 'down':
                            main2()
                            return
                    for subEvents in QuitEvent:
                        if subEvents == 'down':
                            return


            screen.blit(background, backgroundRect)
            
            StartButton.draw(screen)
            #StartButton._propGetRect().top = 20
            QuitButton.draw(screen)
            #QuitButton._propGetRect().top = 120
            NormalButton.draw(screen)

            pygame.display.flip()




def main():
    squirrels = []
    for i in range(10):
        from random import random
        s = random()
        if s > 0.3:
            squirrels += [Squirrel()]
        elif s > 0.1:
            squirrels += [FSquirrel()]
        else:
            squirrels += [SSquirrel()]
        
    squirrels[0].startTime = 0
    for i in range(1, 10):
        from random import randint
        squirrels[i].startTime = squirrels[i - 1].startTime + randint(700, 1000)

    background = pygame.image.load("background.psd")
    backgroundRect = background.get_rect()

    gameover = pygame.image.load("gameover.png")
    gameoverRect = gameover.get_rect()
    gameoverRect.move_ip(gameoverPoint)

    win = pygame.image.load("win.png")
    winRect = win.get_rect()
    winRect.move_ip(gameoverPoint)

    firstlevel = pygbutton.PygButton(None, 'Fisrt Level')
    secondlevel = pygbutton.PygButton(None, 'Second Level') 
    thirdlevel = pygbutton.PygButton(None, 'Third Level')
    fourthlevel = pygbutton.PygButton(None, 'Fourth Level')

    a = [1, 1, 1, 1]
    time = 0
    safeNum = 0
    diedNum = 0
    tag = True
    myfont = pygame.font.SysFont("monospace", 60)
    pygame.mixer.music.play(loops = 0, start = 0.0)
    rect3 = pygame.Rect(900, 50, 100, 100)
    RestartButton = pygbutton.PygButton(rect3, 'Menu')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            firstlevelEvent = firstlevel.handleEvent(event)
            secondlevelEvent = secondlevel.handleEvent(event)
            thirdlevelEvent = thirdlevel.handleEvent(event)
            fourthlevelEvent = fourthlevel.handleEvent(event)
            RestartEvent = RestartButton.handleEvent(event)
            for subEvents in RestartEvent:
                if subEvents == 'down':
                    menu()
                    return
            for subEvents in firstlevelEvent:
                if subEvents == 'down':
                    a[0] = -2.4
                elif subEvents == 'up':
                    a[0] = 1
                    tag = True
            for subEvents in secondlevelEvent:
                if subEvents == 'down':
                    a[1] = -2
                elif subEvents == 'up':
                    a[1] = 1
                    tag = True
            for subEvents in thirdlevelEvent:
                if subEvents == 'down':
                    a[2] = -1.6
                elif subEvents == 'up':
                    a[2] = 1
                    tag = True
            for subEvents in fourthlevelEvent:
                if subEvents == 'down':
                    a[3] = -1.2
                elif subEvents == 'up':
                    a[3] = 1
                    tag = True
        firstlevel.draw(screen)
        firstlevel._propGetRect().top = 230
        secondlevel.draw(screen)
        secondlevel._propGetRect().top = 230 + 117.5
        thirdlevel.draw(screen)
        thirdlevel._propGetRect().top = 230 + 117.5 * 2
        fourthlevel.draw(screen)
        fourthlevel._propGetRect().top = 230 + 117.5 * 3
        screen.blit(background, backgroundRect)
        RestartButton.draw(screen)
        if safeNum + diedNum == 10:
            if safeNum >= 5:
                screen.blit(win, winRect)
            else:
                screen.blit(gameover, gameoverRect)
        else:
            for i in range(10):
                if time >= squirrels[i].startTime and squirrels[i].timeBeforeDisappear >= 0:
                    screen.blit(squirrels[i].image, squirrels[i].rect)
                    if squirrels[i].alive:
                        h = squirrels[i].getPos()[0]
                        if h < 230:
                            squirrels[i].move(1)
                        else:
                            num = round((h - 230) / 117.5)
                            if num > 3:
                                num = 3
                            if a[num] < 0:
                                if squirrels[i].type == "SSquirrel" and tag:
                                    if squirrels[i].image == squirrels[i].thisimage:
                                        squirrels[i].flip()
                                    else:
                                        squirrels[i].die()
                                        diedNum += 1
                                    tag = False
                                else:
                                    squirrels[i].flip()
                            else:
                                if squirrels[i].type != "SSquirrel":
                                    squirrels[i].stay()
                            squirrels[i].move(a[num])
                    if squirrels[i].getPos()[0] < upperbound or squirrels[i].getPos()[1] > lowerbound:
                        if squirrels[i].alive:
                            if squirrels[i].speed[1] > 20 or squirrels[i].getPos()[0] < upperbound:
                                squirrels[i].die()
                                diedNum += 1
                            else:
                                squirrels[i].live()
                                safeNum += 1
                    if squirrels[i].getPos()[2] < leftbound or squirrels[i].getPos()[3] > width:
                        squirrels[i].bounce()
                    squirrels[i].timeBeforeDisappear -= 30
                    if squirrels[i].timeBeforeDisappear < 0 and squirrels[i].type == "SSquirrel":
                        safeNum += 1
        label = myfont.render(str(diedNum), 1, (0, 0, 0))
        screen.blit(label, (800, 100))
        pygame.display.flip()
        time += 30
        clock.tick(20)


def main2():
    squirrels = []
    for i in range(10):
        squirrels += [Squirrel()]
        
    squirrels[0].startTime = 0
    for i in range(1, 10):
        from random import randint
        squirrels[i].startTime = squirrels[i - 1].startTime + randint(700, 1000)

    background = pygame.image.load("background.psd")
    backgroundRect = background.get_rect()

    gameover = pygame.image.load("gameover.png")
    gameoverRect = gameover.get_rect()
    gameoverRect.move_ip(gameoverPoint)

    win = pygame.image.load("win.png")
    winRect = win.get_rect()
    winRect.move_ip(gameoverPoint)

    firstlevel = pygbutton.PygButton(None, 'Fisrt Level')
    secondlevel = pygbutton.PygButton(None, 'Second Level') 
    thirdlevel = pygbutton.PygButton(None, 'Third Level')
    fourthlevel = pygbutton.PygButton(None, 'Fourth Level')
    rect3 = pygame.Rect(900, 50, 100, 100)
    RestartButton = pygbutton.PygButton(rect3, 'Menu')

    a = [1, 1, 1, 1]
    time = 0
    safeNum = 0
    diedNum = 0
    tag = True
    myfont = pygame.font.SysFont("monospace", 60) 
    pygame.mixer.music.play(loops = 0, start = 0.0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            firstlevelEvent = firstlevel.handleEvent(event)
            secondlevelEvent = secondlevel.handleEvent(event)
            thirdlevelEvent = thirdlevel.handleEvent(event)
            fourthlevelEvent = fourthlevel.handleEvent(event)
            RestartEvent = RestartButton.handleEvent(event)
            for subEvents in RestartEvent:
                if subEvents == 'down':
                    menu()
                    return
            for subEvents in firstlevelEvent:
                if subEvents == 'down':
                    a[0] = -2.4
                elif subEvents == 'up':
                    a[0] = 1
                    tag = True
            for subEvents in secondlevelEvent:
                if subEvents == 'down':
                    a[1] = -2
                elif subEvents == 'up':
                    a[1] = 1
                    tag = True
            for subEvents in thirdlevelEvent:
                if subEvents == 'down':
                    a[2] = -1.6
                elif subEvents == 'up':
                    a[2] = 1
                    tag = True
            for subEvents in fourthlevelEvent:
                if subEvents == 'down':
                    a[3] = -1.2
                elif subEvents == 'up':
                    a[3] = 1
                    tag = True
        firstlevel.draw(screen)
        firstlevel._propGetRect().top = 230
        secondlevel.draw(screen)
        secondlevel._propGetRect().top = 230 + 117.5
        thirdlevel.draw(screen)
        thirdlevel._propGetRect().top = 230 + 117.5 * 2
        fourthlevel.draw(screen)
        fourthlevel._propGetRect().top = 230 + 117.5 * 3
        screen.blit(background, backgroundRect)
        RestartButton.draw(screen)
        if safeNum + diedNum == 10:
            if safeNum >= 5:
                screen.blit(win, winRect)
            else:
                screen.blit(gameover, gameoverRect)
        else:
            for i in range(10):
                if time >= squirrels[i].startTime and squirrels[i].timeBeforeDisappear >= 0:
                    screen.blit(squirrels[i].image, squirrels[i].rect)
                    if squirrels[i].alive:
                        h = squirrels[i].getPos()[0]
                        if h < 230:
                            squirrels[i].move(1)
                        else:
                            num = round((h - 230) / 117.5)
                            if num > 3:
                                num = 3
                            if a[num] < 0:
                                if squirrels[i].type == "SSquirrel" and tag:
                                    if squirrels[i].image == squirrels[i].thisimage:
                                        squirrels[i].flip()
                                    else:
                                        squirrels[i].die()
                                        diedNum += 1
                                    tag = False
                                else:
                                    squirrels[i].flip()
                            else:
                                if squirrels[i].type != "SSquirrel":
                                    squirrels[i].stay()
                            squirrels[i].move(a[num])
                    if squirrels[i].getPos()[0] < upperbound or squirrels[i].getPos()[1] > lowerbound:
                        if squirrels[i].alive:
                            if squirrels[i].speed[1] > 20 or squirrels[i].getPos()[0] < upperbound:
                                squirrels[i].die()
                                diedNum += 1
                            else:
                                squirrels[i].live()
                                safeNum += 1
                    if squirrels[i].getPos()[2] < leftbound or squirrels[i].getPos()[3] > width:
                        squirrels[i].bounce()
                    squirrels[i].timeBeforeDisappear -= 30
                    if squirrels[i].timeBeforeDisappear < 0 and squirrels[i].type == "SSquirrel":
                        safeNum += 1
        label = myfont.render(str(diedNum), 1, (0, 0, 0))
        screen.blit(label, (800, 100))
        pygame.display.flip()
        time += 30
        clock.tick(20)

if __name__ == '__main__': menu()
