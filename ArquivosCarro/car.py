from OpenGL.GL import *
from OpenGL.GLU import *
import config
import drawing 
import pneutexturizado

# ============================================================================
# FUNÇÕES AUXILIARES DE GEOMETRIA
# ============================================================================

def draw_cube_local():
    """ Desenha um cubo unitário (1x1x1) centrado na origem (0,0,0). """
    glBegin(GL_QUADS)
    # Frente
    glNormal3f(0, 0, 1); glVertex3f(-0.5, -0.5, 0.5); glVertex3f(0.5, -0.5, 0.5); glVertex3f(0.5, 0.5, 0.5); glVertex3f(-0.5, 0.5, 0.5)
    # Trás
    glNormal3f(0, 0, -1); glVertex3f(-0.5, 0.5, -0.5); glVertex3f(0.5, 0.5, -0.5); glVertex3f(0.5, -0.5, -0.5); glVertex3f(-0.5, -0.5, -0.5)
    # Esquerda
    glNormal3f(-1, 0, 0); glVertex3f(-0.5, -0.5, -0.5); glVertex3f(-0.5, -0.5, 0.5); glVertex3f(-0.5, 0.5, 0.5); glVertex3f(-0.5, 0.5, -0.5)
    # Direita
    glNormal3f(1, 0, 0); glVertex3f(0.5, -0.5, 0.5); glVertex3f(0.5, -0.5, -0.5); glVertex3f(0.5, 0.5, -0.5); glVertex3f(0.5, 0.5, 0.5)
    # Topo
    glNormal3f(0, 1, 0); glVertex3f(-0.5, 0.5, 0.5); glVertex3f(0.5, 0.5, 0.5); glVertex3f(0.5, 0.5, -0.5); glVertex3f(-0.5, 0.5, -0.5)
    # Base
    glNormal3f(0, -1, 0); glVertex3f(-0.5, -0.5, -0.5); glVertex3f(0.5, -0.5, -0.5); glVertex3f(0.5, -0.5, 0.5); glVertex3f(-0.5, -0.5, 0.5)
    glEnd()

def draw_wedge_flap():
    """ Desenha um formato de cunha para os flaps aerodinâmicos. """
    glBegin(GL_QUADS)
    glNormal3f(0, -1, 0); glVertex3f(-0.5, 0, -0.5); glVertex3f(0.5, 0, -0.5); glVertex3f(0.5, 0, 0.5); glVertex3f(-0.5, 0, 0.5)
    glNormal3f(0, 0, -1); glVertex3f(-0.5, 0.2, -0.5); glVertex3f(0.5, 0.2, -0.5); glVertex3f(0.5, 0, -0.5); glVertex3f(-0.5, 0, -0.5)
    glNormal3f(0, 1, 0.5); glVertex3f(-0.5, 0.2, -0.5); glVertex3f(0.5, 0.2, -0.5); glVertex3f(0.5, 0.05, 0.5); glVertex3f(-0.5, 0.05, 0.5)
    glEnd()
    glBegin(GL_TRIANGLES)
    glVertex3f(-0.5, 0, -0.5); glVertex3f(-0.5, 0.2, -0.5); glVertex3f(-0.5, 0.05, 0.5)
    glVertex3f(0.5, 0, -0.5); glVertex3f(0.5, 0.2, -0.5); glVertex3f(0.5, 0.05, 0.5)
    glEnd()

def draw_endplate_shape():
    """ Desenha o polígono lateral das asas (Trapézio invertido). """
    glBegin(GL_POLYGON)
    glNormal3f(1, 0, 0)
    glVertex3f(0.0, 0.2, 0.5)   # Topo Frente
    glVertex3f(0.0, 0.2, -0.5)  # Topo Trás
    glVertex3f(0.0, -0.3, -0.4) # Baixo Trás
    glVertex3f(0.0, -0.2, 0.4)  # Baixo Frente
    glEnd()

# ============================================================================
# COMPONENTES AERODINÂMICOS (ASAS)
# ============================================================================

