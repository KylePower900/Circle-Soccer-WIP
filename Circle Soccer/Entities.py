import pygame
from Configuration import *
from math import * 
import random
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 100)

class Player:
    def __init__(self, radius, team, mass, coordinate, colour):
        self.radius = radius
        self.team = team
        self.mass = mass
        self.direction = 0
        self.rect = pygame.rect.Rect((0,0), (self.radius * 2, self.radius * 2))
        self.rect.center = coordinate
        self.starting_coordinate = coordinate
        self.velocity  = 0
        self.deceleration = 1
        self.drag = False
        self.colour = colour


    def Draw(self):
        if self.velocity > 0.01:
            self.rect.centerx += self.velocity*cos(self.direction)
            self.rect.centery += self.velocity*sin(self.direction)
        else:
            self.direction = 0
            self.velocity = 0
        if self.drag == True:
            pygame.draw.line(SCREEN, RED, pygame.mouse.get_pos(), self.rect.center, 5)

        
        pygame.draw.circle(SCREEN, self.colour, self.rect.center, self.radius)
    
    def Drag(self, MouseUP, MouseDOWN):
        mousepos = pygame.mouse.get_pos()

        if MouseUP == True:
                if self.drag == True:
                    self.drag = False
                
                    self.velocity = 0.03 * hypot(self.rect.centerx - mousepos[0],self.rect.centery - mousepos[1])
                    try:
                        self.direction = atan2(mousepos[1] - self.rect.centery, mousepos[0] - self.rect.centerx) + pi
                        if self.direction > 4 * pi:
                             print('hello')
                    except:
                         print("huh")
                    return True
        if MouseDOWN == True and self.rect.collidepoint(mousepos):
                    self.drag = True
           
class Ball(Player):
    def __init__(self, radius, team, mass, coordinate, colour):
        super().__init__(radius, team, mass, coordinate, colour)
    
    def Draw(self):
         return super().Draw()
    def Drag(self, MouseUP, MouseDOWN):
        return None

class Map:
    def __init__(self, dimensions, topleft, player_list):
        self.dimensions = pygame.surface.Surface(dimensions)
        self.rect = self.dimensions.get_rect()
        self.rect.topleft = topleft
        self.colour = (0,255,0)
        self.players = player_list
        self.score = [0,0]
        self.turn = ['Red', 'Blue'][random.randint(0,1)]

        self.goal1 = pygame.rect.Rect((self.rect.left + 5 , self.rect.centery-100), (5, 200))
        self.goal2 = pygame.rect.Rect((self.rect.right - 10, self.rect.centery-100), (5, 200))
    
    def AddPlayer(self, player):
        self.players.append(player)
        return True
    
    def RemovePlayer(self, player):
        try:
            self.players.remove(player)
            return True
        except:
            return False
        
    def DetectGoal(self, all_circles, ball):
        if self.goal1.colliderect(ball.rect):
            self.score[0] += 1
            for i in all_circles:
                i.velocity = 0
                i.rect.center = i.starting_coordinate
        if self.goal2.colliderect(ball.rect):
            self.score[1] += 1
            for i in all_circles:
                i.velocity = 0
                i.rect.center = i.starting_coordinate

    def Draw(self):
        pygame.draw.rect(SCREEN, (0,125,0), self.rect)
        pygame.draw.rect(SCREEN, self.colour, self.rect, width=10)
        pygame.draw.rect(SCREEN, (255,0,0), self.goal1)
        pygame.draw.rect(SCREEN, (255,0,0), self.goal2)
        text_surface = my_font.render(str(self.score[0]), False, (0, 0, 0))
        SCREEN.blit(text_surface, (self.rect.centerx - 100, self.rect.centery))
        text_surface = my_font.render(str(self.score[1]), False, (0, 0, 0))
        SCREEN.blit(text_surface, (self.rect.centerx + 40, self.rect.centery))
        text_surface = my_font.render(self.turn, False, (0, 0, 0))
        SCREEN.blit(text_surface, (self.rect.centerx - 100, self.rect.centery - 200))


map = Map((1840, 1000), (40,40),{})

blue_circle1 = Player(20, 'Blue', 1, (1740+map.rect.left,100+map.rect.top), BLUE)
blue_circle2 = Player(20, 'Blue', 1, (1640+map.rect.left,300+map.rect.top), BLUE)
blue_circle3 = Player(20, 'Blue', 1, (1540+map.rect.left,400+map.rect.top), BLUE)
blue_circle4 = Player(20, 'Blue', 1, (1340+map.rect.left,500+map.rect.top), BLUE)
blue_circle5 = Player(20, 'Blue', 1, (1540+map.rect.left,600+map.rect.top), BLUE)
blue_circle6 = Player(20, 'Blue', 1, (1640+map.rect.left,700+map.rect.top), BLUE)
blue_circle7 = Player(20, 'Blue', 1, (1740+map.rect.left,900+map.rect.top), BLUE)

red_circle1 = Player(20, 'Red', 1, (100+map.rect.left, 100+map.rect.top), RED)
red_circle2 = Player(20, 'Red', 1, (200+map.rect.left, 300+map.rect.top), RED)
red_circle3 = Player(20, 'Red', 1, (300+map.rect.left, 400+map.rect.top), RED)
red_circle4 = Player(20, 'Red', 1, (500+map.rect.left, 500+map.rect.top), RED)
red_circle5 = Player(20, 'Red', 1, (300+map.rect.left, 600+map.rect.top), RED)
red_circle6 = Player(20, 'Red', 1, (200+map.rect.left, 700+map.rect.top), RED)
red_circle7 = Player(20, 'Red', 1, (100+map.rect.left, 900+map.rect.top), RED)

ball = Ball(20, 'None', 1, (SCREEN_WIDTH/2,SCREEN_HEIGHT/2), BLACK)

list_of_circles = [blue_circle1, blue_circle2, blue_circle3, blue_circle4, blue_circle5, blue_circle6, blue_circle7, red_circle1, red_circle2, red_circle3,red_circle4, red_circle5, red_circle6, red_circle7, ball]

map.players = {
     'Red': len([i for i in list_of_circles if i.team == 'Red']),
     'Blue': len([i for i in list_of_circles if i.team == 'Blue']),
     'Players': len(list_of_circles)
}
