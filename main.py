import keyboard
import pygame
import random as rand
import math
import time as t

pygame.init()


# Constants
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))





# Base Functions

def m_rad(mx, my):
    # Returns the slope (my/mx) in radians.
    radians = 0
    if mx != 0:
        radians = math.atan(my/mx)
    else:
        radians = math.pi/2
    return radians

def magnitude(x, y):
    # Returns the magnitude of a vector
    return math.sqrt((x**2) + (y**2))



# Object / Movement Functions

def spawn_object(x, y):
    object = pygame.Surface((20, 20))
    object.fill('white')
    object_rect = object.get_rect()
    object_rect.update((x, y), (20, 20))
    object_position = [x, y]
    object_velocity = [0, 0]

    return [object, object_rect, object_position, object_velocity]


def move_object(object, delta_x=0, delta_y=0):
    # moves the object according to its velocity. delta_x and delta_y force move the object.

    object[2][0] += delta_x + object[3][0]
    object[2][1] += delta_y + object[3][1]

    object_width = object[1][2]
    object_height = object[1][3]

    object[1].update((object[2][0], object[2][1]), (object_width, object_height))


def add_force(object, x, y):
    # Adds the velocity (x, y) to the object's velocity.
    object[3][0] += x
    object[3][1] += y


def add_point_force(object, x, y, magnitude):
    # Adds a velocity to the object's velocity. This velocity is a vector that points
    # from the object to the point (x, y) with the given magnitude.


    radians = m_rad(x - object[2][0] , y - object[2][1])

    x_sign = math.copysign(1, x - object[2][0])
    delta_x = math.cos(radians) * magnitude * x_sign
    delta_y = math.sin(radians) * magnitude * x_sign

    object[3][0] += delta_x
    object[3][1] += delta_y


def bounce(object, mx, my, multiplier=1.0):
    # Changes the velocity of the object as if it were bouncing against a surface with a slope of 'my/mx'.
    # Multiplies the magnitude of the velocity with 'multiplier'.
    print('boing')
    mag = magnitude(object[3][0], object[3][1])
    print(mag)

    velocity_radians = m_rad(object[3][0], object[3][1])
    surface_radians = m_rad(mx, my)

    new_velocity_radians = (surface_radians - (velocity_radians - surface_radians)) - math.pi

    x_sign = math.copysign(1, object[3][0])

    delta_x = -1 * math.cos(new_velocity_radians) * multiplier * x_sign * mag
    delta_y = -1 * math.sin(new_velocity_radians) * multiplier * x_sign * mag

    print(magnitude(delta_x, delta_y) )

    object[3][0] = delta_x
    object[3][1] = delta_y









if __name__ == '__main__':



    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    blit_array = []
    all_objects = []

    for i in range(4):
        new_object = spawn_object(rand.randint(0, SCREEN_WIDTH), rand.randint(0, SCREEN_HEIGHT))
        all_objects.append(new_object)

    for object_i in all_objects:
        blit_array.append(object_i)


    timer = 0
    playing = True
    # ++++++++++++++++++++++++++++++++++++++++ GAME LOOP
    while playing:
        t.sleep(1/60)
        if keyboard.is_pressed('esc'):
            quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False



        # object physics


        for object_i in all_objects:  # gravity stuff
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                add_point_force(object_i, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 4)
            for object_ii in all_objects:
                add_point_force(object_i, object_ii[2][0], object_ii[2][1], 1)
                print('object grav stuff')



        for object_i in all_objects:
            # print('falling')
            border = SCREEN_HEIGHT-50
            if object_i[2][1] >= border:
                bounce(object_i, 1, 0, 0.9)

            if (timer >= 30) and (object_i[2][1] < border):
                add_force(object_i, 0, 1)


        for object_i in all_objects:
            move_object(object_i)

        # End Stuff

        timer += 1

        # Blitting
        screen.fill('black')
        for object_i in blit_array:
            screen.blit(object_i[0], object_i[1])
        pygame.display.flip()