def draw_detailed_front_wing():
    """ Renderiza a asa dianteira completa estilo Brabham Martini. """
    glPushAttrib(GL_ALL_ATTRIB_BITS)
    glPushMatrix()

    # Redução de escala (20%) e ajuste de posição para perto das rodas
    glScalef(0.8, 0.8, 0.8) 
    glTranslatef(0, 0, -1) 

    # Definição de Cores
    RED_BRABHAM = (0.8, 0.1, 0.1)
    BLUE_DARK   = (0.0, 0.1, 0.5)
    BLUE_LIGHT  = (0.3, 0.6, 1.0)
    WHITE       = (1.0, 1.0, 1.0)
    BLACK_TIRE  = (0.1, 0.1, 0.1)

    # Dimensões
    total_width = 2.4
    main_chord = 1.2
    wing_height = 0.1
    
    # 1. Plano Principal (Base Vermelha)
    glColor3fv(RED_BRABHAM)
    glPushMatrix(); glScalef(total_width, wing_height, main_chord); draw_cube_local(); glPopMatrix()
    
    # Fundo Preto (Skid block)
    glColor3fv(BLACK_TIRE)
    glPushMatrix(); glTranslatef(0, -wing_height/2 - 0.01, 0); glScalef(total_width*0.9, 0.02, main_chord*0.9); draw_cube_local(); glPopMatrix()

    # 2. Bico Central e Listras
    nose_width = 0.6 
    glPushMatrix()
    glTranslatef(0, 0.2, -0.1)
    glRotatef(15, 1, 0, 0) 
    
    # Base do bico
    glColor3fv(RED_BRABHAM)
    glPushMatrix(); glScalef(nose_width, 0.3, main_chord*0.8); draw_cube_local(); glPopMatrix()

    # --- Decalques Martini Racing ---
    stripe_layer_h = 0.155 
    
    # Faixa Branca Central
    glColor3fv(WHITE)
    glPushMatrix(); glTranslatef(0, stripe_layer_h, 0); glScalef(nose_width * 0.7, 0.01, main_chord*0.7); draw_cube_local(); glPopMatrix()
    
    # Faixas Azuis Escuras
    glColor3fv(BLUE_DARK)
    strip_pos = nose_width * 0.35 + 0.02
    glPushMatrix(); glTranslatef(-strip_pos, stripe_layer_h, 0); glScalef(0.05, 0.01, main_chord*0.7); draw_cube_local(); glPopMatrix()
    glPushMatrix(); glTranslatef(strip_pos, stripe_layer_h, 0); glScalef(0.05, 0.01, main_chord*0.7); draw_cube_local(); glPopMatrix()

    # Faixas Azuis Claras
    glColor3fv(BLUE_LIGHT)
    glPushMatrix(); glTranslatef(-0.06, stripe_layer_h + 0.005, 0); glScalef(0.08, 0.01, main_chord*0.65); draw_cube_local(); glPopMatrix()
    glPushMatrix(); glTranslatef(0.06, stripe_layer_h + 0.005, 0); glScalef(0.08, 0.01, main_chord*0.65); draw_cube_local(); glPopMatrix()
    glPopMatrix() # Fim do grupo Bico

    # 3. Flaps Laterais
    glColor3fv(RED_BRABHAM)
    flap_offset = nose_width/2 + 0.4
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * flap_offset, wing_height/2, 0.1)
        glRotatef(side * -5, 0, 1, 0)
        glScalef(0.8, 1.0, 0.8)
        draw_wedge_flap()
        glPopMatrix()

    # 4. Endplates (Laterais verticais da asa)
    endplate_pos_x = total_width / 2
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * (endplate_pos_x - 0.05), 0.2, 0)
        
        # Placa Principal
        glColor3fv(RED_BRABHAM)
        glPushMatrix(); glScalef(0.1, 0.5, main_chord * 1.1); draw_cube_local(); glPopMatrix()
        
        # Detalhe aerodinâmico externo
        glPushMatrix()
        glTranslatef(side * 0.1, -0.15, 0.1) 
        glRotatef(side * -15, 0, 1, 0)
        glRotatef(side * -10, 0, 0, 1) 
        glScalef(0.08, 0.4, 0.8)
        draw_cube_local()
        glPopMatrix()
        glPopMatrix()

    glPopMatrix()
    glPopAttrib()

