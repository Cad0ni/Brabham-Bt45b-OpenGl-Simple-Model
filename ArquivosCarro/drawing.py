from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
import config 

# ============================================================================
# 1. FORMAS PRIMITIVAS E AUXILIARES
# ============================================================================

def draw_cuboid(width, height, depth):
    """ Desenha um cuboide centrado na origem. """
    w, h, d = width/2, height/2, depth/2
    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1);  glVertex3f(-w, -h, d);  glVertex3f(w, -h, d);   glVertex3f(w, h, d);   glVertex3f(-w, h, d)
    glNormal3f(0, 0, -1); glVertex3f(-w, -h, -d); glVertex3f(-w, h, -d);  glVertex3f(w, h, -d);  glVertex3f(w, -h, -d)
    glNormal3f(-1, 0, 0); glVertex3f(-w, -h, d);  glVertex3f(-w, h, d);   glVertex3f(-w, h, -d); glVertex3f(-w, -h, -d)
    glNormal3f(1, 0, 0);  glVertex3f(w, -h, d);   glVertex3f(w, -h, -d);  glVertex3f(w, h, -d);  glVertex3f(w, h, d)
    glNormal3f(0, 1, 0);  glVertex3f(-w, h, d);   glVertex3f(w, h, d);    glVertex3f(w, h, -d);  glVertex3f(-w, h, -d)
    glNormal3f(0, -1, 0); glVertex3f(-w, -h, d);  glVertex3f(-w, -h, -d); glVertex3f(w, -h, -d); glVertex3f(w, -h, d)
    glEnd()

def draw_cylinder(radius, height, slices=32):
    """ Desenha um cilindro fechado com tampas. """
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluCylinder(quadric, radius, radius, height, slices, 1)
    glPushMatrix(); glRotatef(180, 0, 1, 0); gluDisk(quadric, 0, radius, slices, 1); glPopMatrix()
    glPushMatrix(); glTranslatef(0, 0, height); gluDisk(quadric, 0, radius, slices, 1); glPopMatrix()
    gluDeleteQuadric(quadric)

def draw_trapezoidal_prism():
    """ Desenha o prisma trapezoidal usado no chassi do carro. """
    v = [
        [-0.3, -0.5,  0.5], [ 0.3, -0.5,  0.5], [ 0.15,  0.2,  0.2], [-0.15,  0.2,  0.2],
        [-0.7, -0.7, -0.5], [ 0.7, -0.7, -0.5], [ 0.3,  0.5, -0.5], [-0.3,  0.5, -0.5]
    ]
    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1);  glVertex3fv(v[0]); glVertex3fv(v[1]); glVertex3fv(v[2]); glVertex3fv(v[3])
    glNormal3f(0, 0, -1); glVertex3fv(v[4]); glVertex3fv(v[5]); glVertex3fv(v[6]); glVertex3fv(v[7])
    glNormal3f(0, -1, 0); glVertex3fv(v[0]); glVertex3fv(v[1]); glVertex3fv(v[5]); glVertex3fv(v[4])
    glNormal3f(0, 1, 0);  glVertex3fv(v[3]); glVertex3fv(v[2]); glVertex3fv(v[6]); glVertex3fv(v[7])
    glNormal3f(-1, 0, 0); glVertex3fv(v[0]); glVertex3fv(v[3]); glVertex3fv(v[7]); glVertex3fv(v[4])
    glNormal3f(1, 0, 0);  glVertex3fv(v[1]); glVertex3fv(v[2]); glVertex3fv(v[6]); glVertex3fv(v[5])
    glEnd()

def draw_sphere(radius, slices=32, stacks=32):
    quadric = gluNewQuadric(); gluQuadricNormals(quadric, GLU_SMOOTH)
    gluSphere(quadric, radius, slices, stacks); gluDeleteQuadric(quadric)

