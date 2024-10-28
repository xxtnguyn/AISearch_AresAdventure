import pygame
import sys


# Màu sắc
background_color = (30, 30, 30)
wave_color = (0, 128, 255)

# Hàm vẽ hiệu ứng sóng
def draw_waves(screen, waves):
    for wave in waves:
        pos, radius = wave
        # Vẽ vòng tròn với độ dày 2 để tạo sóng
        pygame.draw.circle(screen, wave_color, pos, radius, 2)