def draw_detailed_rear_wing():
    """ Renderiza o aerofólio traseiro completo. """
    wing_width = 2.4
    plate_thickness = 0.05
    wing_chord = 0.8
    wing_thickness = 0.1
    
    glPushMatrix()
    glTranslatef(0.0, 0.9, -2.2) # Posição traseira

    # Endplates (Laterais)
    glColor3f(0.8, 0.1, 0.1) 
    # Direita
    glPushMatrix()
    glTranslatef((wing_width / 2), 0, 0)
    draw_endplate_shape()
    glTranslatef(-plate_thickness, 0, 0)
    draw_endplate_shape()
    glPopMatrix()
    # Esquerda
    glPushMatrix()
    glTranslatef(-(wing_width / 2), 0, 0)
    draw_endplate_shape()
    glTranslatef(plate_thickness, 0, 0)
    draw_endplate_shape()
    glPopMatrix()

    # Lâmina Principal
    glColor3f(0.8, 0.1, 0.1)
    glPushMatrix()
    glTranslatef(0, 0.1, 0)
    glScalef(wing_width, wing_thickness, wing_chord)
    draw_cube_local()
    glPopMatrix()
    
    # Decalques Traseiros
    stripe_width = 0.15
    # Azul Claro
    glColor3f(0.2, 0.6, 1.0)
    glPushMatrix(); glTranslatef(-stripe_width, 0.155, 0); glScalef(stripe_width, 0.01, wing_chord); draw_cube_local(); glPopMatrix()
    # Azul Escuro
    glColor3f(0.0, 0.0, 0.6)
    glPushMatrix(); glTranslatef(stripe_width, 0.155, 0); glScalef(stripe_width, 0.01, wing_chord); draw_cube_local(); glPopMatrix()
    
    # Pilar Central
    glColor3f(0.1, 0.1, 0.1)
    glPushMatrix(); glTranslatef(0, -0.4, 0.1); glScalef(0.1, 0.8, 0.3); draw_cube_local(); glPopMatrix()

    glPopMatrix()

# ============================================================================
# COMPONENTES DO CORPO (CHASSI)
# ============================================================================

def draw_chassis():
    """ Desenha o corpo principal do carro. """
    # Corpo Principal
    glColor3f(0.8, 0.1, 0.1) 
    glPushMatrix()
    glTranslatef(0, 0.25, -0.3)
    glScalef(1.5, 0.45, 3.8)
    drawing.draw_trapezoidal_prism()
    glPopMatrix()
    
    # Fundo Plano (Chassi Central Inferior)
    glColor3f(0.7, 0.1, 0.1)
    glPushMatrix()
    glTranslatef(0, 0.15, -0.5)
    glScalef(1.3, 0.30, 1)
    glRotatef(-4.0, -1, 0, 0)
    drawing.draw_cuboid(1, 1, 1)
    glPopMatrix()

    # Nariz (Conexão com a asa)
    glColor3f(0.8, 0.1, 0.1)
    glPushMatrix()
    glTranslatef(0, 0.2, 1.8)
    glRotatef(-4.0, -1, 0, 0)
    glScalef(0.8, 0.3, 1.8)
    drawing.draw_trapezoidal_prism()
    glPopMatrix()

def draw_wings():
    """ Agrupa as chamadas das asas dianteira e traseira. """
    # Asa Dianteira
    glPushMatrix()
    glTranslatef(0, 0.1, 3.2) 
    draw_detailed_front_wing()
    glPopMatrix()
    
    # Asa Traseira
    draw_detailed_rear_wing()