def draw_cloud(x, y, z, scale=1.0):
    """ Desenha uma nuvem fofinha usando esferas sobrepostas. """
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(scale, scale, scale)
    
    # Cor da nuvem (Branco levemente cinza)
    # Usamos Material para reagir à luz do sol/lua
    glColor3f(0.9, 0.9, 0.95)
    
    # 3 Esferas juntas para formar a nuvem
    # Centro
    glPushMatrix(); glScalef(1.5, 1.0, 1.0); draw_sphere(3.0, 12, 12); glPopMatrix()
    # Esquerda
    glPushMatrix(); glTranslatef(-2.5, -0.5, 0); draw_sphere(2.0, 12, 12); glPopMatrix()
    # Direita
    glPushMatrix(); glTranslatef(2.5, -0.8, 0.5); draw_sphere(2.2, 12, 12); glPopMatrix()
    # Cima
    glPushMatrix(); glTranslatef(0.5, 2.0, -0.5); draw_sphere(1.8, 12, 12); glPopMatrix()
    
    glPopMatrix()

# ============================================================================
# 2. OBJETOS COM TEXTURA
# ============================================================================

def draw_ground():
    """ Chão infinito com textura de grama. """
    size = 1000.0; repeats = 600.0 
    glEnable(GL_TEXTURE_2D)
    if config.grass_texture_id:
        glBindTexture(GL_TEXTURE_2D, config.grass_texture_id); glColor3f(1.0, 1.0, 1.0) 
    else:
        glDisable(GL_TEXTURE_2D); glColor3f(0.0, 0.8, 0.0)

    glBegin(GL_QUADS); glNormal3f(0, 1, 0)
    glTexCoord2f(0.0, 0.0);         glVertex3f(-size, 0, -size)
    glTexCoord2f(0.0, repeats);     glVertex3f(-size, 0, size)
    glTexCoord2f(repeats, repeats); glVertex3f(size, 0, size)
    glTexCoord2f(repeats, 0.0);     glVertex3f(size, 0, -size)
    glEnd()
    glDisable(GL_TEXTURE_2D)

def draw_tree(x, z):
    """ Árvore com copa texturizada e repetição de textura (tiling). """
    glPushMatrix()
    glTranslatef(x, 0, z)
    
    # 1. Tronco
    glDisable(GL_TEXTURE_2D)
    glColor3f(0.4, 0.25, 0.1)
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    draw_cylinder(0.5, 3.0, 8)
    glPopMatrix()
    
    # 2. Copa (Folhas)
    glTranslatef(0, 3.0, 0)
    glEnable(GL_TEXTURE_2D)
    if config.leaves_texture_id:
        glBindTexture(GL_TEXTURE_2D, config.leaves_texture_id)
        glColor3f(1.0, 1.0, 1.0)
    else:
        glDisable(GL_TEXTURE_2D); glColor3f(0.0, 0.8, 0.0)

    # --- AQUI ESTÁ O SEGREDO PARA REPETIR A TEXTURA ---
    # Mudamos o modo para editar a "Matriz de Textura"
    glMatrixMode(GL_TEXTURE)
    glLoadIdentity()
    # glScalef(3.0, 3.0, 1.0) -> Repete a imagem 3x na Horizontal e 3x na Vertical
    glScalef(8.0, 8.0, 1.0) 
    glMatrixMode(GL_MODELVIEW) # Volta para o modo de desenho normal
    # --------------------------------------------------

    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE) 
    gluSphere(quad, 2.5, 16, 16)
    gluDeleteQuadric(quad)
    
    # --- RESET OBRIGATÓRIO (Senão estraga o chão e a pista) ---
    glMatrixMode(GL_TEXTURE)
    glLoadIdentity() # Reseta para 1x1
    glMatrixMode(GL_MODELVIEW)
    # ----------------------------------------------------------
    
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

def draw_tire_wall_arc(radius, start_angle, end_angle):
    """ Barreira de pneus com cores CINZA ESCURO. """
    if config.tire_tread_texture_id:
        glEnable(GL_TEXTURE_2D); glBindTexture(GL_TEXTURE_2D, config.tire_tread_texture_id)
        glMaterialfv(GL_FRONT, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0))
    else: glDisable(GL_TEXTURE_2D)
    
    steps = int(abs(end_angle - start_angle) / 4.0); steps = 1 if steps == 0 else steps
    step_val = (end_angle - start_angle) / steps
    
    tire_radius, tire_height, stack_height = 0.6, 0.5, 3
    quadric = gluNewQuadric(); gluQuadricNormals(quadric, GLU_SMOOTH); gluQuadricTexture(quadric, GL_TRUE) 

    for i in range(steps + 1):
        deg = start_angle + (i * step_val); rad = math.radians(deg)
        x = radius * math.cos(rad); z = radius * math.sin(rad)
        
        # --- ALTERAÇÃO DE COR (CINZA ESCURO / BRANCO) ---
        if i % 2 == 0: glColor3f(0.3, 0.3, 0.3) # Cinza Escuro
        else: glColor3f(0.9, 0.9, 0.9)          # Branco/Cinza Claro
        
        for h in range(stack_height):
            glPushMatrix(); glTranslatef(x, (h * tire_height), z); glRotatef(-90, 1, 0, 0) 
            gluCylinder(quadric, tire_radius, tire_radius, tire_height, 12, 1)
            glDisable(GL_TEXTURE_2D) # Tampas sem textura
            gluDisk(quadric, 0, tire_radius, 12, 1); glTranslatef(0, 0, tire_height); gluDisk(quadric, 0, tire_radius, 12, 1)
            if config.tire_tread_texture_id: glEnable(GL_TEXTURE_2D)
            glPopMatrix()
    
    gluDeleteQuadric(quadric); glDisable(GL_TEXTURE_2D)

