import glfw
from OpenGL.GL import *
import numpy as np


T = GL_LINE_LOOP
def render(typ):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnate
    glBegin(typ)
    for i in range(12):
        x = np.cos(np.radians(30*i))
        y = np.sin(np.radians(30*i))
        glVertex2fv(np.array([x,y]))
    glEnd()
    
def key_callback(window, key, scancode, action, mods):
    global T

    if key==glfw.KEY_1:
        T = GL_POINTS
    if key==glfw.KEY_2:
        T = GL_LINES
    if key==glfw.KEY_3:
        T = GL_LINE_STRIP
    if key==glfw.KEY_4:
        T = GL_LINE_LOOP
    if key==glfw.KEY_5:
        T = GL_TRIANGLES
    if key==glfw.KEY_6:
        T = GL_TRIANGLE_STRIP
    if key==glfw.KEY_7:
        T = GL_TRIANGLE_FAN
    if key==glfw.KEY_8:
        T = GL_QUADS
    if key==glfw.KEY_9:
        T = GL_QUAD_STRIP
    if key==glfw.KEY_0:
        T = GL_POLYGON
        
def cursor_callback(window, xpos, ypos):
    print('mouse cursor moving: (%d, %d)'%(xpos, ypos))

def button_callback(window, button, action, mod):
    if button==glfw.MOUSE_BUTTON_LEFT:
        if action==glfw.PRESS:
            print('press left btn: (%d, %d)'%glfw.get_cursor_pos(window))
        elif action==glfw.RELEASE:
            print('release left btn: (%d, %d)'%glfw.get_cursor_pos(window))

def scroll_callback(window, xoffset, yoffset):
    print('mouse wheel scroll: %d, %d'%(xoffset, yoffset))

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480,480,"2015004075-2-1", None,None)
    if not window:
        glfw.terminate()
        return
    glfw.set_key_callback(window, key_callback)
    #glfw.set_cursor_pos_callback(window, cursor_callback)
    #glfw.set_mouse_button_callback(window, button_callback)
    #glfw.set_scroll_callback(window, scroll_callback)
    
    # Make the window's context current
    glfw.make_context_current(window)

    # set the number of screen refresh to wait before calling glfw.swap_buffer().
    # your monitor refresh rate is 60Hz, the while loop is repeated every 1/60 sec glfw.swap_interval(1)
    #glfw.swap_interval(1)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()
        # Render here, e.g. using pyOpenGL
        render(T)
        

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
 
