import pygame
import math
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_text(x, y, text, font, color=(255, 255, 255)):
    """
    Renderiza texto na tela OpenGL.
    """
    text_surface = font.render(text, True, color).convert_alpha()
    text_data = pygame.image.tostring(text_surface, "RGBA", False)
    width, height = text_surface.get_size()

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    glColor3f(1, 1, 1) 
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x, y)
    glTexCoord2f(1, 0); glVertex2f(x + width, y)
    glTexCoord2f(1, 1); glVertex2f(x + width, y + height)
    glTexCoord2f(0, 1); glVertex2f(x, y + height)
    glEnd()

    glDeleteTextures(1, [tex_id])
    glDisable(GL_BLEND)
    glDisable(GL_TEXTURE_2D)

def draw_circle_filled(cx, cy, radius, color, segments=64):
    glDisable(GL_TEXTURE_2D) # Garante que não tem textura aplicada
    glColor4fv(color)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(cx, cy)
    for i in range(segments + 1):
        ang = 2 * math.pi * i / segments
        glVertex2f(cx + math.cos(ang) * radius, cy + math.sin(ang) * radius)
    glEnd()

# --- FUNÇÃO QUE FALTAVA ---
def draw_volume_bar(x, y, width, height, volume):
    # Fundo da barra (Cinza escuro)
    glDisable(GL_TEXTURE_2D)
    glColor4f(0.2, 0.2, 0.2, 0.8)
    glBegin(GL_QUADS)
    glVertex2f(x, y); glVertex2f(x + width, y)
    glVertex2f(x + width, y + height); glVertex2f(x, y + height)
    glEnd()
    
    # Preenchimento
    if volume > 0.6: glColor4f(0.0, 1.0, 0.0, 0.9)   # Verde
    elif volume > 0.3: glColor4f(1.0, 1.0, 0.0, 0.9) # Amarelo
    else: glColor4f(1.0, 0.2, 0.0, 0.9)              # Vermelho
    
    fill_width = width * volume
    glBegin(GL_QUADS)
    glVertex2f(x, y); glVertex2f(x + fill_width, y)
    glVertex2f(x + fill_width, y + height); glVertex2f(x, y + height)
    glEnd()
    
    # Borda
    glLineWidth(1.0); glColor4f(1.0, 1.0, 1.0, 1.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, y); glVertex2f(x + width, y)
    glVertex2f(x + width, y + height); glVertex2f(x, y + height)
    glEnd()

def draw_procedural_speedometer(x, y, size, speed_val):
    # Garante que estados anteriores não interfiram
    glDisable(GL_TEXTURE_2D)
    
    radius = size / 2.0
    cx = x + radius
    cy = y + radius
    
    # 1. Base do Velocímetro
    draw_circle_filled(cx, cy, radius, (0.8, 0.8, 0.85, 1.0)) # Aro
    draw_circle_filled(cx, cy, radius * 0.92, (0.2, 0.2, 0.2, 1.0)) # Borda interna
    draw_circle_filled(cx, cy, radius * 0.88, (0.05, 0.05, 0.05, 0.9)) # Fundo Preto

    # Escalas
    max_speed_display = 320
    start_angle_deg = 225.0
    end_angle_deg = -45.0
    total_angle = start_angle_deg - end_angle_deg
    
    font_nums = pygame.font.SysFont("Arial", 14, bold=True)
    font_digital = pygame.font.SysFont("Consolas", 18, bold=True)
    
    # 2. Marcadores (Traços)
    glDisable(GL_TEXTURE_2D)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    for v in range(0, max_speed_display + 1, 20):
        ratio = v / max_speed_display
        angle_rad = math.radians(start_angle_deg - (ratio * total_angle))
        cos_a = math.cos(angle_rad)
        sin_a = -math.sin(angle_rad) 
        
        if v % 40 == 0:
            len_tick = radius * 0.15
            glColor3f(1, 1, 1)
        else:
            len_tick = radius * 0.08
            glColor3f(0.7, 0.7, 0.7)
            
        r_out = radius * 0.85
        r_in = r_out - len_tick
        glVertex2f(cx + r_out * cos_a, cy + r_out * sin_a)
        glVertex2f(cx + r_in * cos_a, cy + r_in * sin_a)
    glEnd()
    
    # 3. Números da Borda
    for v in range(0, max_speed_display + 1, 40):
        ratio = v / max_speed_display
        angle_rad = math.radians(start_angle_deg - (ratio * total_angle))
        cos_a = math.cos(angle_rad)
        sin_a = -math.sin(angle_rad)
        r_text = radius * 0.65
        tx = cx + r_text * cos_a - 10
        ty = cy + r_text * sin_a - 10
        draw_text(tx, ty, str(v), font_nums, (255, 255, 255))

    # Texto "km/h"
    draw_text(cx - 15, cy + radius * 0.2, "km/h", font_nums, (200, 200, 200))

    # 4. VISOR DIGITAL
    current_kmh = int(abs(speed_val) * 280)
    
    box_w = radius * 0.5
    box_h = radius * 0.18
    box_x = cx - box_w / 2
    box_y = cy + radius * 0.5
    
    glDisable(GL_TEXTURE_2D)
    glColor3f(0.1, 0.1, 0.15) 
    glBegin(GL_QUADS)
    glVertex2f(box_x, box_y); glVertex2f(box_x + box_w, box_y)
    glVertex2f(box_x + box_w, box_y + box_h); glVertex2f(box_x, box_y + box_h)
    glEnd()
    
    glLineWidth(1.0); glColor3f(0.4, 0.4, 0.4)
    glBegin(GL_LINE_LOOP)
    glVertex2f(box_x, box_y); glVertex2f(box_x + box_w, box_y)
    glVertex2f(box_x + box_w, box_y + box_h); glVertex2f(box_x, box_y + box_h)
    glEnd()
    
    text_speed = str(current_kmh)
    tw, th = font_digital.size(text_speed)
    text_x = box_x + (box_w - tw) / 2
    text_y = box_y + (box_h - th) / 2
    draw_text(text_x, text_y, text_speed, font_digital, (0, 255, 255))

    # 5. PONTEIRO
    pointer_ratio = current_kmh / max_speed_display
    if pointer_ratio > 1.1: pointer_ratio = 1.1
    pointer_angle = start_angle_deg - (pointer_ratio * total_angle)
    
    glDisable(GL_TEXTURE_2D)
    glPushMatrix()
    glTranslatef(cx, cy, 0)
    glRotatef(pointer_angle, 0, 0, -1) 
    
    glColor3f(1.0, 0.2, 0.0)
    glBegin(GL_TRIANGLES)
    w_ptr = radius * 0.04; l_ptr = radius * 0.75
    glVertex2f(0, -w_ptr); glVertex2f(l_ptr, 0); glVertex2f(0, w_ptr)
    glEnd()
    
    draw_circle_filled(0, 0, radius * 0.12, (0.1, 0.1, 0.1, 1.0))
    glPopMatrix()

