import pygame
import sys
import math

# Khởi tạo Pygame
pygame.init()

# Cài đặt màn hình
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Text Bounce Effect")

# Thiết lập phông chữ và chuỗi văn bản
font_path = r"D:\Artificial Intelligent Foudation\Project 1 - Search\fonts\BothWays.ttf"  # Thay bằng đường dẫn đến font của bạn
font_size = 60
font = pygame.font.Font(font_path, font_size)

text = "Santa's Giftgiving Adventure"
text_color = (255, 255, 255)  # Màu trắng
amplitude = 10  # Biên độ dao động
frequency = 0.005  # Tần số dao động

# Tính toán vị trí ban đầu của mỗi chữ cái để nó được căn giữa
text_surfaces = [font.render(char, True, text_color) for char in text]
total_text_width = sum(surface.get_width() for surface in text_surfaces)
start_x = (screen_width - total_text_width) // 2
char_positions = [(start_x + sum(surface.get_width() for surface in text_surfaces[:i]), screen_height // 2) for i in range(len(text))]

# Vòng lặp chính
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Vẽ nền (màu đen)
    screen.fill((0, 0, 0))

    # Vẽ từng chữ cái với hiệu ứng di chuyển lên xuống
    for i, (surface, (x, y)) in enumerate(zip(text_surfaces, char_positions)):
        offset_y = amplitude * math.sin(frequency * (pygame.time.get_ticks() + i * 100))  # Tính độ lệch y cho mỗi chữ cái
        screen.blit(surface, (x, y + offset_y))

    # Cập nhật hiển thị
    pygame.display.flip()
    clock.tick(60)  # Điều chỉnh tốc độ khung hình

# Thoát Pygame
pygame.quit()
sys.exit()
