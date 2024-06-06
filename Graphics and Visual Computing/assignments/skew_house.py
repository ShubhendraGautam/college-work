
import glfw
from OpenGL.GL import *
import numpy as np

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

def draw_sheared_hut():
    glBegin(GL_QUADS)  # Draw the sheared base of the hut
    glVertex2f(-0.3, -0.3)
    glVertex2f(0.3, -0.3)
    glVertex2f(0.3, 0.0)
    glVertex2f(-0.3, 0.0)
    glEnd()

    glBegin(GL_TRIANGLES)  # Draw the sheared roof of the hut
    glVertex2f(-0.4, 0.0)
    glVertex2f(0.4, 0.0)
    glVertex2f(0.0, 0.3)
    glEnd()

def apply_shearing(matrix):
    glPushMatrix()
    glMultMatrixf(matrix.T)
    draw_sheared_hut()
    glPopMatrix()

def main():
    # Initialize GLFW
    if not glfw.init():
        return
    
    # Create a window
    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "OpenGL Hut Shearing", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    
    # Set up OpenGL
    glClearColor(0.0, 0.0, 0.0, 1.0)
    
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        
        # Apply shearing in y direction to draw the sheared hut
        shearing_matrix = np.array([
            [1.0, 0.5, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
        apply_shearing(shearing_matrix)
        
        # Swap buffers and poll events
        glfw.swap_buffers(window)
        glfw.poll_events()

    # Terminate GLFW
    glfw.terminate()

if __name__ == "__main__":
    main()