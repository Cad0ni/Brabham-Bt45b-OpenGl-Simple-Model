import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import os
import sys

def load_texture(filename):
    """
    Carrega uma imagem como textura OpenGL.
    Usa caminhos absolutos baseados na localização do script para evitar erros
    quando se move a pasta do projeto.
    """
    # 1. Descobre o caminho da pasta onde este arquivo (utils.py) está
    if getattr(sys, 'frozen', False):
        # Se for um executável (futuro)
        base_path = os.path.dirname(sys.executable)
    else:
        # Se estiver rodando o script .py
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Cria o caminho completo para a imagem
    full_path = os.path.join(base_path, filename)

    print(f"Tentando carregar: {full_path}") # Debug para você ver onde ele está procurando

    if not os.path.exists(full_path):
        print(f"ERRO: Arquivo '{filename}' nao encontrado no caminho: {full_path}")
        print("Verifique se o nome do arquivo e a extensao (.jpg/.png) estao corretos.")
        return None

    try:
        # 3. Carrega a imagem usando o caminho completo
        surface = pygame.image.load(full_path).convert_alpha()
        
        # Redimensiona para garantir compatibilidade (Potência de 2)
        surface = pygame.transform.scale(surface, (512, 512))
        
        image_width, image_height = surface.get_size()
        img_data = pygame.image.tostring(surface, "RGBA", True)

        # Gera textura OpenGL
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR) 
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) 
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        
        gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA, image_width, image_height, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        
        print(f"Sucesso: Textura '{filename}' carregada.")
        return texture_id

    except Exception as e:
        print(f"ERRO CRITICO ao processar textura '{filename}': {e}")
        return None