# ============================================================================
# 3. OBJETOS DE PISTA
# ============================================================================

def draw_obstacle_cone(base_radius, height, slices=16):
    glColor3f(1.0, 0.4, 0.0); quadric = gluNewQuadric(); gluQuadricNormals(quadric, GLU_SMOOTH)
    gluCylinder(quadric, base_radius, 0, height, slices, 1); gluDisk(quadric, 0, base_radius, slices, 1); gluDeleteQuadric(quadric)

def draw_lamppost():
    """ 
    Desenha um poste de luz. 
    Se for noite, acende a lâmpada e projeta um feixe inclinado para a pista.
    """
    # 1. Estrutura do Poste
    glColor3f(0.2, 0.2, 0.2); glPushMatrix(); glTranslatef(0, 0.15, 0); glScalef(0.3, 0.3, 0.3); draw_cuboid(1, 1, 1); glPopMatrix()
    glColor3f(0.25, 0.25, 0.25); glPushMatrix(); glTranslatef(0, 4.0, 0); glScalef(0.1, 8.0, 0.1); draw_cuboid(1, 1, 1); glPopMatrix()
    glPushMatrix(); glTranslatef(0.5, 7.8, 0); glScalef(1.0, 0.1, 0.1); draw_cuboid(1, 1, 1); glPopMatrix()

    # Posição da lâmpada no alto
    lamp_pos = (1.0, 7.7, 0)
    
    is_night = not config.is_day 

    # 2. Lâmpada (Emissão)
    if is_night:
        light_color = (1.0, 1.0, 0.8)
        glMaterialfv(GL_FRONT, GL_EMISSION, (1.0, 1.0, 0.8, 1.0)) 
        glColor3fv(light_color)
    else:
        glMaterialfv(GL_FRONT, GL_EMISSION, (0.0, 0.0, 0.0, 1.0))
        glColor3f(0.9, 0.9, 0.9)

    glPushMatrix(); glTranslatef(lamp_pos[0], lamp_pos[1], lamp_pos[2]); draw_sphere(0.25, 16, 16); glPopMatrix()

    # 3. FEIXE DE LUZ VOLUMÉTRICO (Inclinado)
    if is_night:
        glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE); glDepthMask(GL_FALSE); glDisable(GL_LIGHTING)

        # --- CÁLCULO DA INCLINAÇÃO ---
        # Onde a luz bate no chão.
        # ground_y: Altura do chão (logo acima da pista)
        ground_y = 0.1 
        # target_dist: Quão longe do poste o centro da luz vai bater (projecão)
        target_dist = 5.0 
        # O centro do círculo no chão é deslocado no X local em relação à lâmpada
        target_x = lamp_pos[0] + target_dist
        target_z = lamp_pos[2]

        cone_radius = 6.0 # Raio do círculo de luz no chão

        glBegin(GL_TRIANGLE_FAN)
        # Vértice 1: Ponta do cone (na lâmpada) - Mais opaco
        glColor4f(1.0, 1.0, 0.8, 0.2) 
        glVertex3f(lamp_pos[0], lamp_pos[1], lamp_pos[2])
        
        # Vértices da Base: Círculo no chão (deslocado) - Transparente
        glColor4f(1.0, 1.0, 0.8, 0.0) 
        for i in range(0, 361, 20): # 20 graus para ficar mais suave
            rad = math.radians(i)
            # O círculo é desenhado em torno do target_x, target_z
            cx = target_x + math.cos(rad) * cone_radius
            cz = target_z + math.sin(rad) * cone_radius
            glVertex3f(cx, ground_y, cz)
        glEnd()

        glEnable(GL_LIGHTING); glDepthMask(GL_TRUE); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA); glDisable(GL_BLEND)

    glMaterialfv(GL_FRONT, GL_EMISSION, (0.0, 0.0, 0.0, 1.0))