# --- FUNÇÃO PRINCIPAL DO HUD (CORRIGIDA) ---
# Adicionado o argumento 'music_volume'
def draw_hud(display_size, speed_val, music_volume, current_lap, total_laps):
    width, height = display_size
    
    glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity()
    gluOrtho2D(0, width, height, 0) 
    glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()
    glDisable(GL_LIGHTING); glDisable(GL_DEPTH_TEST)

    font_title = pygame.font.SysFont("Arial", 20, bold=True)
    font_text = pygame.font.SysFont("Consolas", 16)
    
    # --- FONTE GRANDE PARA AS VOLTAS ---
    font_laps = pygame.font.SysFont("Arial", 36, bold=True) 
    
    # Caixa de Comandos (Esquerda)
    glEnable(GL_BLEND)
    glColor4f(0.1, 0.1, 0.1, 0.8)
    glBegin(GL_QUADS)
    glVertex2f(10, 10); glVertex2f(330, 10)
    glVertex2f(330, 240); glVertex2f(10, 240)
    glEnd()
    glDisable(GL_BLEND)

    draw_text(20, 20, "COMANDOS", font_title, (255, 200, 0))
    draw_text(20, 50, "ESPACO: Inicia Animacao", font_text)
    draw_text(20, 70, "SETAS: Movimentam Camera", font_text)
    draw_text(20, 90, "W/A/S/D: Pilotar", font_text)
    draw_text(20, 110, "Z / X: Zoom", font_text)
    draw_text(20, 130, "C: Modo Dia/Noite", font_text)
    draw_text(20, 150, "R: Ativar chuva", font_text)
    draw_text(20, 170, "ESC: Sair", font_text)

    # Volume
    vol_percent = int(music_volume * 100)
    draw_text(20, 200, f"Volume: {vol_percent}%", font_text)
    draw_text(20, 215, "[ - ]   [ + ]", font_text, (150, 150, 150))
    draw_volume_bar(150, 200, 150, 15, music_volume)

    # --- MOSTRADOR DE VOLTAS (CANTO SUPERIOR DIREITO) ---
    lap_text = f"LAP {current_lap}/{total_laps}"
    
    # Desenha um fundo preto semitransparente para destacar o texto
    text_w, text_h = font_laps.size(lap_text)
    box_x = width - text_w - 30
    box_y = 10
    
    glEnable(GL_BLEND)
    glColor4f(0.0, 0.0, 0.0, 0.6) # Fundo preto
    glBegin(GL_QUADS)
    glVertex2f(box_x - 10, box_y - 5); glVertex2f(width - 10, box_y - 5)
    glVertex2f(width - 10, box_y + text_h + 5); glVertex2f(box_x - 10, box_y + text_h + 5)
    glEnd()
    glDisable(GL_BLEND)

    # Desenha o texto em Amarelo Ouro
    draw_text(box_x, box_y, lap_text, font_laps, (255, 215, 0))

    # Velocímetro (Inferior Direito)
    size = 220
    pos_x = width - size - 20
    pos_y = height - size - 20
    glDisable(GL_TEXTURE_2D)
    draw_procedural_speedometer(pos_x, pos_y, size, speed_val)

    glEnable(GL_DEPTH_TEST); glEnable(GL_LIGHTING)
    glMatrixMode(GL_PROJECTION); glPopMatrix()
    glMatrixMode(GL_MODELVIEW); glPopMatrix()