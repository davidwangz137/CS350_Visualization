"""
Contains the logic for handling the different game events and animating them
"""

import pygame
clock = pygame.time.Clock()

# TODO: draw a number on each square to denote how may are there in that queue

# A list of the different directions
directions = ['N', 'E', 'S', 'W']

# Utility functions for finding the kind of turn it is
def right_turn(origin, dest):
    if origin+dest in ['NW', 'EN', 'SE', 'WS']:
        return True
    return False

def left_turn(origin, dest):
    if origin+dest in ['NE', 'ES', 'SW', 'WN']:
        return True
    return False

def straight(origin, dest):
    if origin+dest in ['NS', 'EW', 'SN', 'WE']:
        return True
    return False

# Draws a square with the corresponding center
# Rotate it according to the origin of the car
# S: 0 degrees
# E: 90 degrees
# N: 180 degrees
# W: 270 degrees

side_length = 24
def draw_square(center, origin, color, number, text):
    center[0] -= window_side_length/2
    center[1] -= window_side_length/2
    if origin == 'N':
        center = [-center[0], -center[1]]
    elif origin == 'E':
        center = [center[1], -center[0]]
    elif origin == 'S':
        center = [center[0], center[1]]
    elif origin == 'W':
        center = [-center[1], center[0]]
    else:
        raise Exception("Invalid origin: %s" % origin)
    center[0] += window_side_length/2
    center[1] += window_side_length/2
    pygame.draw.rect(screen, color, pygame.Rect(center[0]-side_length/2, center[1]-side_length/2, side_length, side_length))
    # Now draw the text
    if text:
        text = font.render("%d" % number, True, (255, 255, 255))
        screen.blit(text, (center[0] - text.get_width()/2, center[1] - text.get_height()/2))

# Spawn any now existing stacks
# Despawn any stacks that don't exist anymore
# Update the numbers on those that still do

base = 460
spacing = 50
def process_tile(k, v, y, base=base, text=True):
    if v == 0:
        return
    if right_turn(k[0], k[1]):
        draw_square([base + 2*spacing, y], k[0], (0, 255, 0), v, text)
    elif straight(k[0], k[1]):
        draw_square([base + spacing, y], k[0], (0, 128, 255), v, text)
    elif left_turn(k[0], k[1]):
        draw_square([base, y], k[0], (255, 100, 0), v, text)
    else:
        raise Exception("Not a valid turn: %s %s" %(k[0], k[1]))

wait_y = 670
inter_y = 560

# This simply updates the graphics
def update_graphics(wait, inter):
    # Clear the screen of all previous graphics
    screen.fill((0, 0, 0))

    for k, v in wait.iteritems():
        process_tile(k, v, wait_y)

    for k, v in inter.iteritems():
        process_tile(k, v, inter_y)

    # Draw the traffic boundaries
    color = (255, 255, 255)
    thickness = 20
    pygame.draw.rect(screen, color, pygame.Rect(0, base + 3*spacing, window_side_length, thickness))
    pygame.draw.rect(screen, color, pygame.Rect(0, window_side_length - (base + 3*spacing) - thickness, window_side_length, thickness))
    pygame.draw.rect(screen, color, pygame.Rect(base + 3*spacing, 0, thickness, window_side_length))
    pygame.draw.rect(screen, color, pygame.Rect(window_side_length - (base + 3*spacing) - thickness, 0, thickness, window_side_length))

    # Traffic lines on the side for decorations
    thickness = 10
    length = window_side_length - (base + 3*spacing) - thickness
    pygame.draw.rect(screen, color, pygame.Rect(0, window_side_length/2-thickness/2, length, thickness))
    pygame.draw.rect(screen, color, pygame.Rect(base + 3*spacing + thickness, window_side_length/2-thickness/2, length, thickness))
    pygame.draw.rect(screen, color, pygame.Rect(window_side_length/2-thickness/2, 0, thickness, length))
    pygame.draw.rect(screen, color, pygame.Rect(window_side_length/2-thickness/2, base + 3*spacing + thickness, thickness, length))

