import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

def draw_ellipse_with_rotation(x_center, y_center, a, b, color, angle_in_degrees):
    """ Draw an ellipse centered at (x_center, y_center) with radii a and b and rotated by angle_in_degrees """
    angle_in_radians = np.radians(angle_in_degrees)
    
    glBegin(GL_LINE_LOOP)
    glColor3fv(color)
    for i in range(100):  # number of segments
        theta = 2.0 * 3.1415926 * float(i) / 100.0
        x = a * np.cos(theta)
        y = b * np.sin(theta)
        
        # Apply rotation
        x_rotated = x * np.cos(angle_in_radians) - y * np.sin(angle_in_radians)
        y_rotated = x * np.sin(angle_in_radians) + y * np.cos(angle_in_radians)
        
        glVertex2f(x_center + x_rotated, y_center + y_rotated)
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluOrtho2D(0, display[0], display[1], 0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        x=20
        for i in range(11):
            draw_ellipse_with_rotation(400, 300, 300, 100, (1, 0, 0), 100+x)
            x=x+12  # Red ellipse rotated by 45 degrees
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
