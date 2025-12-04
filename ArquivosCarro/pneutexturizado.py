from OpenGL.GL import *
from OpenGL.GLU import *
import math
import config

# --- Cores ---
COLOR_TIRE = (0.15, 0.15, 0.15, 1.0)
COLOR_CHROME = (0.75, 0.75, 0.8, 1.0)
COLOR_HOLE_DARK = (0.05, 0.05, 0.05, 1.0)

def set_material(color, shiny=10):
    glColor4fv(color)
    if shiny > 80:
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    elif shiny > 0:
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.3, 0.3, 0.3, 1.0))
    else:
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0))
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, float(shiny))

def draw_smooth_shoulder(outer_radius, face_z, corner_r, is_front=True):
    slices = 32; stacks = 8
    center_r = outer_radius - corner_r
    center_z = face_z - corner_r if is_front else -face_z + corner_r
    z_dir = 1 if is_front else -1

    for i in range(slices):
        angle1 = 2 * math.pi * i / slices
        angle2 = 2 * math.pi * (i + 1) / slices
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(stacks + 1):
            arc = (math.pi / 2) * j / stacks
            lr = center_r + corner_r * math.cos(arc); lz = center_z + (corner_r * math.sin(arc) * z_dir)
            nx = math.cos(angle1) * math.cos(arc); ny = math.sin(angle1) * math.cos(arc); nz = math.sin(arc) * z_dir
            glNormal3f(nx, ny, nz); glVertex3f(lr * math.cos(angle1), lr * math.sin(angle1), lz)
            nx = math.cos(angle2) * math.cos(arc); ny = math.sin(angle2) * math.cos(arc)
            glNormal3f(nx, ny, nz); glVertex3f(lr * math.cos(angle2), lr * math.sin(angle2), lz)
        glEnd()

def draw_retro_rim_face(radius):
    q = gluNewQuadric()
    # Garante que textura está desligada para o metal
    glDisable(GL_TEXTURE_2D) 
    
    set_material(COLOR_CHROME, shiny=120); gluDisk(q, 0, radius, 32, 1)
    set_material(COLOR_HOLE_DARK, shiny=0)
    hole_dist = radius * 0.6; hole_sz = radius * 0.25
    for i in range(4):
        glPushMatrix(); glRotate(90 * i, 0, 0, 1); glTranslatef(hole_dist, 0, 0.002)
        gluDisk(q, 0, hole_sz, 16, 1)
        set_material(COLOR_CHROME, shiny=80); gluCylinder(q, hole_sz, hole_sz, 0.02, 16, 1)
        set_material(COLOR_HOLE_DARK, shiny=0); glPopMatrix()
    
    set_material(COLOR_CHROME, shiny=120)
    glPushMatrix(); glTranslatef(0, 0, 0.01); gluCylinder(q, radius*0.2, radius*0.12, radius*0.25, 16, 1) 
    glTranslatef(0, 0, 0.07); gluDisk(q, 0, radius*0.12, 16, 1); glPopMatrix()
    
    set_material(COLOR_HOLE_DARK, shiny=20)
    for i in range(4):
        glPushMatrix(); glRotate(90 * i + 45, 0, 0, 1); glTranslatef(radius * 0.5, 0, 0.005)
        gluCylinder(q, 0.015, 0.015, 0.01, 8, 1); glPopMatrix()
    gluDeleteQuadric(q)

def draw_f1_wheel(radius, width, slices=64, stacks=1):
    rim_outer_r = radius * 0.65; rim_inner_r = radius * 0.40; face_z = width / 2.0; corner_r = width * 0.12
    q = gluNewQuadric(); gluQuadricNormals(q, GLU_SMOOTH); gluQuadricTexture(q, GL_TRUE)

    glPushMatrix(); glRotatef(90, 0, 1, 0)
    
    # 1. BANDA DE RODAGEM (COM TEXTURA)
    if config.tire_tread_texture_id:
        glEnable(GL_TEXTURE_2D); glBindTexture(GL_TEXTURE_2D, config.tire_tread_texture_id)
        glColor3f(1, 1, 1); glMaterialfv(GL_FRONT, GL_SPECULAR, (0,0,0,1))
    else:
        glDisable(GL_TEXTURE_2D); set_material(COLOR_TIRE, shiny=20)

    glPushMatrix(); center_w = width - (2 * corner_r); glTranslatef(0, 0, -center_w/2) 
    gluCylinder(q, radius, radius, center_w, 64, 1); glPopMatrix()
    
    # --- CORREÇÃO DO ARO SUMIDO: DESLIGA TEXTURA AQUI ---
    glDisable(GL_TEXTURE_2D) 
    # ----------------------------------------------------

    # 2. Ombros
    set_material(COLOR_TIRE, shiny=30)
    draw_smooth_shoulder(radius, face_z, corner_r, is_front=True)
    draw_smooth_shoulder(radius, face_z, corner_r, is_front=False)

    # 3. LATERAIS
    sidewall_outer_r = radius - corner_r
    glPushMatrix(); glTranslatef(0, 0, face_z)
    if config.sidewall_texture_id:
        glEnable(GL_TEXTURE_2D); glBindTexture(GL_TEXTURE_2D, config.sidewall_texture_id); glColor3f(1, 1, 1)
        gluDisk(q, rim_outer_r, sidewall_outer_r, 64, 1); glDisable(GL_TEXTURE_2D)
    else:
        set_material(COLOR_TIRE, shiny=10); gluDisk(q, rim_outer_r, sidewall_outer_r, 64, 1)
    glPopMatrix()
    
    glPushMatrix(); glTranslatef(0, 0, -face_z); glRotatef(180, 1, 0, 0)
    set_material(COLOR_TIRE, shiny=10); gluDisk(q, rim_outer_r, sidewall_outer_r, 64, 1); glPopMatrix()

    # 4. ARO (Metal)
    glPushMatrix()
    set_material(COLOR_CHROME, shiny=120) 
    glTranslatef(0, 0, -width/2)
    gluCylinder(q, rim_outer_r, rim_outer_r, width, 64, 1)
    glPopMatrix()

    rim_depth = 0.05
    glPushMatrix(); glTranslatef(0, 0, face_z - rim_depth)
    gluCylinder(q, rim_inner_r, rim_outer_r, rim_depth, 64, 1) 
    # Desenha a face (textura já foi desligada no início da função auxiliar, mas garantimos)
    draw_retro_rim_face(rim_inner_r)
    glPopMatrix()

    glPushMatrix(); glTranslatef(0, 0, -face_z + 0.05); glRotatef(180, 1, 0, 0)
    set_material(COLOR_TIRE, shiny=5); gluDisk(q, 0, rim_outer_r, 32, 1); glPopMatrix()

    gluDeleteQuadric(q); glPopMatrix(); glColor3f(1, 1, 1)