def draw_sidepods():
    """ Desenha as laterais e o airbox do motor. """
    sidepod_y = 0.22; sidepod_x = 0.9 
    sidepod_w = 0.40; sidepod_h = 0.5; sidepod_l = 2.5 
    
    glColor3f(0.8, 0.1, 0.1) 
    
    # Lateral Direita
    glPushMatrix()
    glTranslatef(sidepod_x, sidepod_y, -0.5)
    glRotatef(-90, 0, 0, 1)
    glScalef(sidepod_w, sidepod_h, sidepod_l)
    drawing.draw_trapezoidal_prism() 
    glPopMatrix()
    
    # Lateral Esquerda
    glPushMatrix()
    glTranslatef(-sidepod_x, sidepod_y, -0.5)
    glRotatef(90, 0, 0, 1)
    glScalef(sidepod_w, sidepod_h, sidepod_l)
    drawing.draw_trapezoidal_prism()
    glPopMatrix()

    # --- Airbox (Entrada de ar superior) ---
    # Parte Preta (Interna)
    glColor3f(0.1, 0.1, 0.1)
    glPushMatrix()
    glTranslatef(0, 0.6, -0.5)  
    glRotatef(180, 0, 1, 0)
    glScalef(0.6, 0.8, 0.7)
    drawing.draw_trapezoidal_prism()
    glPopMatrix()

    # Parte Vermelha (Carenagem)
    glColor3f(0.8, 0.1, 0.1)
    glPushMatrix()
    glTranslatef(0, 0.6, -0.55)  
    glRotatef(180, 0, 1, 0)
    glScalef(0.6, 0.90, 0.7)
    drawing.draw_trapezoidal_prism()
    glPopMatrix()

    # Conexão traseira
    glPushMatrix()
    glTranslatef(0, 0.6, -1)
    glRotatef(180, 0, 1, 0)
    glScalef(1.2, 0.5, 1.6)
    drawing.draw_trapezoidal_prism()
    glPopMatrix()

# ============================================================================
# ESCAPAMENTO
# ============================================================================
def draw_exhaust_system():
    """ Desenha as ponteiras de escapamento com interior preto e profundidade. """
    
    # Configuração do material metálico (brilho especular) para a parte EXTERNA
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0.9, 0.9, 0.9, 1.0))
    glMaterialf(GL_FRONT, GL_SHININESS, 100.0)

    # Função auxiliar interna
    def draw_single_pipe(side_sign):
        glPushMatrix()
        # Posição e inclinação
        glTranslatef(0.15 * side_sign, 0.4, -2.3)
        glRotatef(-10, 1, 0, 0)
        glRotatef(5 * side_sign, 0, 1, 0)

        quad = gluNewQuadric()

        # --- 1. TUBO EXTERNO (Metálico e Brilhante) ---
        # A iluminação está ligada aqui, pegando o material metálico definido acima.
        glColor3f(0.4, 0.4, 0.45) # Cor base cinza metálico
        # Raio externo = 0.08
        gluCylinder(quad, 0.08, 0.08, 0.5, 24, 1) 
        
        # --- 2. INTERIOR (Preto Fosco / Fuligem) ---
        # Desabilitamos a iluminação para que o interior seja um preto "chapado",
        # sem reflexos, criando a ilusão de um buraco fundo e escuro.
        glDisable(GL_LIGHTING)
        glColor3f(0.0, 0.0, 0.0) # Preto Puro

        # Desenha um cilindro interno ligeiramente menor (raio 0.078 vs 0.08 externo)
        # para evitar que eles se cruzem visualmente (Z-fighting).
        gluCylinder(quad, 0.078, 0.078, 0.5, 24, 1)

        # Desenha a "tampa" do fundo do escapamento
        glPushMatrix()
        glTranslatef(0, 0, 0.5) # Move para o final do tubo
        gluDisk(quad, 0.0, 0.078, 24, 1) # Fecha o buraco
        glPopMatrix()

        # IMPORTANTE: Reabilita a iluminação para o próximo objeto do carro
        glEnable(GL_LIGHTING) 
        
        gluDeleteQuadric(quad)
        glPopMatrix()

    # Desenha os dois lados
    draw_single_pipe(1)
    draw_single_pipe(-1)

    # Reseta o material para o padrão (sem brilho)
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0))
    glMaterialf(GL_FRONT, GL_SHININESS, 0.0)
# ============================================================================
# COCKPIT E PILOTO
# ============================================================================

