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

planeImg = pygame.image.load('plane.png')
planeImg = pygame.transform.scale(planeImg,(100,160))

enemiesImg = pygame.image.load('Enemies/type_1.png')
enemiesImg = pygame.transform.scale(enemiesImg,(100,100))

Type2EnemiesImg = pygame.image.load('Enemies/type_2.png')
Type2EnemiesImg = pygame.transform.scale(Type2EnemiesImg,(100,100))

plane_width = 100
plane_height = 160

enemies_width = 100
enemies_height = 100

backgroundImg = pygame.image.load('background.png')
pause = False

#score
def enemies_dodged(count):
    font = pygame.font.SysFont('freesansbold.ttf', 25)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))

#lives
def lives_left(counter):
    font = pygame.font.SysFont('freesansbold.ttf', 25)
    text = font.render("Lives: "+str(counter), True, black)
    gameDisplay.blit(text,(100,0))


#create enemies
def enemies(x,y,type):
    #type corresponds to the number of enemies dodged
    if type <= 10:
        gameDisplay.blit(enemiesImg,(x,y))
        pygame.display.update()
    if type > 10:
        gameDisplay.blit(Type2EnemiesImg,(x,y))
        pygame.display.update()

#function to load plane
def plane(x,y):
    gameDisplay.blit(planeImg,(x,y))
    pygame.display.update()

def text_objects(text, font):
    textSurf = font.render(text,True, black)
    return textSurf, textSurf.get_rect()

#Game over
def game_over():
    largeText = pygame.font.Font('freesansbold.ttf',90)
    TextSurf, TextRect = text_objects("Game Over!", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("PLAY AGAIN", 90,450,130,50,green,bright_green,"play_again")
        button("QUIT", 550,450,100,50,red,bright_red,"quit")
        
        pygame.display.update()

#function to handle crash
def crash(life,dodged):
    if life <= 0:
        game_over()
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
                lives = 3
                dodged = 0

                game_loop(lives, dodged)
            if action == "quit":
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('Music/Button.wav'))
                pygame.time.delay(400)         
                pygame.quit()
                quit()
            
            #unpause game after clicking continue
            if action == "pause":
                unpause()

            #Restart game after game over
            if action == "play_again":
                game_loop(3,0)
    else:
        pygame.draw.rect(gameDisplay,ic,(x,y,w,h))
    
    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x + (w/2)), (y+(h/2)))
    gameDisplay.blit(textSurf,textRect)

#unPause
def unpause():
    global pause
    pause = False

#Pause
def paused():

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        gameDisplay.blit(backgroundImg,(0,0))
        largeText = pygame.font.Font('freesansbold.ttf',90)
        TextSurf, TextRect = text_objects("Paused", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("CONTINUE", 120,450,120,50,green,bright_green,"pause")
        button("QUIT", 550,450,100,50,red,bright_red,"quit")
        
        pygame.display.update()
        clock.tick(15)


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
    enemies_startx = random.randrange(0, display_width)
    enemies_starty = -600
    enemies_speed = 3
    enemies_width = 80
    enemies_height = 80
    backgroundX1 = 0
    backgroundY1 = 0
    backgroundX2 = 0
    backgroundY2 = -display_height
    global pause
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
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()

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

        #enemies(enemies_startx, enemies_starty, type)
        enemies(enemies_startx, enemies_starty,dodged)
        enemies_starty += enemies_speed
        
        #draw plane
        plane(x,y)
        enemies_dodged(dodged)
        lives_left(lives)

        if x > display_width - plane_width or x < 0 :
            lives -= 1
            crash(lives,dodged)

        if enemies_starty > display_height:
            enemies_starty = 0 - enemies_height
            enemies_startx = random.randrange(0,display_width)
            dodged += 1
            if dodged % 5 == 0:
                enemies_speed +=2


        if y < enemies_starty + enemies_height:
            #print('y crossover')

            if x > enemies_startx and x < enemies_startx + enemies_width or x + plane_width > enemies_startx and x + plane_width < enemies_startx + enemies_width:
                #print('x crossover')
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