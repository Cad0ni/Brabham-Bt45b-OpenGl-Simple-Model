import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Importa os módulos do projeto
import config
import utils
import drawing
import logic
import car
import interface
import particles
import audio 

def main():
    # --- 1. INICIALIZAÇÃO ---
    pygame.init()
    display_size = (1280, 720)
    
    pygame.display.set_mode(display_size, DOUBLEBUF | OPENGL | HWPALETTE | HWSURFACE)
    pygame.display.set_caption("F1 Brabham BT45B - Grand Prix Final")
    
    clock = pygame.time.Clock()
    
    # --- 2. CONFIGURAÇÕES GRÁFICAS ---
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING); glEnable(GL_LIGHT0); glEnable(GL_NORMALIZE)
    glLightfv(GL_LIGHT0, GL_POSITION, (0.5, 1.0, 0.5, 0.0)) 
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.5, 0.5, 0.5, 1.0)) 
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glMaterialf(GL_FRONT, GL_SHININESS, 32.0)
    
    # --- 3. CARREGAMENTO DE ASSETS ---
    print("--- Carregando Texturas ---")
    config.tire_tread_texture_id = utils.load_texture("texture2.jpg")
    config.sidewall_texture_id = utils.load_texture("sidewall.png")
    config.asphalt_texture_id = utils.load_texture("asphalt.jpg")
    config.grass_texture_id = utils.load_texture("grass.jpeg")
    config.leaves_texture_id = utils.load_texture("leaves.png")
    config.logo_texture_id = utils.load_texture("martiniRacing.png")
    config.wing_logo_texture_id = utils.load_texture("MartiniLogo.png")

    # --- 4. OTIMIZAÇÃO DE CENÁRIO ---
    scenery_list_id = glGenLists(1)
    def compile_scenery():
        glNewList(scenery_list_id, GL_COMPILE)
        drawing.draw_circuit_and_environment() 
        glEndList()
        print("Cenário recompilado.")
    print("Gerando geometria inicial...")
    compile_scenery()

    # --- 5. SISTEMAS ---
    smoke_system = particles.SmokeSystem()
    rain_system = particles.RainSystem()
    rain_system.initialize()
    confetti_system = particles.ConfettiSystem()

    # --- ÁUDIO (CORRIGIDO) ---
    sound_manager = audio.SoundManager()
    sound_manager.load_sounds() 
    
    # AGORA SIM: Toca a música explicitamente antes do loop começar
    sound_manager.start_background_music() 
    # -------------------------

    cam_rot_x, cam_rot_y = 15.0, 180.0
    camera_height, camera_distance = 5.0, 18.0
    
    # --- 6. LOOP PRINCIPAL ---
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); quit()
            
            if event.type == pygame.KEYDOWN:
                # LARGADA / RESET
                if event.key == pygame.K_SPACE:
                    config.animation_active = not config.animation_active
                    if config.animation_active:
                        config.car_pos = [40.0, 0.2, 0.0]
                        config.car_rot_y = 0.0
                        config.animation_state = 1
                        config.start_timer = 0.0 
                        config.animation_progress = 0.0
                        config.start_sound_played = False
                        
                        config.current_lap = 1 
                        config.victory_mode = False
                        config.victory_sound_played = False
                        
                        # Retoma a música caso tenha parado na vitória
                        try: pygame.mixer.music.play(-1)
                        except: pass
                        
                    else:
                        config.car_speed = 0.0
                        config.animation_state = 0
                        config.victory_mode = False
                
                if event.key == pygame.K_c: config.is_day = not config.is_day
                if event.key == pygame.K_r:
                    config.is_raining = not config.is_raining
                    compile_scenery() 
                    sound_manager.update_rain_sound(config.is_raining)
                if event.key == pygame.K_ESCAPE: pygame.quit(); quit()
        
        # Clima
        if config.is_raining:
            if config.is_day: 
                glClearColor(0.25, 0.25, 0.3, 1.0) 
                glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.35, 1.0))
                glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.6, 0.6, 0.65, 1.0))
            else: 
                glClearColor(0.02, 0.02, 0.05, 1.0) 
                glLightfv(GL_LIGHT0, GL_AMBIENT, (0.05, 0.05, 0.05, 1.0))
                glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.1, 0.1, 0.15, 1.0))
        elif config.is_day: 
            glClearColor(0.5, 0.7, 1.0, 1.0) 
            glLightfv(GL_LIGHT0, GL_AMBIENT, (0.4, 0.4, 0.4, 1.0))
            glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.9, 0.9, 0.9, 1.0))
        else: 
            glClearColor(0.05, 0.05, 0.15, 1.0)
            glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.15, 1.0))
            glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.2, 0.2, 0.35, 1.0))

        # Updates
        keys = pygame.key.get_pressed()
        logic.update_game_state(keys)
        
        # Efeitos
        if config.animation_active:
            if config.start_timer >= 2.0 and not config.start_sound_played:
                sound_manager.play_start_signal()
                config.start_sound_played = True 

        if config.victory_mode:
            if not config.victory_sound_played:
                sound_manager.play_victory()
                config.victory_sound_played = True
            confetti_system.update()

        # Volume
        if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]: 
            config.music_volume = max(0.0, config.music_volume - 0.01)
            sound_manager.set_music_volume(config.music_volume)
        if keys[pygame.K_EQUALS] or keys[pygame.K_PLUS] or keys[pygame.K_KP_PLUS]:
            config.music_volume = min(1.0, config.music_volume + 0.01)
            sound_manager.set_music_volume(config.music_volume)

        # Partículas
        rain_system.update()
        if abs(config.car_speed) > 0.1 and abs(config.front_wheel_steer_angle) > 5.0:
            smoke_system.add_smoke(config.car_pos[0], config.car_pos[1], config.car_pos[2], config.car_rot_y)
        smoke_system.update()

        # Áudio do Motor
        manual_accel = keys[pygame.K_w]
        auto_accel = config.animation_active and config.start_timer > 2.0
        is_accelerating = manual_accel or auto_accel
        sound_manager.update(config.car_speed, config.front_wheel_steer_angle, is_accelerating)

        # Câmera
        if keys[pygame.K_z]: camera_distance -= 0.4; camera_height -= 0.15
        if keys[pygame.K_x]: camera_distance += 0.4; camera_height += 0.15
        camera_distance = max(5.0, min(18.0, camera_distance))
        camera_height = max(1.2, min(5.0, camera_height))
        if camera_height < 2.0: cam_rot_x = 10.0 
        else: cam_rot_x = 15.0

        if keys[pygame.K_LEFT]: cam_rot_y -= 2.0
        if keys[pygame.K_RIGHT]: cam_rot_y += 2.0
        if keys[pygame.K_UP]: cam_rot_x = max(5.0, cam_rot_x - 2.0)
        if keys[pygame.K_DOWN]: cam_rot_x = min(85.0, cam_rot_x + 2.0)

        # Renderização
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION); glLoadIdentity()
        gluPerspective(config.camera_fov, (display_size[0] / display_size[1]), 1.0, 1500.0)
        glMatrixMode(GL_MODELVIEW); glLoadIdentity()
        
        glTranslatef(0.0, -camera_height, -camera_distance)
        glRotatef(cam_rot_x, 1, 0, 0)
        glRotatef(cam_rot_y - config.car_rot_y, 0, 1, 0) 
        glTranslatef(-config.car_pos[0], -config.car_pos[1], -config.car_pos[2])
        
        glCallList(scenery_list_id)
        drawing.draw_all_lampposts()
        drawing.draw_starting_gantry(40, 10, angle=0)
        
        glPushMatrix()
        glTranslatef(config.car_pos[0], config.car_pos[1], config.car_pos[2])
        glRotatef(config.car_rot_y, 0, 1, 0)
        car.draw_complete_car()
        glPopMatrix()
        
        smoke_system.draw()
        rain_system.draw()
        confetti_system.draw()
        
        interface.draw_hud(display_size, config.car_speed, config.music_volume, config.current_lap, config.total_laps)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()