def draw_cockpit_area():
    """ Desenha o cockpit, para-brisa, piloto e volante animado. """
    cockpit_y = 0.40; cockpit_z = 0.4
    inner_w = 0.9; outer_w = 0.9 

    # Base Preta do Cockpit
    glColor3f(0.05, 0.05, 0.05) 
    glPushMatrix()
    glTranslatef(0, cockpit_y + 0.1 , cockpit_z - 0.1)
    glRotatef(-4.0, -1, 0, 0)
    glScalef(inner_w, 0.25, 2) 
    drawing.draw_trapezoidal_prism()
    glPopMatrix()

    # --- Proteções Laterais do Cockpit ---
    glColor3f(0.9, 0.1, 0.1) 

    # Lateral Esquerda
    glPushMatrix()
    glTranslatef(outer_w/2, cockpit_y + 0.1, cockpit_z)
    glRotatef(75, 0, 1, 0)
    glRotatef(-15, 1, 0, 0) # Inclinação aerodinâmica
    glScalef(2, 0.25, 0.1)
    drawing.draw_trapezoidal_prism()
    glPopMatrix()

    # Lateral Direita
    glPushMatrix()
    glTranslatef(-outer_w/2, cockpit_y + 0.1, cockpit_z)
    glRotatef(-75, 0, 1, 0)
    glRotatef(15, 1, 0, 0)
    glScalef(2, 0.25, 0.1)
    drawing.draw_trapezoidal_prism()
    glPopMatrix()

    # Encosto/Painel
    glPushMatrix()
    glTranslatef(0, 0.4, 1.3)
    glScalef(0.7, 0.5, 1)
    drawing.draw_trapezoidal_prism()
    glPopMatrix()
    
    # Para-brisa (Transparente)
    glColor4f(0.1, 0.1, 0.2, 0.5)
    glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glPushMatrix()
    glTranslatef(0, cockpit_y + 0.35, cockpit_z + 0.5)
    glRotatef(-45, 1, 0, 0)
    glScalef(outer_w * 0.8, 0.2, 0.05)
    drawing.draw_cuboid(1, 1, 1)
    glPopMatrix()
    glDisable(GL_BLEND)

    # --- Piloto (Cabeça Animada) ---
    head_pos = (0, 0.65, 0.25)
    glPushMatrix()
    glTranslatef(head_pos[0], head_pos[1], head_pos[2])
    glRotatef(config.front_wheel_steer_angle * 0.8, 0, 1, 0) # Olha para a curva

    # Materiais do capacete
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0.5, 0.5, 0.5, 1.0)); glMaterialf(GL_FRONT, GL_SHININESS, 40.0)
    
    # Capacete e detalhes
    glColor3f(0.95, 0.95, 0.95); glPushMatrix(); glScalef(1.05, 1.15, 1.25); drawing.draw_sphere(0.16); glPopMatrix()
    glColor3f(0.1, 0.1, 0.12); glPushMatrix(); glTranslatef(0, 0.07, 0); glScalef(1.06, 0.75, 1.26); drawing.draw_sphere(0.161); glPopMatrix()
    glColor3f(1.0, 0.85, 0.0); glPushMatrix(); glTranslatef(0, 0.045, 0); glScalef(1.07, 0.12, 1.27); drawing.draw_sphere(0.162); glPopMatrix()
    
    # Rosto
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0)); glColor3f(0.05, 0.05, 0.05)
    glPushMatrix(); glTranslatef(0, 0.03, 0.14); glScalef(0.17, 0.11, 0.08); drawing.draw_sphere(1.0); glPopMatrix()
    
    # Viseira
    glColor3f(1.0, 1.0, 0.0); glMaterialfv(GL_FRONT, GL_SPECULAR, (0.5, 0.5, 0.5, 1.0))
    glPushMatrix(); glTranslatef(0, 0.03, 0.178); glRotatef(10, 1, 0, 0); glScalef(0.17, 0.095, 0.03); drawing.draw_sphere(1.0); glPopMatrix()
    
    # Reflexo Viseira
    glEnable(GL_BLEND); glColor4f(0.05, 0.05, 0.1, 0.95)
    glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0)); glMaterialf(GL_FRONT, GL_SHININESS, 120.0)
    glPushMatrix(); glTranslatef(0, 0.03, 0.18); glRotatef(10, 1, 0, 0); glScalef(0.16, 0.085, 0.04); drawing.draw_sphere(1.0); glPopMatrix()
    glDisable(GL_BLEND)
    glPopMatrix() # Fim Cabeça
    
    # --- Volante Animado ---
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0)); glMaterialf(GL_FRONT, GL_SHININESS, 0.0)
    glColor3f(0.9, 0.9, 0.8)
    glPushMatrix()
    glTranslatef(0, 0.5, 0.7) 
    glRotatef(config.front_wheel_steer_angle * 3.0, 0, 0, 1) 
    glScalef(0.2, 0.2, 0.05)
    drawing.draw_cuboid(1, 1, 1)
    glPopMatrix()