"""
Animation code
"""

step = 5  # The animation step size in pixels
# This animates from the wait queue to the inter queue
def road_to_wait(wait, inter, origin, dest):
    for i in range((window_side_length - wait_y)/step):
        update_graphics(wait, inter)
        process_tile((origin, dest), 1, window_side_length - i*step, base, False)
        pygame.display.flip()
        clock.tick(120)

# This animates from the wait queue to the inter queue
def wait_to_inter(wait, inter, origin, dest):
    for i in range((wait_y-inter_y)/step):
        update_graphics(wait, inter)
        process_tile((origin, dest), 1, wait_y-i*step, base, False)
        pygame.display.flip()
        clock.tick(120)

# This animates from the inter queue to the finish queue
def inter_to_fin(wait, inter, origin, dest):

    # Depending on the turn, do a different animation
    if right_turn(origin, dest):
        # Go to center of right lane
        center_right = 50
        for i in range(center_right/step):
            update_graphics(wait, inter)
            process_tile((origin, dest), 1, inter_y-i*step, base, False)
            pygame.display.flip()
            clock.tick(120)
        # Go into right lane
        for i in range((window_side_length-base-2*spacing)/step):
            update_graphics(wait, inter)
            process_tile((origin, dest), 1, inter_y-center_right, base+i*step, False)
            pygame.display.flip()
            clock.tick(120)

    elif straight(origin, dest):
        # Go straight
        for i in range(inter_y/step):
            update_graphics(wait, inter)
            process_tile((origin, dest), 1, inter_y-i*step, base, False)
            pygame.display.flip()
            clock.tick(120)
    elif left_turn(origin, dest):
        # Go to center of left lane
        center_left = 270
        for i in range(center_left/step):
            update_graphics(wait, inter)
            process_tile((origin, dest), 1, inter_y-i*step, base, False)
            pygame.display.flip()
            clock.tick(120)
        # Go into left lane
        for i in range(base/step):
            update_graphics(wait, inter)
            process_tile((origin, dest), 1, inter_y-center_left, base-i*step, False)
            pygame.display.flip()
            clock.tick(120)
    else:
        raise Exception("Not a valid turn: %s %s" %(origin, dest))

"""
Traffic Logic
"""

# Maintain queues for each direction to each direction for whether they are waiting or in the intersection itself
# Upon a change, also animate the change that occured
class TrafficState:
    def __init__(self):
        self.wait = {}
        self.inter = {}
        for d in directions:
            for d2 in directions:
                # No cars U-turn
                if d == d2:
                    continue
                self.wait[(d, d2)] = 0
                self.inter[(d, d2)] = 0

    def waiting(self, origin, dest, animate):

        # Do the animation. This will call update graphics, so we don't have to worry about the rest of the squares
        if animate:
            road_to_wait(self.wait, self.inter, origin, dest)

        # Need to update again for the number to show up
        self.wait[(origin, dest)] += 1
        update_graphics(self.wait, self.inter)

    def in_intersection(self, origin, dest, animate):

        # move a car to the intersection from the waiting section
        self.wait[(origin, dest)] -= 1

        # Do the animation. This will call update graphics, so we don't have to worry about the rest of the squares
        if animate:
            wait_to_inter(self.wait, self.inter, origin, dest)

        # Need to update again for the number to show up
        self.inter[(origin, dest)] += 1
        update_graphics(self.wait, self.inter)

    def leaving_intersection(self, origin, dest, animate):

        # The car moves from the intersection
        self.inter[(origin, dest)] -= 1

        # Do the animation. This will call update graphics, so we don't have to worry about the rest of the squares
        if animate:
            inter_to_fin(self.wait, self.inter, origin, dest)

        update_graphics(self.wait, self.inter)


# We initialize pygame here so we have access to the window parameters
window_side_length = 800
pygame.init()
screen = pygame.display.set_mode((window_side_length, window_side_length))
font = pygame.font.SysFont("comicsansms", 36)
