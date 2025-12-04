# ==========================================================
# ARQUIVO DE CONFIGURAÇÃO E ESTADO GLOBAL
# ==========================================================

# --- ESTADO DO CARRO ---
car_pos = [35.0, 0.2, 0.0]  # Posição X, Y, Z
car_rot_y = 0.0            # Rotação do chassi
car_speed = 0.0            # Velocidade atual
front_wheel_steer_angle = 0.0 # Ângulo das rodas da frente
wheel_rotation_angle = 0.0    # Animação de giro das rodas

# --- CÂMERA ---
camera_fov = 45.0

# --- TEXTURAS (IDs gerados pelo OpenGL) ---
tire_tread_texture_id = None
sidewall_texture_id = None
asphalt_texture_id = None
grass_texture_id = None
leaves_texture_id = None
logo_texture_id = None # Textura da Martini Racing
wing_logo_texture_id = None

# --- CONTROLE DE ANIMAÇÃO (LARGADA) ---
animation_active = False # Se a cutscene está rodando
animation_state = 0      # 0=Parado, 1=Esperando Luz, 2=Acelerando
start_timer = 0.0        # Temporizador do semáforo
animation_progress = 0.0 # Progresso na curva automática

# --- AMBIENTE E CLIMA ---
is_day = True        # True = Dia, False = Noite
is_raining = False   # True = Chuva, False = Limpo

# --- ÁUDIO (A VARIÁVEL QUE FALTAVA) ---
music_volume = 0.3   # Volume da música (0.0 a 1.0)
start_sound_played = False # Controle para o som não repetir


# --- SISTEMA DE VOLTAS ---
current_lap = 1
total_laps = 3

victory_mode = False       # Se o show de vitória está ativo
victory_sound_played = False # Para tocar o som só uma vez