# ============================================================================
# LOGOS E ADESIVOS (MARTINI RACING)
# ============================================================================

def draw_logos():
    """ Desenha as texturas da Martini nos sidepods e a NOVA logo no aerofólio. """
    
    # --- PARTE 1: SIDEPODS (martiniRacing.png) ---
    # (Mantido igual pois já estava funcionando)
    texture_side = getattr(config, 'logo_texture_id', None)
    if not texture_side and hasattr(config, 'martini_texture_id'):
        texture_side = config.martini_texture_id

    if texture_side:
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_side)
        glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor3f(1, 1, 1)

        sp_logo_w = 1.0; sp_logo_h = 0.45

        # Sidepod Esquerdo
        glPushMatrix()
        glTranslatef(-1.13, 0.25, -0.8) 
        glRotatef(90, 0, 1, 0) 
        glBegin(GL_QUADS)
        glTexCoord2f(1, 0); glVertex3f(-sp_logo_w/2, -sp_logo_h/2, 0)
        glTexCoord2f(0, 0); glVertex3f(sp_logo_w/2, -sp_logo_h/2, 0)
        glTexCoord2f(0, 1); glVertex3f(sp_logo_w/2, sp_logo_h/2, 0)
        glTexCoord2f(1, 1); glVertex3f(-sp_logo_w/2, sp_logo_h/2, 0)
        glEnd()
        glPopMatrix()

        # Sidepod Direito
        glPushMatrix()
        glTranslatef(1.13, 0.25, -0.8) 
        glRotatef(-90, 0, 1, 0)
        glBegin(GL_QUADS)
        glTexCoord2f(1, 0); glVertex3f(-sp_logo_w/2, -sp_logo_h/2, 0)
        glTexCoord2f(0, 0); glVertex3f(sp_logo_w/2, -sp_logo_h/2, 0)
        glTexCoord2f(0, 1); glVertex3f(sp_logo_w/2, sp_logo_h/2, 0)
        glTexCoord2f(1, 1); glVertex3f(-sp_logo_w/2, sp_logo_h/2, 0)
        glEnd()
        glPopMatrix()
        
        glDisable(GL_TEXTURE_2D)
        glPopAttrib()

    # --- PARTE 2: AEROFÓLIO (MartiniLogo.png) ---
    texture_wing = getattr(config, 'wing_logo_texture_id', None)
    
    if texture_wing:
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_wing) 
        glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor3f(1, 1, 1)

        # CORREÇÃO DE PROPORÇÃO (Desachatar)
        # Diminuí a largura e aumentei ligeiramente a altura para uma proporção melhor
        wing_w, wing_h = 0.8, 0.4

        # Logo Topo da Asa
        glPushMatrix()
        glTranslatef(0.0, 1.07, -2.2) # Altura correta acima das faixas
        
        glRotatef(-90, 1, 0, 0) # Deitado virado para cima
        
        # CORREÇÃO DE ORIENTAÇÃO (Desvirar)
        # Removi o glRotatef(180, 0, 0, 1) que estava aqui.
        # Agora ele deve ficar legível para quem olha o carro de frente/cima.
        
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(-wing_w/2, -wing_h/2, 0)
        glTexCoord2f(1, 0); glVertex3f(wing_w/2, -wing_h/2, 0)
        glTexCoord2f(1, 1); glVertex3f(wing_w/2, wing_h/2, 0)
        glTexCoord2f(0, 1); glVertex3f(-wing_w/2, wing_h/2, 0)
        glEnd()
        glPopMatrix()
        
        glPopAttrib()
# ============================================================================
# RODAS E SUSPENSÃO
# ============================================================================

