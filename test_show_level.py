import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Cài đặt cửa sổ
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Chọn Màn Chơi")

# Màu sắc
button_color = (0, 128, 255)
button_hover_color = (0, 255, 255)
text_color = (255, 255, 255)
background_color = (30, 30, 30)

# Kích thước nút và ma trận
button_width = 150
button_height = 100
rows = 6
cols = 4
buttons = []

# Tạo danh sách các nút
for row in range(rows):
    for col in range(cols):
        button_rect = pygame.Rect(
            col * (button_width + 10) + 50,  # X
            row * (button_height + 10) + 50,  # Y
            button_width,                       # Width
            button_height                       # Height
        )
        buttons.append(button_rect)

# Vòng lặp chính
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Xóa màn hình với màu nền
    screen.fill(background_color)

    # Vẽ các nút
    for index, button in enumerate(buttons):
        mouse_pos = pygame.mouse.get_pos()
        if button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover_color, button)  # Màu khi hover
        else:
            pygame.draw.rect(screen, button_color, button)  # Màu bình thường
        
        # Vẽ số thứ tự màn chơi lên nút
        font = pygame.font.Font(None, 36)
        text_surface = font.render(str(index + 1), True, text_color)
        text_rect = text_surface.get_rect(center=button.center)
        screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(60)

# Thoát Pygame
pygame.quit()
sys.exit()
