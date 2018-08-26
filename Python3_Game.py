import pygame
import time
import random

pygame.init()
display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
grey = (60,70,86)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

carImg = pygame.image.load('plane.png')
carImg = pygame.transform.scale(carImg,(100,160))
car_width = 100
car_height = 160

backgroundImg = pygame.image.load('background.png')


#score
def things_dodged(count):
    font = pygame.font.SysFont('freesansbold.ttf', 25)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))

#lives
def lives_left(counter):
    font = pygame.font.SysFont('freesansbold.ttf', 25)
    text = font.render("Lives: "+str(counter), True, black)
    gameDisplay.blit(text,(100,0))

#create obstacles
def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

#function to load car
def car(x,y):
    gameDisplay.blit(carImg,(x,y))
    pygame.display.update()

def text_objects(text, font):
    textSurf = font.render(text,True, black)
    return textSurf, textSurf.get_rect()

#function to handle crash
def crash(life,dodged):
    if life <= 0:
        message_display('GAME OVER')    
        game_intro()
    message_display('You Crashed!!!')
    game_loop(life,dodged)

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',110)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf,TextRect)

    pygame.display.update()

    time.sleep(2)

def button(msg, x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    pygame.mixer.music.load('Music/Button.wav')
    if x + w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            #button actions
            if action == "play":
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('Music/Button.wav'))
                pygame.time.delay(400) 
                #initialize game variables
                lives = 4
                dodged = 0

                game_loop(lives, dodged)
            elif action == "quit":
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('Music/Button.wav'))
                pygame.time.delay(400)         
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(gameDisplay,ic,(x,y,w,h))
    
    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x + (w/2)), (y+(h/2)))
    gameDisplay.blit(textSurf,textRect)

#Splash Screen
def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        #gameDisplay.fill(grey)
        gameDisplay.blit(backgroundImg,(0,0))
        largeText = pygame.font.Font('freesansbold.ttf',90)
        TextSurf, TextRect = text_objects("Save the World!!!", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("PLAY", 150,450,100,50,green,bright_green,"play")
        button("QUIT", 550,450,100,50,red,bright_red,"quit")
        
        pygame.display.update()
        clock.tick(15)

#Game Loop
def game_loop(lives, dodged):
    x = (display_width * 0.45)
    y = (display_height * 0.73)

    x_change = 0
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 3
    thing_width = 80
    thing_height = 80
    backgroundX1 = 0
    backgroundY1 = 0
    backgroundX2 = 0
    backgroundY2 = -display_height
    pygame.mixer.music.load('Music/Platformer2.wav')


    pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/Platformer2.wav'))
    
    gameExit = False

    while not gameExit:
        #event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                    x_change = 0

        x += x_change

        #moving background
        if backgroundY1 >= display_height:
            backgroundY1 = 0
        if backgroundY2 >= 0:
            backgroundY2 = -display_height
        gameDisplay.blit(backgroundImg,(backgroundX1,backgroundY1))
        gameDisplay.blit(backgroundImg,(backgroundX2,backgroundY2))

        #background speed
        backgroundY1 += 2
        backgroundY2 += 2

        #things(thingx, thingy, thingw, thingh, color)
        things(thing_startx, thing_starty, thing_width, thing_height, red)
        thing_starty += thing_speed
        car(x,y)
        things_dodged(dodged)
        lives_left(lives)

        if x > display_width - car_width or x < 0 :
            lives -= 1
            crash(lives,dodged)

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width)
            dodged += 1
            if dodged % 5 == 0:
                thing_speed +=2


        if y < thing_starty + thing_height:
            print('y crossover')

            if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:
                print('x crossover')
                lives -=1
                crash(lives,dodged)

        pygame.display.update()
        clock.tick(60)

#start music
#pygame.mixer.music.load('gameintro.mp3')
#pygame.mixer.music.play(-1)

#intro screen
game_intro()

pygame.quit()
quit()