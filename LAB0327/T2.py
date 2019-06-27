import glfw
from OpenGL.GL import *
import numpy as np

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(120, 120, 120)
    glVertex2fv(T @ np.array([0.0,0.5]))
    glVertex2fv(T @ np.array([0.0,0.0]))
    glVertex2fv(T @ np.array([0.5,0.0]))
    glEnd()

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(640,480,"Hello World", None,None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    # set the number of screen refresh to wait before calling glfw.swap_buffer().
    # your monitor refresh rate is 60Hz, the while loop is repeated every 1/60 sec glfw.swap_interval(1)
    glfw.swap_interval(1)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()

        t = glfw.get_time()

        s = np.sin(t)
        H = np.array([[s,0.],
                      [0.,s]] )
        th = glfw.get_time()
        T = np.array([[np.cos(th), -np.sin(th)],
                      [np.sin(th), np.cos(th)]])
        # Render here, e.g. using pyOpenGL
        render(T)
        render(H)
        

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
 
