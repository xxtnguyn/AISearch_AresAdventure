import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Cài đặt kích thước màn hình cho cửa sổ chính
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Cửa sổ Chính")

# Màu sắc và phông chữ
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)  # Màu vàng
font = pygame.font.Font(None, 36)

# Nút để mở cửa sổ phụ
main_button_rect = pygame.Rect(300, 250, 200, 50)
main_button_text = font.render("Chọn Thuật Toán", True, WHITE)

# Cấu hình cửa sổ phụ
show_sub_window = False
sub_window_surface = pygame.Surface((400, 300), pygame.SRCALPHA)  # Cửa sổ phụ bán trong suốt
sub_window_rect = sub_window_surface.get_rect(center=(400, 300))

# Các nút trong cửa sổ phụ
algorithm_buttons = [
    {"rect": pygame.Rect(100, 40, 200, 50), "text": "Thuật Toán 1"},
    {"rect": pygame.Rect(100, 100, 200, 50), "text": "Thuật Toán 2"},
    {"rect": pygame.Rect(100, 160, 200, 50), "text": "Thuật Toán 3"},
    {"rect": pygame.Rect(100, 220, 200, 50), "text": "Thuật Toán 4"},
]

# Vòng lặp chính
running = True
while running:
    screen.fill(BLACK)  # Làm mới màn hình chính với màu đen

    # Vẽ nút mở cửa sổ phụ
    pygame.draw.rect(screen, BLUE, main_button_rect)
    screen.blit(main_button_text, (main_button_rect.x + 20, main_button_rect.y + 10))

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if main_button_rect.collidepoint(event.pos) and not show_sub_window:
                show_sub_window = True  # Hiển thị cửa sổ phụ

            # Kiểm tra các nút trong cửa sổ phụ nếu đang hiển thị
            if show_sub_window:
                for i, button in enumerate(algorithm_buttons, 1):
                    button_rect = button["rect"].move(sub_window_rect.topleft)  # Di chuyển button theo sub_window vị trí
                    if button_rect.collidepoint(event.pos):
                        print(f"Thuật Toán {i} được chọn")
                        show_sub_window = False  # Đóng cửa sổ phụ

    # Vẽ cửa sổ phụ nếu cần
    if show_sub_window:
        sub_window_surface.fill(YELLOW)  # Làm cửa sổ phụ màu vàng

        # Vẽ các nút thuật toán trong cửa sổ phụ
        for button in algorithm_buttons:
            pygame.draw.rect(sub_window_surface, BLUE, button["rect"])
            text = font.render(button["text"], True, WHITE)
            sub_window_surface.blit(text, (button["rect"].x + 10, button["rect"].y + 10))

        # Vẽ cửa sổ phụ lên màn hình chính
        screen.blit(sub_window_surface, sub_window_rect)

    pygame.display.flip()  # Cập nhật toàn bộ màn hình sau khi vẽ

pygame.quit()
sys.exit()