def draw_wheels_system():
    """ Desenha as rodas com textura e a suspensão detalhada (triângulos duplos). """
    f_rad = 0.4; f_width = 0.4; r_rad = 0.5; r_width = 0.7
    fx = 1.0; rx = 1.3; fz = 1.5; rz = -1.8
    fy = 0.25; ry = 0.3 # Altura do eixo

    # --- Desenha as Rodas (Base branca para textura) ---
    glColor3f(1.0, 1.0, 1.0) 
    # Dianteira Direita
    glPushMatrix(); glTranslatef(fx, fy, fz); glRotatef(config.front_wheel_steer_angle, 0, 1, 0); glRotatef(config.wheel_rotation_angle, 1, 0, 0); pneutexturizado.draw_f1_wheel(f_rad, f_width); glPopMatrix()
    # Dianteira Esquerda
    glPushMatrix(); glTranslatef(-fx, fy, fz); glRotatef(config.front_wheel_steer_angle, 0, 1, 0); glRotatef(180, 0, 1, 0); glRotatef(-config.wheel_rotation_angle, 1, 0, 0); pneutexturizado.draw_f1_wheel(f_rad, f_width); glPopMatrix()
    # Traseira Direita
    glPushMatrix(); glTranslatef(rx, ry, rz); glRotatef(config.wheel_rotation_angle, 1, 0, 0); pneutexturizado.draw_f1_wheel(r_rad, r_width); glPopMatrix()
    # Traseira Esquerda
    glPushMatrix(); glTranslatef(-rx, ry, rz); glRotatef(180, 0, 1, 0); glRotatef(-config.wheel_rotation_angle, 1, 0, 0); pneutexturizado.draw_f1_wheel(r_rad, r_width); glPopMatrix()

    # --- Suspensão (Triângulos e Braços) ---
    glColor3f(0.2, 0.2, 0.25) 
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0.7, 0.7, 0.7, 1.0)); glMaterialf(GL_FRONT, GL_SHININESS, 60.0)

    # Função interna para desenhar braços
    def draw_suspension_arm(start_x, start_y, start_z, end_x, end_y, end_z):
        glBegin(GL_LINES)
        glVertex3f(start_x, start_y, start_z); glVertex3f(end_x, end_y, end_z)
        glEnd()

    glLineWidth(3.0) 

    # Pontos de conexão
    chassis_fx = 0.3; wheel_fy_up = fy + 0.15; wheel_fy_down = fy - 0.15
    
    # Suspensão Dianteira (Direita/Esquerda)
    for s in [1, -1]: # 1=Dir, -1=Esq
        sx = chassis_fx * s; ex = (fx - 0.1) * s
        # Braço Superior
        draw_suspension_arm(sx, fy + 0.1, fz - 0.2, ex, wheel_fy_up, fz)
        draw_suspension_arm(sx, fy + 0.1, fz + 0.2, ex, wheel_fy_up, fz)
        # Braço Inferior
        draw_suspension_arm(sx, fy - 0.1, fz - 0.2, ex, wheel_fy_down, fz)
        draw_suspension_arm(sx, fy - 0.1, fz + 0.2, ex, wheel_fy_down, fz)

    # Suspensão Traseira
    chassis_rx = 0.4; wheel_ry_up = ry + 0.2; wheel_ry_down = ry - 0.2
    
    for s in [1, -1]:
        sx = chassis_rx * s; ex = (rx - 0.1) * s
        # Superior
        draw_suspension_arm(sx, ry + 0.2, rz + 0.3, ex, wheel_ry_up, rz)
        draw_suspension_arm(0.1*s, ry + 0.3, rz + 0.8, ex, wheel_ry_up, rz)
        # Inferior
        draw_suspension_arm(sx, ry - 0.2, rz + 0.3, ex, wheel_ry_down, rz)
        draw_suspension_arm(0.1*s, ry - 0.1, rz + 0.8, ex, wheel_ry_down, rz)
        
        # Eixo de transmissão (Mais grosso)
        glLineWidth(6.0); glColor3f(0.15, 0.15, 0.2)
        draw_suspension_arm(0.2*s, ry, rz + 0.1, ex, ry, rz)
        glLineWidth(3.0); glColor3f(0.2, 0.2, 0.25) # Reseta cor

    glLineWidth(1.0); glMaterialfv(GL_FRONT, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0)); glMaterialf(GL_FRONT, GL_SHININESS, 0.0)

# ============================================================================
# MONTAGEM FINAL
# ============================================================================

def draw_complete_car():
    draw_chassis()
    draw_wings()
    draw_sidepods()
    draw_cockpit_area()
    draw_wheels_system()
    draw_exhaust_system()
    draw_logos()
    


    glDisable(GL_TEXTURE_2D); glDisable(GL_BLEND); glColor3f(1, 1, 1)