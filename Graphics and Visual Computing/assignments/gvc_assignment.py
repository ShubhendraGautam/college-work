import pygame
import math

def dda_line(surface, start, end):
    x1, y1 = start
    x2, y2 = end

    dx = x2 - x1
    dy = y2 - y1
    steps = round(max(abs(dx), abs(dy)))  # Convert to integer
    x_increment = dx / steps
    y_increment = dy / steps

    x, y = x1, y1
    for _ in range(steps):
        pygame.draw.circle(surface, (255, 255, 255), (int(x), int(y)), 1)
        x += x_increment
        y += y_increment

def draw_triangle(surface, x, y, size, overlap_distance, count):
    top_vertex = (x, y)
    left_vertex = (x - size / 2, y + size * math.sqrt(3) / 2)
    right_vertex = (x + size / 2, y + size * math.sqrt(3) / 2)

    dda_line(surface, top_vertex, left_vertex)
    dda_line(surface, left_vertex, right_vertex)
    dda_line(surface, right_vertex, top_vertex)

    if count > 0:
        # Increase y by overlap_distance for each additional triangle
        draw_triangle(surface, x, y + overlap_distance, size, overlap_distance, count - 1)

import math

def rotate_point(x, y, angle, cx, cy):
    angle_rad = math.radians(angle)
    x_rot = cx + (x - cx) * math.cos(angle_rad) - (y - cy) * math.sin(angle_rad)
    y_rot = cy + (x - cx) * math.sin(angle_rad) + (y - cy) * math.cos(angle_rad)
    return x_rot, y_rot

def draw_triangle_downward(surface, x, y, size, overlap_distance, count):
    # Original vertices
    top_vertex = (x, y)
    left_vertex = (x - size / 2, y + size * math.sqrt(3) / 2)
    right_vertex = (x + size / 2, y + size * math.sqrt(3) / 2)

    # Rotate vertices by 180 degrees around the center (x, y)
    top_vertex = rotate_point(*top_vertex, 180, x, y)
    left_vertex = rotate_point(*left_vertex, 180, x, y)
    right_vertex = rotate_point(*right_vertex, 180, x, y)

    # Draw lines between rotated vertices
    dda_line(surface, top_vertex, left_vertex)
    dda_line(surface, left_vertex, right_vertex)
    dda_line(surface, right_vertex, top_vertex)

    if count > 0:
        # Recursively draw the next triangle, with the same size but shifted by the overlap distance
        new_y = y + overlap_distance
        draw_triangle_downward(surface, x, new_y, size, overlap_distance, count - 1)

# ... rest of the code ...

# ... rest of the code ...



def main():
    pygame.init()
    display = (800, 600)
    screen = pygame.display.set_mode(display)
    pygame.display.set_caption('Overlapping Triangles')

    running = True
    overlap_distance = 50  # Adjust the overlapping distance here
    count = 3  # Adjust the number of overlapping triangles here
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        draw_triangle(screen, 400, 100, 300, overlap_distance, count)
        draw_triangle_downward(screen, 400, 400, 300, overlap_distance, count)
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