def draw_grandstand(length, rows=15, width_per_seat=0.8, height_per_seat=0.5):
    total_depth = rows * width_per_seat; total_height = rows * height_per_seat
    glPushMatrix(); glTranslatef(-length/2, 0, 0)
    for i in range(rows):
        y = i * height_per_seat; z = i * width_per_seat
        if i % 2 == 0: glColor3f(0.8, 0.1, 0.1)
        else: glColor3f(0.9, 0.9, 0.9)
        glBegin(GL_QUADS); glNormal3f(0, 1, 0); glVertex3f(0, y+height_per_seat, z); glVertex3f(length, y+height_per_seat, z); glVertex3f(length, y+height_per_seat, z+width_per_seat); glVertex3f(0, y+height_per_seat, z+width_per_seat); glEnd()
        glColor3f(0.5, 0.5, 0.5); glBegin(GL_QUADS); glNormal3f(0, 0, 1); glVertex3f(0, y, z+width_per_seat); glVertex3f(length, y, z+width_per_seat); glVertex3f(length, y+height_per_seat, z+width_per_seat); glVertex3f(0, y+height_per_seat, z+width_per_seat); glEnd()
    glPopMatrix()
    glColor3f(0.4, 0.4, 0.4); glPushMatrix(); glTranslatef(0, total_height/2, total_depth); glScalef(length, total_height, 0.2); draw_cuboid(1, 1, 1); glPopMatrix()
    roof_h = total_height + 4.0; roof_d = total_depth + 2.0; glColor3f(0.9, 0.9, 0.95); glPushMatrix(); glTranslatef(0, roof_h, total_depth/2 - 1.0); glScalef(length + 1.0, 0.2, roof_d + 2.0); draw_cuboid(1, 1, 1); glPopMatrix()
    num_pillars = int(length / 10) + 1; glColor3f(0.3, 0.3, 0.3)
    for i in range(num_pillars):
        x_pos = -length/2 + (i * (length / (num_pillars-1)))
        glPushMatrix(); glTranslatef(x_pos, 0, total_depth - 0.5); glRotatef(-90, 1, 0, 0); draw_cylinder(0.3, roof_h, 8); glPopMatrix()

def draw_safety_fence(length, height=2.5):
    glDisable(GL_TEXTURE_2D); base_h = 0.8
    glColor3f(0.6, 0.6, 0.65); glPushMatrix(); glTranslatef(0, base_h/2, 0); glScalef(0.3, base_h, length); draw_cuboid(1, 1, 1); glPopMatrix()
    pole_dist = 4.0; num_poles = int(length / pole_dist); pole_h = height - base_h; glColor3f(0.4, 0.4, 0.45)
    for i in range(num_poles + 1):
        z_pos = -length/2 + (i * pole_dist); glPushMatrix(); glTranslatef(0, base_h + pole_h/2, z_pos); glScalef(0.1, pole_h, 0.1); draw_cuboid(1, 1, 1); glPopMatrix()
    num_wires = 5; wire_spacing = pole_h / (num_wires + 1); glColor3f(0.85, 0.85, 0.85)
    for i in range(num_wires):
        glPushMatrix(); glTranslatef(0, base_h + ((i + 1) * wire_spacing), 0); glScalef(0.05, 0.02, length); draw_cuboid(1, 1, 1); glPopMatrix()

