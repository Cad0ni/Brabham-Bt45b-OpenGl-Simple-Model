import pygame
import time
import numpy as np

pygame.init()
try:
    pygame.mixer.init()
    print("Mixer iniciado.")
except:
    print("Falha no mixer.")

# Gera um "BEEP" matemático (onda quadrada)
sample_rate = 44100
duration = 1.0 # 1 segundo
n_samples = int(round(duration * sample_rate))
# Cria array numpy com som
buf = np.random.randint(-32768, 32767, n_samples).astype(np.int16)
sound = pygame.sndarray.make_sound(buf)

print("Tocando ruído de teste...")
sound.play()
time.sleep(1)
print("Fim do teste.")