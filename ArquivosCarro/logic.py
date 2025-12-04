import pygame
import math
import config

def update_game_state(keys):
    # ========================================================================
    # 1. MODO MANUAL (WASD) - Se a animação NÃO estiver ativa
    # ========================================================================
    if not config.animation_active:
        # Aceleração
        if keys[pygame.K_w]: config.car_speed += 0.01 
        elif keys[pygame.K_s]: config.car_speed -= 0.02 
        else: config.car_speed *= 0.98

        config.car_speed = max(-0.2, min(1.2, config.car_speed))

        # Direção
        if abs(config.car_speed) > 0.01:
            turn_speed = 3.0 
            if keys[pygame.K_a]: 
                config.car_rot_y += turn_speed
                config.front_wheel_steer_angle = min(35, config.front_wheel_steer_angle + 5)
            elif keys[pygame.K_d]: 
                config.car_rot_y -= turn_speed
                config.front_wheel_steer_angle = max(-35, config.front_wheel_steer_angle - 5)
            else:
                # Retorno automático do volante
                if config.front_wheel_steer_angle > 0: config.front_wheel_steer_angle -= 5
                if config.front_wheel_steer_angle < 0: config.front_wheel_steer_angle += 5

        # Atualiza Posição (Sem Colisão, Movimento Livre)
        move_step = config.car_speed * 2.5 
        rad = math.radians(config.car_rot_y)
        config.car_pos[0] += math.sin(rad) * move_step
        config.car_pos[2] += math.cos(rad) * move_step

    # ========================================================================
    # 2. MODO AUTOMÁTICO - CORRIDA E VOLTAS
    # ========================================================================
    else:
        # Avança o tempo do semáforo
        config.start_timer += 0.016 
        
        # Timings
        green_light_time = 2.0    
        reaction_delay = 0.3      
        start_moving_time = green_light_time + reaction_delay 
        
        # Posição onde o carro começa na lógica matemática (Z=10)
        start_line_progress = 85.0

        # --- FASE 1: ESPERANDO NO GRID ---
        if config.start_timer < start_moving_time:
            config.car_speed = 0.0
            config.animation_progress = start_line_progress
            
            # Trava posição
            config.car_pos[0] = 40.0 
            config.car_pos[2] = 10.0 
            config.car_rot_y = 0.0
            config.front_wheel_steer_angle = 0.0
            
        # --- FASE 2: CORRENDO ---
        else:
            target_speed = 0.95
            acceleration_rate = 0.005 
            
            if config.car_speed < target_speed:
                config.car_speed += acceleration_rate
            
            step_distance = config.car_speed * 2.5
            config.animation_progress += step_distance

        # --- CÁLCULO DE VOLTAS ---
        R = 40.0; L = 150.0 
        half_L = L / 2.0
        curve_len = math.pi * R
        perimeter = (2 * L) + (2 * curve_len) # Perímetro total da pista
        
        # Calcula voltas baseado na distância percorrida
        distance_run = config.animation_progress - start_line_progress
        calculated_lap = 1 + int(distance_run / perimeter)
        
        # Verifica Vitória
        if calculated_lap > config.total_laps:
            # ACABOU A CORRIDA
            config.current_lap = config.total_laps
            config.animation_active = False # Sai do modo automático
            config.car_speed = 0.0
            
            # Ativa o modo de vitória (Confetes e Som)
            config.victory_mode = True
            print("VITÓRIA! Corrida finalizada.")
        else:
            config.current_lap = calculated_lap

        # --- MATEMÁTICA DA PISTA (Loop Infinito) ---
        dist = config.animation_progress % perimeter
        
        # 1. RETA DIREITA
        if dist < L:
            z_pos = -half_L + dist
            # Desvio (Chicane)
            if 10.0 < z_pos < 60.0 and config.car_speed > 0.5:
                ratio = (z_pos - 10.0) / 50.0
                offset = math.sin(ratio * math.pi) * 4.0 
                config.car_pos[0] = R - offset
                config.front_wheel_steer_angle = -15.0 if ratio < 0.5 else 15.0
                config.car_rot_y = 5.0 if ratio < 0.5 else -5.0
            else:
                config.car_pos[0] = R; config.front_wheel_steer_angle = 0.0; config.car_rot_y = 0.0
            config.car_pos[2] = z_pos

        # 2. CURVA FUNDO
        elif dist < (L + curve_len):
            ratio = (dist - L) / curve_len
            angle = ratio * math.pi
            config.car_pos[0] = R * math.cos(angle)
            config.car_pos[2] = half_L + (R * math.sin(angle))
            config.car_rot_y = -(ratio * 180.0)
            config.front_wheel_steer_angle = -30.0

        # 3. RETA ESQUERDA
        elif dist < (2 * L + curve_len):
            z_pos = half_L - (dist - (L + curve_len))
            # Desvio 2
            if -30.0 < z_pos < 10.0:
                ratio = (10.0 - z_pos) / 40.0
                offset = math.sin(ratio * math.pi) * 4.0
                config.car_pos[0] = -R + offset
                config.front_wheel_steer_angle = -15.0 if ratio < 0.5 else 15.0
                config.car_rot_y = -185.0 if ratio < 0.5 else -175.0
            else:
                config.car_pos[0] = -R; config.front_wheel_steer_angle = 0.0; config.car_rot_y = -180.0
            config.car_pos[2] = z_pos

        # 4. CURVA FRENTE
        else:
            ratio = (dist - (2 * L + curve_len)) / curve_len
            angle = ratio * math.pi
            config.car_pos[0] = -R * math.cos(angle)
            config.car_pos[2] = -half_L - (R * math.sin(angle))
            config.car_rot_y = -180.0 - (ratio * 180.0)
            config.front_wheel_steer_angle = -30.0

    # ========================================================================
    # 3. ANIMAÇÃO DAS RODAS (VELOCIDADE ALTA)
    # ========================================================================
    if abs(config.car_speed) > 0.01:
        # Multiplicador 60.0 para rotação muito rápida
        rotation_speed = config.car_speed * 60.0 
        config.wheel_rotation_angle += rotation_speed