from OpenGL.GL import *
import random
import math

# Mantendo a correção do import
import config as game_config 

# ==========================================================
# 1. SISTEMA DE FUMAÇA (MANTIDO IGUAL AO ANTERIOR)
# ==========================================================
class SmokeParticle:
    def __init__(self, x, y, z, angle):
        self.x = x; self.y = y; self.z = z
        self.life = 1.0 
        self.size = random.uniform(0.2, 0.4) 
        rad = math.radians(angle + random.uniform(-20, 20))
        speed = random.uniform(0.1, 0.3)
        self.vx = -math.sin(rad) * speed
        self.vz = -math.cos(rad) * speed
        self.vy = random.uniform(0.05, 0.15) 

    def update(self):
        self.x += self.vx; self.y += self.vy; self.z += self.vz
        self.life -= 0.02; self.size += 0.015 

class SmokeSystem:
    def __init__(self):
        self.particles = []

    def add_smoke(self, x, y, z, car_angle):
        for _ in range(3): 
            offset_x = random.uniform(-0.3, 0.3)
            self.particles.append(SmokeParticle(x + offset_x, y, z, car_angle))

    def update(self):
        for p in self.particles: p.update()
        self.particles = [p for p in self.particles if p.life > 0]

    def draw(self):
        if not self.particles: return
        glDisable(GL_LIGHTING); glDisable(GL_TEXTURE_2D)
        glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0.8, 0.8, 0.8, 0.3) 
        glBegin(GL_QUADS)
        for p in self.particles:
            alpha = p.life * 0.4
            glColor4f(0.6, 0.6, 0.6, alpha)
            s = p.size
            glVertex3f(p.x - s, p.y - s, p.z); glVertex3f(p.x + s, p.y - s, p.z)
            glVertex3f(p.x + s, p.y + s, p.z); glVertex3f(p.x - s, p.y + s, p.z)
        glEnd()
        glDisable(GL_BLEND); glEnable(GL_LIGHTING)

# ==========================================================
# 2. SISTEMA DE CHUVA (CONCENTRADA NA PISTA)
# ==========================================================
class RainSystem:
    def __init__(self):
        self.drops = []
        # DIMINUÍDO: De 10.000 para 3.500
        # Como a área é menor, vai parecer que tem MAIS chuva que antes.
        self.max_drops = 3500 
        
    def initialize(self):
        self.drops = []
        for _ in range(self.max_drops):
            self.drops.append(self.reset_drop(initial=True))

    def reset_drop(self, initial=False):
        # --- ÁREA CONCENTRADA ---
        # Antes era -400 a 400. Agora focamos onde o carro anda.
        # A pista tem aprox. 150 de comprimento e 80 de largura total.
        x = random.randint(-150, 150)
        z = random.randint(-150, 150)
        
        # ALTURA: Baixei um pouco para vermos a chuva cair mais perto da câmera
        if initial:
            y = random.randint(0, 80)
        else:
            y = random.randint(50, 90) # Spawna logo acima da visão
        
        speed = random.uniform(3.0, 5.0) 
        return [x, y, z, speed]

    def update(self):
        if not game_config.is_raining:
            return

        for drop in self.drops:
            drop[1] -= drop[3]
            if drop[1] < 0:
                new_drop = self.reset_drop()
                drop[0] = new_drop[0]; drop[1] = new_drop[1]; drop[2] = new_drop[2]; drop[3] = new_drop[3]

    def draw(self):
        if not game_config.is_raining: return
        glDisable(GL_LIGHTING); glDisable(GL_TEXTURE_2D); glEnable(GL_BLEND)
        glColor4f(0.8, 0.85, 1.0, 0.8) 
        glLineWidth(2.0)
        glBegin(GL_LINES)
        for drop in self.drops:
            x, y, z, speed = drop
            glVertex3f(x, y, z); glVertex3f(x, y - 4.0, z) 
        glEnd()
        glLineWidth(1.0)
        glDisable(GL_BLEND); glEnable(GL_LIGHTING)

class ConfettiSystem:
    def __init__(self):
        self.particles = []
        # Gera 500 confetes iniciais
        for _ in range(500):
            self.add_particle(initial=True)

    def add_particle(self, initial=False):
        # Posição aleatória em torno do carro (assumindo que o carro para em Z=0)
        x = random.uniform(-30, 110) # Área da reta de chegada
        z = random.uniform(-50, 50)
        
        if initial: y = random.uniform(0, 50)
        else: y = random.uniform(40, 60) # Nasce no alto
        
        # Cor Aleatória (R, G, B)
        color = (random.random(), random.random(), random.random())
        
        # Velocidade de queda e "balanço" lateral
        speed = random.uniform(0.1, 0.3)
        drift_phase = random.uniform(0, math.pi * 2)
        
        self.particles.append([x, y, z, speed, color, drift_phase])

    def update(self):
        if not game_config.victory_mode: return

        for p in self.particles:
            p[1] -= p[3] # Cai (Y)
            p[5] += 0.1  # Atualiza fase do balanço
            
            # Balanço lateral (Seno) para parecer papel caindo
            p[0] += math.sin(p[5]) * 0.05 
            
            # Se tocar o chão, respawna lá em cima
            if p[1] < 0:
                p[1] = random.uniform(40, 50)
                p[3] = random.uniform(0.1, 0.3)

    def draw(self):
        if not game_config.victory_mode: return

        glDisable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        
        glBegin(GL_QUADS)
        for p in self.particles:
            x, y, z, speed, color, drift = p
            glColor3fv(color) # Cor do confete
            
            # Tamanho do papelzinho
            s = 0.3 
            glVertex3f(x - s, y - s, z)
            glVertex3f(x + s, y - s, z)
            glVertex3f(x + s, y + s, z)
            glVertex3f(x - s, y + s, z)
        glEnd()
        
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)