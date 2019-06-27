import glfw
from OpenGL.GL import *
import numpy as np



def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw coordinate
    glBegin(GL_LINES)
    glColor3ub(255,0,0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0,255,0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255,255,255)
    glVertex2fv( (T @ np.array([.0,.5,1.]) ) [:-1] )
    glVertex2fv( (T @ np.array([.0,.0,1.]) ) [:-1] )
    glVertex2fv( (T @ np.array([.5,.0,1.]) ) [:-1] )
    glEnd()
        

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480,480,"2015004075-2-1", None,None)
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
        Rotate = np.array([ [np.cos(t), -np.sin(t),0.],
                         [np.sin(t), np.cos(t),0.],
                          [0.,0.,1.] ])
        Trans = np.array([ [1.,0.,.5],
                         [0.,1.,0.],
                         [0.,0.,1.] ])
        Compose = Rotate @ Trans
        # Render here, e.g. using pyOpenGL
        render(Compose)
        

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
 
