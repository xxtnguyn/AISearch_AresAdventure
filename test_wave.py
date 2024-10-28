import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Cài đặt cửa sổ
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Wave Effect on Click")

# Màu sắc
background_color = (30, 30, 30)
wave_color = (0, 128, 255)

# Danh sách chứa các sóng (mỗi sóng có vị trí và bán kính)
waves = []

# Hàm vẽ hiệu ứng sóng
def draw_waves():
    for wave in waves:
        pos, radius = wave
        # Vẽ vòng tròn với độ dày 2 để tạo sóng
        pygame.draw.circle(screen, wave_color, pos, radius, 2)

# Vòng lặp chính
running = True
clock = pygame.time.Clock()
while running:
    # Xóa màn hình với màu nền
    screen.fill(background_color)

    # Kiểm tra sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Khi nhấp chuột, thêm sóng mới vào danh sách
            mouse_pos = event.pos
            waves.append([mouse_pos, 0])  # Bán kính ban đầu là 0

    # Cập nhật các sóng
    for wave in waves:
        wave[1] += 1  # Tăng bán kính để tạo hiệu ứng lan rộng

    # Loại bỏ các sóng có bán kính quá lớn (để tránh danh sách quá dài)
    waves = [wave for wave in waves if wave[1] < 20]

    # Vẽ các sóng
    draw_waves()

    # Cập nhật hiển thị
    pygame.display.flip()
    clock.tick(60)

# Thoát Pygame
pygame.quit()
sys.exit()
