import pygame
import math
import random
import sys

# init pygame
pygame.init()

# screen
screen_width = 1000
screen_height = 800
surface = pygame.display.set_mode((screen_width,screen_height))

# colours
green = 0,255,0
red = 255,0,0
blue = 0,0,255
yellow = 255,255,0
white = 255,255,255
black = 0,0,0

# clock
clock = pygame.time.Clock()

# classes -------------------|
class Player:
    def __init__(self, colour, x, y, width, height, speed, max_health):
        self.rect = pygame.Rect(x,y,width,height)
        self.colour = colour
        self.direction = ''
        self.speed = speed

        self.max_health = max_health
        self.health = self.max_health

    def move(self):
        if self.direction == 'right':
            self.rect.x = self.rect.x+self.speed
        if self.direction == 'left':
            self.rect.x = self.rect.x-self.speed
        if self.direction == 'up':
            self.rect.y = self.rect.y-self.speed
        if self.direction == 'down':
            self.rect.y = self.rect.y+self.speed

    def moveDirection(self, direction):
        if direction == 'right':
            self.rect.x = self.rect.x+self.speed
        if direction == 'left':
            self.rect.x = self.rect.x-self.speed
        if direction == 'up':
            self.rect.y = self.rect.y-self.speed
        if direction == 'down':
            self.rect.y = self.rect.y+self.speed

    def collision(self, other_rect):
        #Return True if self collided with other_rect
        return self.rect.colliderect(other_rect)

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)


class Bullet(Player):
    def __init__(self, colour, x, y, width, height, speed, targetx,targety):
        super().__init__(colour, x, y, width, height, speed, max_health=100)
        angle = math.atan2(targety-y, targetx-x) 
        print('Angle in degrees:', int(angle*180/math.pi)) # angles in radians
        self.dx = math.cos(angle)*speed
        self.dy = math.sin(angle)*speed
        self.x = x
        self.y = y

    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.x = int(self.x) # converting back to integers to create rectangle
        self.rect.y = int(self.y)


class healthbar():
    def __init__(self, x, y, width, height, player):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.max_health = player.max_health
        self.health = player.health
    
    def draw(self,surface):
        print(self.health)
        ratio = self.health / self.max_health
        pygame.draw.rect(surface, red, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, green, (self.x, self.y, self.w * ratio, self.y))
        


#Build properties
p1 = Player(green,200,200,100,100, 10, 100)
hb = healthbar(50, 20, 150, 20, p1)


bullets = []
enemies = []

#Main program loop
def main():
    game_start = True
    game_over = False

    time = 0
    Small_font = pygame.font.SysFont(None, 40)
    message_start = Small_font.render("Game_Start : Click the SpaceBar", True, (255, 255, 255))

    while True:
        message_time = Small_font.render("time : %.2f s" %time, True, (255, 255, 255))
        if game_start == True:
            time += 0.035
        if game_over == True:
            game_start = False
        surface.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_start = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:#What happens when left mouse button his pressed
                print(True)

            elif event.type == pygame.KEYDOWN:
                print(event.key) #Print value of key press

                if event.key == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    #print(x,y)
                    b = Bullet(red, p1.rect.centerx, p1.rect.centery, 20,20, 20, x, y )
                    bullets.append(b)

                if event.key == pygame.K_d:
                    p1.moveDirection('right')

                if event.key == pygame.K_a:
                    p1.moveDirection('left')

                if event.key == pygame.K_w:
                    p1.moveDirection('up')

                if event.key == pygame.K_s:
                    p1.moveDirection('down')
        if game_start == False:
            surface.blit(message_start, (180, 350))
            surface.blit(message_time, (200, 430))
        
        else:
        #Update game objects
            for b in bullets:
                b.move()
            for e in enemies:
                e.move()
            # enemies spawn on the top of the screen and move down
            if random.randint(1,30) == 15: #15 doesn't matter
                x = random.randint(0,screen_width-40)
                e = Player(yellow, x,-40, 40,40, 10,100)
                e.direction = 'down'
                enemies.append(e)

            #Check for collisions
            for b in bullets:
                for e in enemies:
                    if b.collision(e.rect):
                        #e.colour = white #TESTING
                        enemies.remove(e)
                        bullets.remove(b)
            
            for e in enemies:
                p1.max_health = 100

                if p1.rect.colliderect(e.rect):
                    p1.health = p1.health - 10  # decrease player's health by 10
                    hb.health -= 10

                    if p1.health < 0:
                        p1.health = 0  # ensure health doesn't go below 0
                        
                        if p1.health == 0:
                            game_start == False
                            surface.blit(message_start, (180, 350))
                            surface.blit(message_time, (200, 430))
        
            
            #All the drawing
            for b in bullets:
                b.draw(surface)
            for e in enemies:
                e.draw(surface)
            p1.draw(surface)
            hb.draw(surface)
            pygame.display.update()
            clock.tick(60) #60 FPS

main()
pygame.quit()
exit()