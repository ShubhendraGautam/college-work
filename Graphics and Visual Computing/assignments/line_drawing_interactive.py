# import pygame
# from pygame.locals import *
# from OpenGL.GL import *
# from OpenGL.GLUT import *
# import numpy as np
# import math

# # Initialize pygame
# pygame.init()
# display = (800, 600)
# screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
# glOrtho(0, 800, 600, 0, -1, 1)  # Set the orthographic view

# # DDA line drawing algorithm with on-the-fly anti-aliasing
# def draw_line_dda(x0, y0, x1, y1):
#     dx = x1 - x0
#     dy = y1 - y0
#     steps = max(abs(dx), abs(dy))
#     x_inc = dx / steps
#     y_inc = dy / steps
#     x, y = x0, y0

#     for _ in range(steps):
#         apply_antialiasing_xiaolinwu(x, y)
#         x += x_inc
#         y += y_inc

# # Bresenham line drawing algorithm with on-the-fly anti-aliasing
# def draw_line_bresenham(x0, y0, x1, y1,anti_alias_choice):
#     dx = abs(x1 - x0)
#     dy = abs(y1 - y0)
    
#     sx = 1 if x0 < x1 else -1
#     sy = 1 if y0 < y1 else -1
#     if dx > dy:
#         dx, dy = dy, dx
#         exchange = True
#     else:
#         exchange = False
#     err = 2 * dy - dx
#     for _ in range(dx):
#         glColor3f(1, 1, 1)
#         glBegin(GL_POINTS)
#         glVertex2f(x0, y0)
#         glEnd()
#         if anti_alias_choice == 1:
#             apply_antialiasing_gaussian(x0,y0)
#         elif anti_alias_choice==2:
#             apply_antialiasing_conical(x0,y0)
#         elif anti_alias_choice==3:
#             apply_antialiasing_xiaolinwu(x0,y0)
#         else:
#             apply_gupta_sproull(x0,y0,err,dx,dy)
        
#         while err >= 0:
#             if exchange:
#                 x0 += sx
#             else:
#                 y0 += sy
#             err -= 2 * dx
#         if exchange:
#             y0 += sy
#         else:
#             x0 += sx
#         err += 2 * dy

# # Midpoint line drawing algorithm with on-the-fly anti-aliasing
# def draw_line_midpoint(x0, y0, x1, y1):
#     dx = x1 - x0
#     dy = y1 - y0
#     d = 2*dy - dx
#     incrE = 2*dy
#     incrNE = 2*(dy - dx)
#     x, y = x0, y0
#     apply_antialiasing_xiaolinwu(x, y)
#     while x < x1:
#         if d <= 0:
#             d += incrE
#             x += 1
#         else:
#             d += incrNE
#             x += 1
#             y += 1
#         apply_antialiasing_xiaolinwu(x, y)

# # Xiaolin Wu's anti-aliasing (simplified)
# def apply_antialiasing_xiaolinwu(x, y):
#     fractional_y = y - int(y)
    
#     # Plot the main point
#     glColor3f(1, 1 - fractional_y, 1 - fractional_y)
#     glBegin(GL_POINTS)
#     glVertex2f(int(x), int(y))
#     glEnd()
    
#     # Plot the next point with the inverse fraction (the blending part)
#     glColor3f(1, fractional_y, fractional_y)
#     glBegin(GL_POINTS)
#     glVertex2f(int(x), int(y)+1)
#     glEnd()


# def gaussian(x, sigma):
#     return (1.0 / (2 * math.pi * sigma**2)) * math.exp(-(x**2) / (2 * sigma**2))

# # Gaussian anti-aliasing
# def apply_antialiasing_gaussian(x, y, sigma=1.0):
#     offset_range = 2  # considering a 5x5 kernel for simplicity
#     for i in range(-offset_range, offset_range+1):
#         for j in range(-offset_range, offset_range+1):
#             weight = gaussian(i, sigma) * gaussian(j, sigma)
#             glColor3f(weight, weight, weight)
#             glBegin(GL_POINTS)
#             glVertex2f(x+i, y+j)
#             glEnd()


# # Conical (tent) filter
# def conical(distance, radius):
#     if distance <= radius:
#         return 1 - distance/radius
#     return 0

