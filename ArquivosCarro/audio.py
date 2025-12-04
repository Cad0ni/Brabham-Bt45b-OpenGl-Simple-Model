import pygame
import os

class SoundManager:
    def __init__(self):
        try:
            pygame.mixer.init() 
            self.initialized = True
        except:
            print("Erro ao inicializar sistema de som.")
            self.initialized = False
            return

        pygame.mixer.set_num_channels(8)
        self.channel_engine = pygame.mixer.Channel(0)
        self.channel_skid   = pygame.mixer.Channel(1)
        self.channel_sfx    = pygame.mixer.Channel(2)
        self.channel_rain   = pygame.mixer.Channel(3)

        self.snd_engine = None
        self.snd_skid = None
        self.snd_start = None
        self.snd_rain = None
        self.snd_victory = None 

    def load_sounds(self):
        if not self.initialized: return
        
        base_path = os.path.dirname(os.path.abspath(__file__))
        def get_path(filename): return os.path.join(base_path, filename)

        print("--- Carregando Sons ---")

        # 1. MÚSICA (Apenas carrega, não toca ainda)
        music_file = get_path("music.mp3")
        if os.path.exists(music_file):
            try:
                pygame.mixer.music.load(music_file)
                print("Música carregada na memória.")
            except Exception as e: 
                print(f"Erro ao carregar música: {e}")

        # 2. MOTOR
        self.snd_engine = self._load_any(get_path("engine"))
        if self.snd_engine:
            self.snd_engine.set_volume(1.0) 
            self.channel_engine.set_volume(0.0) 
            self.channel_engine.play(self.snd_engine, loops=-1)
        else:
            print("Aviso: Som do motor não encontrado.")

        # 3. DERRAPAGEM
        self.snd_skid = self._load_any(get_path("skid"))
        if self.snd_skid: self.snd_skid.set_volume(0.5)

        # 4. LARGADA
        self.snd_start = self._load_any(get_path("start"))
        if self.snd_start: self.snd_start.set_volume(1.0) 

        # 5. CHUVA
        self.snd_rain = self._load_any(get_path("rain"))
        if self.snd_rain: self.snd_rain.set_volume(0.7)

        # 6. VITÓRIA
        self.snd_victory = self._load_any(get_path("victory"))
        if self.snd_victory:
            self.snd_victory.set_volume(1.0)

    def _load_any(self, path_no_ext):
        if os.path.exists(path_no_ext + ".wav"): return pygame.mixer.Sound(path_no_ext + ".wav")
        elif os.path.exists(path_no_ext + ".mp3"): return pygame.mixer.Sound(path_no_ext + ".mp3")
        return None

    # --- NOVO MÉTODO: INICIA A MÚSICA ---
    def start_background_music(self):
        if not self.initialized: return
        try:
            # Volume inicial 0.3
            pygame.mixer.music.set_volume(0.3)
            # Play em loop (-1)
            pygame.mixer.music.play(-1)
            print("Música de fundo iniciada!")
        except:
            print("Não foi possível iniciar a música.")

    def play_start_signal(self):
        if self.snd_start: self.channel_sfx.play(self.snd_start)

    def play_victory(self):
        if self.snd_victory:
            pygame.mixer.music.fadeout(500) 
            self.channel_sfx.play(self.snd_victory)

    def update_rain_sound(self, is_raining):
        if not self.snd_rain: return
        if is_raining:
            if not self.channel_rain.get_busy():
                self.channel_rain.play(self.snd_rain, loops=-1, fade_ms=2000)
        else:
            if self.channel_rain.get_busy():
                self.channel_rain.fadeout(2000)

    def set_music_volume(self, volume):
        if self.initialized: pygame.mixer.music.set_volume(volume)

    def update(self, speed, steering_angle, is_accelerating):
        if not self.initialized: return

        if self.snd_engine:
            speed_abs = abs(speed)
            target_vol = 0.0
            if is_accelerating:
                target_vol = 0.2 + (speed_abs * 0.8)
            else:
                target_vol = speed_abs * 0.5
            
            self.channel_engine.set_volume(max(0.0, min(target_vol, 1.0)))
            
            if not self.channel_engine.get_busy():
                self.channel_engine.play(self.snd_engine, loops=-1)

        if self.snd_skid:
            is_fast = abs(speed) > 0.3
            is_turning = abs(steering_angle) > 15.0
            if is_fast and is_turning:
                if not self.channel_skid.get_busy(): self.channel_skid.play(self.snd_skid)
            else:
                if self.channel_skid.get_busy(): self.channel_skid.fadeout(300)