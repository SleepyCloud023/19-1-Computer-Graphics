import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gCamAng = 0.
gCamHeight = 1.

# draw a cube of side 1, centered at the origin.
def drawUnitCube():
    glBegin(GL_QUADS)
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f( 0.5, 0.5, 0.5) 
                             
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f( 0.5,-0.5,-0.5) 
                             
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
                             
    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5)
 
    glVertex3f(-0.5, 0.5, 0.5) 
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5) 
    glVertex3f(-0.5,-0.5, 0.5) 
                             
    glVertex3f( 0.5, 0.5,-0.5) 
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glEnd()

def drawCubeArray():
    for i in range(5):
        for j in range(5):
            for k in range(5):
                glPushMatrix()
                glTranslatef(i,j,-k-1)
                glScalef(.5,.5,.5)
                drawUnitCube()
                glPopMatrix()

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()
def render():
    global gCamAng, gCamHeight
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    
    # draw polygons only with boundary edges
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )


    glMatrixMode(GL_PROJECTION)    
    glLoadIdentity()
    # test other parameter values
    # near plane: 10 units behind the camera
    # far plane: 10 units in front of the camera

    gluPerspective(45, 1, 1, 10)
    glRotatef(36.264,1,0,0)
    glRotatef(-45,0,1,0)
    glTranslatef(-3,-3,-3)
    
    glTranslatef(0,0,0)
    #gluLookAt(3,3,3, 0,0,0, 0,1,0)
    

    drawFrame()
    glColor3ub(255, 255, 255)

    #drawUnitCube()

    # test 
    drawCubeArray()

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1

def myOrtho(left, right, bottom, top, zNear, zFar):
    
    M = np.array([[2/(right-left),0,0,-(right+left)/(right-left)],
                  [0,2/(top-bottom),0,-(top+bottom)/(top-bottom)],
                  [0,0,2/(zNear-zFar),-(zNear+zFar)/(zNear-zFar)],
                  [0,0,0,1]])
    glMultMatrixf(M.T)

def myLookAt(eye, at, up): #eye, at up 1D numpy array of length 3
    up = up/np.sqrt(up@up)
    v_dir = at - eye
    u = np.cross(v_dir,up)
    u = u/np.sqrt(u@u)
    
    v = np.cross(u,v_dir)
    v = v/np.sqrt(v@v)
    
    w = np.cross(u,v)
    w = w/np.sqrt(w@w)
    
    M = np.array([np.append(u,0),
                 np.append(v,0),
                 np.append(w,0),
                 np.array([0,0,0,1])])
    M = M.T
    glMultMatrixf(M)
    glTranslatef(-eye[0], -eye[1], -eye[2])
    
def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,'2015004075-4-1', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