def draw_traffic_light(x, z, angle=0):
    glPushMatrix(); glTranslatef(x, 0, z); glRotatef(angle, 0, 1, 0)
    glColor3f(0.05, 0.05, 0.05); glPushMatrix(); glScalef(0.5, 1.6, 0.4); draw_cuboid(1, 1, 1); glPopMatrix()
    r_on = y_on = g_on = False
    if config.animation_active:
        t = config.start_timer
        if t < 1.0: r_on = True
        elif t < 2.0: r_on = True; y_on = True
        else: g_on = True
    else: r_on = True
    def draw_lamp(y_off, color_on, color_off, is_on):
        col = color_on if is_on else color_off; emit = color_on + (1.0,) if is_on else (0,0,0,1)
        glColor3fv(col); glMaterialfv(GL_FRONT, GL_EMISSION, emit); glPushMatrix(); glTranslatef(0, y_off, 0.22); draw_sphere(0.18, 16, 16); glPopMatrix()
    draw_lamp(0.5, (1,0,0), (0.2,0,0), r_on); draw_lamp(0.0, (1,0.8,0), (0.2,0.15,0), y_on); draw_lamp(-0.5, (0,1,0), (0,0.2,0), g_on)
    glMaterialfv(GL_FRONT, GL_EMISSION, (0,0,0,1)); glPopMatrix()

def draw_starting_gantry(x, z, angle=0):
    glPushMatrix(); glTranslatef(x, 0, z); glRotatef(angle, 0, 1, 0)
    glColor3f(0.9, 0.9, 0.9); w, h, th = 22.0, 7.0, 0.5
    glPushMatrix(); glTranslatef(-w/2, 0, 0); glRotatef(-90, 1, 0, 0); draw_cylinder(th/2, h, 12); glPopMatrix()
    glPushMatrix(); glTranslatef(w/2, 0, 0); glRotatef(-90, 1, 0, 0); draw_cylinder(th/2, h, 12); glPopMatrix()
    glPushMatrix(); glTranslatef(-w/2 - 0.5, h - th/2, 0); glRotatef(90, 0, 1, 0); draw_cylinder(th/2, w + 1.0, 12); glPopMatrix()
    glPushMatrix(); glTranslatef(0, h - th - 0.8, 0); draw_traffic_light(0, 0, angle=180); glPopMatrix()
    glPopMatrix()

# ============================================================================
# 4. CENÁRIO PRINCIPAL (COM CORREÇÃO DE Z-FIGHTING)
# ============================================================================

# ============================================================================
# FUNÇÃO AUXILIAR: NUVENS
# ============================================================================
def draw_cloud(x, y, z, scale=1.0):
    """ Desenha uma nuvem usando esferas. """
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(scale, scale, scale)
    
    # Cor da nuvem (Branco levemente cinza para reagir à luz)
    glColor3f(0.9, 0.9, 0.95)
    
    # Agrupamento de esferas
    glPushMatrix(); glScalef(1.5, 1.0, 1.0); draw_sphere(3.0, 12, 12); glPopMatrix() # Centro
    glPushMatrix(); glTranslatef(-2.5, -0.5, 0); draw_sphere(2.0, 12, 12); glPopMatrix() # Esq
    glPushMatrix(); glTranslatef(2.5, -0.8, 0.5); draw_sphere(2.2, 12, 12); glPopMatrix() # Dir
    glPushMatrix(); glTranslatef(0.5, 2.0, -0.5); draw_sphere(1.8, 12, 12); glPopMatrix() # Cima
    
    glPopMatrix()