# # Conical anti-aliasing
# def apply_antialiasing_conical(x, y, radius=1.0):
#     offset_range = 2  # considering a 5x5 kernel for simplicity
#     for i in range(-offset_range, offset_range+1):
#         for j in range(-offset_range, offset_range+1):
#             d = math.sqrt(i**2 + j**2)
#             weight = conical(d, radius)
#             glColor3f(weight, weight, weight)
#             glBegin(GL_POINTS)
#             glVertex2f(x+i, y+j)
#             glEnd()


# # Apply Gupta-Sproull anti-aliasing on-the-fly
# def apply_gupta_sproull(x, y, err, dx, dy):
#     start_intensity = 0.5 - abs(err) / (max(dx, dy) * 0.5)
#     glColor3f(start_intensity, start_intensity, start_intensity)
#     glBegin(GL_POINTS)
#     glVertex2f(x, y)
#     glEnd()


# def main():
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

#     # Getting user's choices
#     print("Choose a line drawing algorithm:")
#     print("1. Bresenham ")
#     print("2. DDA ")
#     print("3. Midpoint ")
#     choice = int(input())

#     x0, y0 = map(int, input("Enter starting point (x y): ").split())
#     x1, y1 = map(int, input("Enter ending point (x y): ").split())

#     print("Choose anti-aliasing algorithm:")
#     print("1. Gaussian Filter ")
#     print("2. Conical Filter ")
#     print("3. Xiolin WU ")
#     print("4. Gupta Sproll")

#     anti_alias_choice = int(input())


#     if choice== 1:
#         draw_line_bresenham(x0,y0,x1,y1,anti_alias_choice)
#     elif choice == 2:
#         draw_line_dda(x0, y0, x1, y1)

#     pygame.display.flip()

#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#                 pygame.quit()

# if __name__ == "__main__":
#     main()


# import pygame
# from pygame.locals import *
# from OpenGL.GL import *
# from OpenGL.GLUT import *

# # Initialize pygame
# pygame.init()
# display = (800, 600)
# screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
# glOrtho(0, 800, 600, 0, -1, 1)  # Set the orthographic view
# glClearColor(0, 0, 0, 1)  # Set background color to black

# # Apply Gupta-Sproull anti-aliasing on-the-fly
# def apply_gupta_sproull(x, y):
#     glColor3f(1, 1, 1)  # Set color to white
#     glBegin(GL_POINTS)
#     glVertex2f(x, y)
#     glEnd()

# # Bresenham line drawing algorithm
# def draw_line_bresenham(x0, y0, x1, y1):
#     dx = abs(x1 - x0)
#     dy = abs(y1 - y0)
#     sx = 1 if x0 < x1 else -1
#     sy = 1 if y0 < y1 else -1
#     err = dx - dy

#     while True:
#         apply_gupta_sproull(x0, y0)
#         if x0 == x1 and y0 == y1:
#             break

#         e2 = 2 * err
#         if e2 > -dy:
#             err -= dy
#             x0 += sx
#         if e2 < dx:
#             err += dx
#             y0 += sy

# def main():
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

#     # Getting user's choices
#     print("Choose a line drawing algorithm:")
#     print("1. Bresenham with Gupta-Sproull anti-aliasing")
#     choice = int(input())

#     x0, y0 = map(int, input("Enter starting point (x y): ").split())
#     x1, y1 = map(int, input("Enter ending point (x y): ").split())

#     if choice == 1:
#         draw_line_bresenham(x0, y0, x1, y1)

#     pygame.display.flip()

#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#                 pygame.quit()

# if __name__ == "__main__":
#     main()



import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import math

# Initialize pygame
pygame.init()
display = (800, 600)
screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
glOrtho(0, 800, 600, 0, -1, 1)  # Set the orthographic view

# Basic plotting function
def plot_pixel(x, y, intensity=1.0):
    glColor3f(intensity, intensity, intensity)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

# Line Drawing Algorithms
def draw_line_bresenham(x0, y0, x1, y1, anti_aliasing_func=None):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        if anti_aliasing_func:
            anti_aliasing_func(x0, y0, err, dx, dy)
        else:
            plot_pixel(x0, y0)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

