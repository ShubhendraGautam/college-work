import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import random

def draw_circle(x_center, y_center, radius, color):
    """ Draw a circle centered at (x_center, y_center) with the given radius and color """
    glBegin(GL_LINE_LOOP)
    glColor3fv(color)
    for i in range(100):
        theta = 2.0 * 3.1415926 * float(i) / 100.0
        x = radius * np.cos(theta) + x_center
        y = radius * np.sin(theta) + y_center
        glVertex2f(x, y)
    glEnd()

def draw_multiple_circles_through_points(x1, y1, x2, y2, num_circles, color):
    h = (x1 + x2) / 2
    k = (y1 + y2) / 2
    if x2 - x1 != 0:
        m = (y2 - y1) / (x2 - x1)
        m_perpendicular = -1 / m
    else:
        m_perpendicular = float('inf')
    
    for i in range(1, num_circles + 1):
        offset = i * 0.5
        if m_perpendicular != float('inf'):
            dx = offset / np.sqrt(1 + m_perpendicular ** 2)
            dy = m_perpendicular * dx
        else:
            dx = 0
            dy = offset
        
        center_x = h + dx
        center_y = k + dy
        radius = np.sqrt((x1 - center_x) ** 2 + (y1 - center_y) ** 2)
        draw_circle(center_x, center_y, radius+5, color)

def main_correct_aspect_ratio():
    pygame.init()
    display_width = 800
    display_height = 600
    aspect_ratio = display_width / display_height
    pygame.display.set_mode((display_width, display_height), DOUBLEBUF | OPENGL)
    
    left, right = -20, 20
    bottom = -20
    top = bottom + (right - left) / aspect_ratio
    gluOrtho2D(left, right, bottom, top)

    x1, y1 = -10, 8-16
    x2, y2 = -6, 12-16

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_multiple_circles_through_points(x1, y1, x2, y2, 7, (1, 0, 0))
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main_correct_aspect_ratio()