# ============================================================================
# CENÁRIO COMPLETO (ATUALIZADO)
# ============================================================================
def draw_circuit_and_environment():
    track_width = 12.0; straight_length = 150.0; curve_radius = 40.0
    asphalt_color = (0.2, 0.2, 0.2); line_color = (0.9, 0.9, 0.9); grass_color = (0.2, 0.5, 0.1)
    kerb_width = 1.0; kerb_height = 0.1; kerb_len = 5.0
    
    # --- CAMADAS DE ALTURA (LAYERS) ---
    layer_track = 0.05
    layer_line  = 0.06
    kerb_base_y = layer_track

    glMaterialfv(GL_FRONT, GL_EMISSION, (0.0, 0.0, 0.0, 1.0))

    # 1. Chão (Grama)
    glColor3fv(grass_color); glPushMatrix(); glTranslatef(0, -0.02, 0); draw_ground(); glPopMatrix()
    
    # 2. Nuvens (LÓGICA DE CLIMA)
    cloud_r = random.Random(99) 
    
    # Se estiver chovendo: 1000 nuvens. Se não: 100 nuvens.
    num_clouds = 1000 if config.is_raining else 100
    
    for _ in range(num_clouds): 
        cx = cloud_r.randint(-1800, 1800)
        cz = cloud_r.randint(-1800, 1800)
        
        # Zona de exclusão do centro (empurra nuvens para o horizonte)
        if abs(cx) < 600 and abs(cz) < 600:
            if cloud_r.choice([True, False]): cx = cx + 800 if cx > 0 else cx - 800
            else: cz = cz + 800 if cz > 0 else cz - 800

        cy = cloud_r.randint(50, 180)  
        s  = cloud_r.uniform(3.0, 8.0) 
        
        # Se chover: Nuvens Cinzas. Se sol: Nuvens Brancas.
        if config.is_raining:
            glColor3f(0.4, 0.4, 0.45) # Cinza tempestade
        else:
            glColor3f(0.9, 0.9, 0.95) # Branco
            
        draw_cloud(cx, cy, cz, s)
        # Altura variada (nuvens distantes podem parecer mais baixas pela perspectiva)
        cy = cloud_r.randint(50, 180)  
        
        # Tamanho colossal para nuvens distantes (para não parecerem pontinhos)
        s  = cloud_r.uniform(3.0, 8.0) 
        
        draw_cloud(cx, cy, cz, s)

    # Função Auxiliar Zebras
    def draw_kerb_quad_segment(p1_x, p1_z, p2_x, p2_z, g1_x, g1_z, g2_x, g2_z, color, normal):
        glColor3fv(color); y_top = kerb_base_y + kerb_height
        glBegin(GL_QUADS); glNormal3f(0.0, 1.0, 0.0); glVertex3f(p1_x, y_top, p1_z); glVertex3f(g1_x, y_top, g1_z); glVertex3f(g2_x, y_top, g2_z); glVertex3f(p2_x, y_top, p2_z); glEnd()
        glBegin(GL_QUADS); glNormal3fv(normal); glVertex3f(p1_x, kerb_base_y, p1_z); glVertex3f(p2_x, kerb_base_y, p2_z); glVertex3f(p2_x, y_top, p2_z); glVertex3f(p1_x, y_top, p1_z); glEnd()

    # 3. Pista (Retas)
    if config.asphalt_texture_id: glEnable(GL_TEXTURE_2D); glBindTexture(GL_TEXTURE_2D, config.asphalt_texture_id); glColor3f(1, 1, 1)
    else: glColor3fv(asphalt_color)
    tex_rep_x = 4.0; tex_rep_z = 40.0
    for side in [-1, 1]: 
        glPushMatrix(); glTranslatef(side * curve_radius, layer_track, 0); glBegin(GL_QUADS); glNormal3f(0,1,0)
        glTexCoord2f(0,0); glVertex3f(-track_width/2,0,-straight_length/2); glTexCoord2f(tex_rep_x,0); glVertex3f(track_width/2,0,-straight_length/2)
        glTexCoord2f(tex_rep_x,tex_rep_z); glVertex3f(track_width/2,0,straight_length/2); glTexCoord2f(0,tex_rep_z); glVertex3f(-track_width/2,0,straight_length/2)
        glEnd(); glPopMatrix()
    glDisable(GL_TEXTURE_2D)

    # 4. Faixas Centrais (Retas)
    for z in range(int(-straight_length/2) + 5, int(straight_length/2) - 5, 15):
        glColor3fv(line_color)
        glPushMatrix(); glTranslatef(-curve_radius, layer_line, z); glScalef(0.2, 0.01, 5.0); draw_cuboid(1, 1, 1); glPopMatrix()
        glPushMatrix(); glTranslatef(curve_radius, layer_line, z); glScalef(0.2, 0.01, 5.0); draw_cuboid(1, 1, 1); glPopMatrix()

    # 5. Zebras Retas
    num_segs = int(straight_length / kerb_len)
    for i in range(num_segs):
        z1 = -straight_length/2 + (i * kerb_len); z2 = z1 + kerb_len; c = (1,0,0) if i % 2 == 0 else (1,1,1)
        draw_kerb_quad_segment(-curve_radius-track_width/2, z1, -curve_radius-track_width/2, z2, -curve_radius-track_width/2-kerb_width, z1, -curve_radius-track_width/2-kerb_width, z2, c, (1,0,0))
        draw_kerb_quad_segment(-curve_radius+track_width/2, z1, -curve_radius+track_width/2, z2, -curve_radius+track_width/2+kerb_width, z1, -curve_radius+track_width/2+kerb_width, z2, c, (-1,0,0))
        draw_kerb_quad_segment(curve_radius+track_width/2, z1, curve_radius+track_width/2, z2, curve_radius+track_width/2+kerb_width, z1, curve_radius+track_width/2+kerb_width, z2, c, (-1,0,0))
        draw_kerb_quad_segment(curve_radius-track_width/2, z1, curve_radius-track_width/2, z2, curve_radius-track_width/2-kerb_width, z1, curve_radius-track_width/2-kerb_width, z2, c, (1,0,0))

    # 6. Curvas (Função Interna)
    def draw_curve(base_z, start, end):
        glPushMatrix(); glTranslatef(0, 0, base_z)
        if config.asphalt_texture_id: glEnable(GL_TEXTURE_2D); glBindTexture(GL_TEXTURE_2D, config.asphalt_texture_id); glColor3f(1,1,1)
        else: glColor3fv(asphalt_color)
        glBegin(GL_QUAD_STRIP); glNormal3f(0, 1, 0)
        steps = 90; step = (end - start) / steps
        for i in range(int(steps) + 1):
            rad = math.radians(start + (i * step)); c, s = math.cos(rad), math.sin(rad); v = (i/steps) * 5.0
            glTexCoord2f(tex_rep_x, v); glVertex3f((curve_radius + track_width/2) * c, layer_track, (curve_radius + track_width/2) * s)
            glTexCoord2f(0, v);         glVertex3f((curve_radius - track_width/2) * c, layer_track, (curve_radius - track_width/2) * s)
        glEnd(); glDisable(GL_TEXTURE_2D)
        
        # Faixas Curva
        glColor3fv(line_color); line_deg = 8.0; line_gap = 8.0; total = end - start; num_lines = int(abs(total) / (line_deg + line_gap)); d = 1 if total > 0 else -1
        for i in range(num_lines):
            seg_start = start + (i * (line_deg + line_gap) * d); mid_rad = math.radians(seg_start + (line_deg * d / 2.0))
            glPushMatrix(); glTranslatef(curve_radius * math.cos(mid_rad), layer_line, curve_radius * math.sin(mid_rad)); glRotatef(-math.degrees(mid_rad), 0, 1, 0); glScalef(0.2, 0.01, 4.0); draw_cuboid(1, 1, 1); glPopMatrix()
        
        # Zebras Curva
        local_seg_angle = 10.0; num_kerbs = int(abs(total) / local_seg_angle)
        for i in range(num_kerbs):
            if start < end: a1, a2 = start + (i*local_seg_angle), start + ((i+1)*local_seg_angle)
            else: a1, a2 = start - (i*local_seg_angle), start - ((i+1)*local_seg_angle)
            c_col = (1, 0, 0) if i % 2 == 0 else (1, 1, 1)
            if a1 > a2: a_s, a_e = a2, a1
            else: a_s, a_e = a1, a2
            r1, r2 = math.radians(a_s), math.radians(a_e); c1, s1 = math.cos(r1), math.sin(r1); c2, s2 = math.cos(r2), math.sin(r2)
            mid = (r1+r2)/2; nx, nz = math.cos(mid), math.sin(mid)
            r_in = curve_radius + track_width/2; r_out = r_in + kerb_width
            draw_kerb_quad_segment(r_in*c1, r_in*s1, r_in*c2, r_in*s2, r_out*c1, r_out*s1, r_out*c2, r_out*s2, c_col, (nx, 0, nz))
            r_out_i = curve_radius - track_width/2; r_in_i = r_out_i - kerb_width
            draw_kerb_quad_segment(r_out_i*c1, r_out_i*s1, r_out_i*c2, r_out_i*s2, r_in_i*c1, r_in_i*s1, r_in_i*c2, r_in_i*s2, c_col, (-nx, 0, -nz))
        
        # Pneus
        draw_tire_wall_arc(curve_radius + track_width/2 + 5.0, start, end)
        glPopMatrix()

    # Desenha as duas curvas
    draw_curve(-straight_length/2, 180, 360)
    draw_curve(straight_length/2, 0, 180)

    # 7. Arquibancadas e Grades
    glPushMatrix()
    stand_len = 120.0; fence_offset = 32.5
    glPushMatrix(); glTranslatef(15, 0, 0); glRotatef(-90, 0, 1, 0); draw_grandstand(stand_len, 12); glPopMatrix()
    glPushMatrix(); glTranslatef(fence_offset, 0, 0); draw_safety_fence(150); glPopMatrix()
    glPushMatrix(); glTranslatef(-15, 0, 0); glRotatef(90, 0, 1, 0); draw_grandstand(stand_len, 12); glPopMatrix()
    glPushMatrix(); glTranslatef(-fence_offset, 0, 0); draw_safety_fence(150); glPopMatrix()
    glPopMatrix()

    # 8. Árvores
    r = random.Random(42); count = 0
    while count < 40:
        tx, tz = r.randint(-200, 200), r.randint(-250, 250)
        if abs(tx) < 70 and abs(tz) < 140: continue
        draw_tree(tx, tz); count += 1
    for i in range(0, 360, 15): rad = math.radians(i); draw_tree(140 * math.cos(rad), 140 * math.sin(rad))

    # 9. Cones
    for ox, oz in [(-40, 0), (-40, -15), (40, 20), (40, 35), (40, 50)]:
        glPushMatrix(); glTranslatef(ox, layer_track, oz); glRotatef(-90, 1, 0, 0); draw_obstacle_cone(0.4, 1.0); glPopMatrix()

    # 10. Postes (São desenhados dinamicamente no main.py)
    pass

