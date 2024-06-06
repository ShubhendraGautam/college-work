from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

def dda_line(start, end):
    x1, y1, z1 = start
    x2, y2, z2 = end

    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    steps = int(max(abs(dx), abs(dy), abs(dz)) * 100)
    x_increment = dx / steps
    y_increment = dy / steps
    z_increment = dz / steps

    x, y, z = x1, y1, z1
    for _ in range(steps):
        glVertex3fv((x, y, z))
        x += x_increment
        y += y_increment
        z += z_increment
    glVertex3fv((x, y, z))

def draw_pyramid():
    vertices = [
        [0, 1, 0],  # Apex
        [-1, -1, 1], # Base vertices
        [1, -1, 1],
        [1, -1, -1],
        [-1, -1, -1],
    ]

    edges = [
        (0, 1), (0, 2), (0, 3), (0, 4), # Edges from apex to base
        (1, 2), (2, 3), (3, 4), (4, 1), # Base edges
    ]

    glBegin(GL_LINES)
    for edge in edges:
        dda_line(vertices[edge[0]], vertices[edge[1]])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, display[0] / display[1], 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_pyramid()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