# ... [Add the DDA and Midpoint algorithms here]
# DDA line drawing algorithm
def draw_line_dda(x0, y0, x1, y1, anti_aliasing_func=None):
    dx = x1 - x0
    dy = y1 - y0
    steps = max(abs(dx), abs(dy))
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x0, y0

    for _ in range(int(steps)):
        if anti_aliasing_func:
            anti_aliasing_func(x, y, y - round(y), dx, dy)
        else:
            plot_pixel(round(x), round(y))
        x += x_inc
        y += y_inc

# Midpoint line drawing algorithm
def draw_line_midpoint(x0, y0, x1, y1, anti_aliasing_func=None):
    dx = x1 - x0
    dy = y1 - y0
    d = 2*dy - dx
    incrE = 2*dy
    incrNE = 2*(dy - dx)
    x, y = x0, y0

    plot_pixel(x, y)
    while x < x1:
        if d <= 0:
            d += incrE
            x += 1
        else:
            d += incrNE
            x += 1
            y += 1
        if anti_aliasing_func:
            anti_aliasing_func(x, y, d, dx, dy)
        else:
            plot_pixel(x, y)

# Anti-Aliasing Functions
def gupta_sproull(x, y, err, dx, dy):
    intensity = 0.7 + abs(err) / max(dx, dy) * 0.3  # Adjusted for better visibility
    plot_pixel(x, y, intensity)

def xiaolin_wu(x, y, err, dx, dy):
    def plot_pixel_with_intensity(x, y, intensity):
        glColor3f(intensity, intensity, intensity)
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()
        
    ipart = lambda x: int(x)
    fpart = lambda x: x - int(x)
    rfpart = lambda x: 1 - fpart(x)
    
    # In our case, we want to interpolate based on the error term.
    # The error term gives us a sense of how far the current y value 
    # is from the ideal y value.
    intensity_left = rfpart(err/max(dx, dy))
    intensity_right = fpart(err/max(dx, dy))
    
    plot_pixel_with_intensity(x, y, intensity_left)
    plot_pixel_with_intensity(x + 1, y, intensity_right)

def gaussian_filter(x, y, err, dx, dy, sigma=0.5):
    offset_range = 2  # considering a 5x5 kernel for simplicity
    for i in range(-offset_range, offset_range + 1):
        for j in range(-offset_range, offset_range + 1):
            d = math.sqrt(i**2 + j**2)
            weight = (1.0 / (2 * math.pi * sigma**2)) * math.exp(-(d**2) / (2 * sigma**2))
            plot_pixel(x + i, y + j, weight)

def conical_filter(x, y, err, dx, dy, radius=1.0):
    # Function to compute Euclidean distance
    def distance(x1, y1, x2, y2):
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

    # Compute the intensity at (x, y)
    intensity = max(0, 1 - distance(x, y, x, y) / radius)
    plot_pixel(x, y, intensity)

    # Check nearby pixels within the radius
    for i in range(-int(radius), int(radius) + 1):
        for j in range(-int(radius), int(radius) + 1):
            if i == 0 and j == 0:
                continue  # Skip center pixel, already plotted
            d = distance(x, y, x + i, y + j)
            if d <= radius:
                intensity = max(0, 1 - d / radius)
                plot_pixel(x + i, y + j, intensity)


def main():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    print("Choose a line drawing algorithm:")
    print("1. Bresenham")
    print("2. DDA")
    print("3. Midpoint")
    choice = int(input())

    print("Choose an anti-aliasing algorithm:")
    print("1. None")
    print("2. Gupta-Sproull")
    print("3. Xiaolin Wu")
    print("4. Gaussian Filter")
    print("5. Conical Filter")
    aa_choice = int(input())

    x0, y0 = map(int, input("Enter starting point (x y): ").split())
    x1, y1 = map(int, input("Enter ending point (x y): ").split())

    aa_func = None
    if aa_choice == 2:
        aa_func = gupta_sproull
    elif aa_choice == 3:
        aa_func = xiaolin_wu
    elif aa_choice == 4:
        aa_func = gaussian_filter
    elif aa_choice == 5:
        aa_func = conical_filter

    if choice == 1:
        draw_line_bresenham(x0, y0, x1, y1, aa_func)
    elif choice == 2:
        draw_line_dda(x0, y0, x1, y1, aa_func)
    elif choice == 3:
        draw_line_midpoint(x0, y0, x1, y1, aa_func)


    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

if __name__ == "__main__":
    main()
