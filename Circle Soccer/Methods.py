import pygame
from math import *
from Configuration import *
from Entities import *
def CheckCollision(circle1, circle2):
    x = abs(circle1.rect.centerx-circle2.rect.centerx)
    y = abs(circle1.rect.centery-circle2.rect.centery)
    hypotenuse = sqrt(x**2 + y**2)
    if (circle1.radius + circle2.radius -(circle1.velocity+circle2.velocity)) < hypotenuse <= (circle1.radius + circle2.radius +(circle1.velocity + circle2.velocity)):
        if hypotenuse < circle1.radius + circle2.radius:
            circle1.direction += pi
            circle2.direction += pi
            circle1.rect.centerx -= circle1.velocity*cos(circle1.direction)
            circle1.rect.centery -= circle1.velocity*sin(circle1.direction)
            circle2.rect.centerx -= circle2.velocity*cos(circle2.direction)
            circle2.rect.centery -= circle2.velocity*sin(circle2.direction)
        return True
    else:
        return False

def CircleCollision(circle1, circle2):
    #The Circle which is colliding with it. Check the angle of collision.


    if circle1.velocity > circle2.velocity:
        x_displacement = circle2.rect.centerx - circle1.rect.centerx
        y_displacement = circle2.rect.centery - circle1.rect.centery
        try:
            angle_of_collision = tan(x_displacement/y_displacement)
        except:
            angle_of_collision = 0

        if x_displacement > 0 and y_displacement > 0:
            angle_of_collision = abs(angle_of_collision)
        elif x_displacement < 0 and y_displacement > 0:
            angle_of_collision = pi - abs(angle_of_collision)
        elif x_displacement > 0 and y_displacement < 0:
            angle_of_collision = -abs(angle_of_collision)
        elif x_displacement < 0 and y_displacement < 0:
            angle_of_collision = pi + abs(angle_of_collision)
    

        circle2.velocity = circle1.velocity * 3/4
        circle1.velocity *= 1/4
        circle2.direction = angle_of_collision
        circle1.direction = angle_of_collision + pi
    elif circle1.velocity < circle2.velocity:
        x_displacement = circle1.rect.centerx - circle2.rect.centerx
        y_displacement = circle1.rect.centery - circle2.rect.centery
        try:
            angle_of_collision = tan(x_displacement/y_displacement)
        except:
            angle_of_collision = 0

        if x_displacement > 0 and y_displacement > 0:
            angle_of_collision = abs(angle_of_collision)
        elif x_displacement < 0 and y_displacement > 0:
            angle_of_collision = pi - abs(angle_of_collision)
        elif x_displacement > 0 and y_displacement < 0:
            angle_of_collision = -abs(angle_of_collision)
        elif x_displacement < 0 and y_displacement < 0:
            angle_of_collision = pi + abs(angle_of_collision)

        circle1.velocity = circle2.velocity * 3/4
        circle2.velocity *= 1/4
        circle1.direction = angle_of_collision
        circle2.direction = angle_of_collision + pi


    
    print(angle_of_collision)
    
def WallCollision(circle):
    centerx = circle.rect.centerx
    centery = circle.rect.centery
    left_wall = map.rect.left
    right_wall = map.rect.right
    top_wall = map.rect.top
    bottom_wall = map.rect.bottom
    #Checks if circle exceeds any of the walls in the game
    if ((centerx + circle.radius) >= right_wall or (centerx - circle.radius) <=left_wall) and ((centery + circle.radius) >= bottom_wall or (centery - circle.radius) <= top_wall):
        circle.direction -= pi
    elif (centerx + circle.radius) >= right_wall or (centerx - circle.radius) <=left_wall:
        circle.direction = pi-circle.direction
    elif (centery + circle.radius) >= bottom_wall or (centery - circle.radius) <= top_wall:
        circle.direction = -circle.direction
    
def MatchRunning( all_circles, MouseUP = False, MouseDOWN = False):
    deceleration = 0.99
    #Constantly Check all of collisions
    for i in range(len(all_circles)):
        for a in range(i+1, len(all_circles)):
            if CheckCollision(all_circles[i],all_circles[a]) == True:
                CircleCollision(all_circles[i],all_circles[a])


        WallCollision(all_circles[i])
        if all_circles[i].team == map.turn:
            if all_circles[i].Drag(MouseUP, MouseDOWN):
                if all_circles[i].team == 'Red':
                    map.turn = 'Blue'
                else:
                    map.turn = 'Red'

        #Universal Deceleration
        if all_circles[i].velocity > 0:
            all_circles[i].velocity *= deceleration
    map.DetectGoal(all_circles, ball)

    map.Draw()
    for i in all_circles:
        i.Draw()

    