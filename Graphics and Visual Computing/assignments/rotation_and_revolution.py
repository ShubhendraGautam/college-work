import pygame
import math

# Initialize Pygame
pygame.init()

# Colors
WHITE = (155, 195, 155)
BLACK = (35, 45, 43)

# Set up the display
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Triangles")

# Triangle vertices positioned in the center of the window
center_vertices = [
    [WIDTH//2 + 50, HEIGHT//2],
    [WIDTH//2 - 50, HEIGHT//2 + 50],
    [WIDTH//2 - 50, HEIGHT//2 - 50]
]

# Triangle vertices positioned to the left of the window
left_vertices = [
    [WIDTH//4 + 50, HEIGHT//2],
    [WIDTH//4 - 50, HEIGHT//2 + 50],
    [WIDTH//4 - 50, HEIGHT//2 - 50]
]

fixed_point = [WIDTH // 4, HEIGHT // 4]

def rotate_point(point, angle, center):
    """Rotate a point around a center by a given angle."""
    s, c = math.sin(angle), math.cos(angle)
    x, y = point
    x -= center[0]
    y -= center[1]
    new_x = x * c - y * s
    new_y = x * s + y * c
    return new_x + center[0], new_y + center[1]

def draw_triangle(vertices):
    """Function to draw a triangle."""
    pygame.draw.polygon(screen, BLACK, vertices)

def main():
    """Main loop to handle drawing and rotating the triangles."""
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Clear the screen
        screen.fill(WHITE)

        # Rotate the center triangle vertices about its centroid
        center = (WIDTH // 2, HEIGHT // 2)
        for i, vertex in enumerate(center_vertices):
            center_vertices[i] = list(rotate_point(vertex, math.radians(1), center))

        # Rotate the left triangle vertices about the fixed point
        for i, vertex in enumerate(left_vertices):
            left_vertices[i] = list(rotate_point(vertex, math.radians(1), fixed_point))

        # Draw both triangles
        draw_triangle(center_vertices)
        draw_triangle(left_vertices)

        # Draw the fixed point for the left triangle
        pygame.draw.circle(screen, (255, 0, 0), fixed_point, 5)

        # Update the display
        pygame.display.flip()
        clock.tick(60)

# Run the main loop
main()
