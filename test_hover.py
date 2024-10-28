import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Cài đặt màn hình
screen = pygame.display.set_mode((800, 600))

# Tải hình ảnh nút và bức ảnh hiển thị khi hover
button_image = pygame.image.load(r"D:\Artificial Intelligent Foudation\Project 1 - Search\images\buttons\home_button.png")  # Thay đổi đường dẫn theo ảnh của bạn
button_rect = button_image.get_rect(topleft=(100, 100))

hover_image = pygame.image.load(r"D:\Artificial Intelligent Foudation\Project 1 - Search\images\player.png")  # Thay đổi đường dẫn theo ảnh của bạn
hover_rect = hover_image.get_rect(center=(400, 300))  # Đặt bức ảnh ở giữa cửa sổ

# Biến để theo dõi trạng thái hiển thị của bức ảnh
show_hover_image = False

# Vòng lặp chính
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Lấy vị trí của chuột
    mouse_pos = pygame.mouse.get_pos()

    # Kiểm tra hover trên nút
    if button_rect.collidepoint(mouse_pos):
        show_hover_image = True
    else:
        # Kiểm tra nếu chuột đang ở trên bức ảnh hover
        if hover_rect.collidepoint(mouse_pos):
            show_hover_image = True
        else:
            show_hover_image = False

    # Vẽ lên màn hình
    screen.fill((255, 255, 255))  # Màu nền
    screen.blit(button_image, button_rect)  # Vẽ nút

    # Vẽ bức ảnh nếu cần
    if show_hover_image:
        screen.blit(hover_image, hover_rect)

    pygame.display.flip()

# Thoát Pygame
pygame.quit()
sys.exit()
