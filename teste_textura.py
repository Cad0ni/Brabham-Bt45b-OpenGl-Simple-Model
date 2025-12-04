import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import os

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    # Configuração básica de câmera 2D
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    
    # Habilita texturas
    glEnable(GL_TEXTURE_2D)
    
    # --- DEBUG DO CAMINHO ---
    print(f"Diretório atual de trabalho: {os.getcwd()}")
    filename = "asphalt.png"
    
    if not os.path.exists(filename):
        print(f"ERRO CRÍTICO: O arquivo '{filename}' NÃO foi encontrado nesta pasta!")
        print("Certifique-se de que a imagem está na mesma pasta deste script.")
        pygame.quit()
        return

    # --- CARREGAMENTO SIMPLES ---
    try:
        textureSurface = pygame.image.load(filename)
        textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
        width = textureSurface.get_width()
        height = textureSurface.get_height()

        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        
        print("Sucesso: Imagem carregada no OpenGL.")

    except Exception as e:
        print(f"Erro ao carregar imagem: {e}")
        return

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # IMPORTANTE: Cor branca para a textura aparecer
        glColor3f(1, 1, 1)
        
        glBindTexture(GL_TEXTURE_2D, texid)
        
        # Desenha um quadrado gigante com a textura
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(100, 100)
        glTexCoord2f(1, 0); glVertex2f(700, 100)
        glTexCoord2f(1, 1); glVertex2f(700, 500)
        glTexCoord2f(0, 1); glVertex2f(100, 500)
        glEnd()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()