def draw_all_lampposts():
    """ 
    Desenha todos os postes de luz. 
    Separado do cenário estático para permitir acender/apagar a luz.
    """
    track_width = 12.0; curve_radius = 40.0; kerb_width = 1.0
    
    # Distância lateral dos postes
    dist_x = curve_radius + track_width/2 + kerb_width + 5.0
    
    # Posições Z dos postes
    z_positions = [100, 50, 0, -50, -100, -150]
    
    for pz in z_positions:
        # Lado Direito
        glPushMatrix()
        glTranslatef(dist_x, 0, pz)
        glRotatef(180, 0, 1, 0) 
        draw_lamppost()
        glPopMatrix()
        
        # Lado Esquerdo
        glPushMatrix()
        glTranslatef(-dist_x, 0, pz)
        draw_lamppost()
        glPopMatrix()

    # 5. Objetos Extras
    glPushMatrix()
    stand_len = 120.0; fence_offset = 32.5
    glPushMatrix(); glTranslatef(15, 0, 0); glRotatef(-90, 0, 1, 0); draw_grandstand(stand_len, 12); glPopMatrix()
    glPushMatrix(); glTranslatef(fence_offset, 0, 0); draw_safety_fence(150); glPopMatrix()

    glPushMatrix(); glTranslatef(-15, 0, 0); glRotatef(90, 0, 1, 0); draw_grandstand(stand_len, 12); glPopMatrix()
    glPushMatrix(); glTranslatef(-fence_offset, 0, 0); draw_safety_fence(150); glPopMatrix()
    glPopMatrix()

    r = random.Random(42); count = 0
    while count < 40:
        tx, tz = r.randint(-200, 200), r.randint(-250, 250)
        if abs(tx) < 70 and abs(tz) < 140: continue
        draw_tree(tx, tz); count += 1
    for i in range(0, 360, 15): rad = math.radians(i); draw_tree(140 * math.cos(rad), 140 * math.sin(rad))

    obstacle_positions = [(-40, 0), (-40, -15), (40, 20), (40, 35), (40, 50)]
    for ox, oz in obstacle_positions:
        # SUBSTITUÍDO: layer_track POR 0.05
        glPushMatrix(); glTranslatef(ox, 0.05, oz); glRotatef(-90, 1, 0, 0); draw_obstacle_cone(0.4, 1.0); glPopMatrix()

    dist_x = curve_radius + track_width/2 + kerb_width + 5.0
    for pz in [100, 50, 0, -50, -100, -150]:
        glPushMatrix(); glTranslatef(dist_x, 0, pz); glRotatef(180, 0, 1, 0); draw_lamppost(); glPopMatrix()

    cloud_r = random.Random(99) 
    
    for _ in range(15): # 15 Nuvens
        # Posição aleatória no céu
        cx = cloud_r.randint(-400, 400)
        cy = cloud_r.randint(60, 100) # Altura (bem alto)
        cz = cloud_r.randint(-400, 400)
        s = cloud_r.uniform(1.5, 3.0) # Tamanho variado
        
        draw_cloud(cx, cy, cz, s)