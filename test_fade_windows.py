import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Cài đặt các kích thước cửa sổ
window_sizes = [(800, 600), (600, 400)]  # Kích thước của hai cửa sổ
current_window_index = 0

# Tạo màn hình đầu tiên
screen = pygame.display.set_mode(window_sizes[current_window_index])
pygame.display.set_caption("Window 1")

# Màu sắc và vị trí nút
button_color = (0, 128, 255)
button_hover_color = (0, 200, 255)
button_rect = pygame.Rect(350, 250, 100, 50)

# Thiết lập phông chữ cho văn bản nút
font = pygame.font.Font(None, 36)
button_text = font.render("Switch", True, (255, 255, 255))

# Hàm hiệu ứng phóng to từ giữa
def zoom_in_transition(new_size):
    global screen
    new_surface = pygame.Surface(new_size)
    new_surface.fill((30, 30, 30))  # Màu nền của cửa sổ mới
    
    clock = pygame.time.Clock()
    
    # Bắt đầu với kích thước nhỏ và tăng dần
    scale = 0.1  # Bắt đầu từ 10% kích thước
    done = False
    while not done:
        # Xóa màn hình
        screen.fill((0, 0, 0))
        
        # Tính toán kích thước và vị trí để phóng to từ giữa
        width = int(new_size[0] * scale)
        height = int(new_size[1] * scale)
        x = (screen.get_width() - width) // 2
        y = (screen.get_height() - height) // 2
        
        # Vẽ cửa sổ mới ở kích thước tạm thời
        scaled_surface = pygame.transform.scale(new_surface, (width, height))
        screen.blit(scaled_surface, (x, y))
        
        pygame.display.flip()
        
        # Tăng scale để phóng to
        scale += 0.05
        if scale >= 1.0:
            done = True
        
        clock.tick(60)
    
    # Đặt màn hình với kích thước đầy đủ sau khi hoàn tất
    screen = pygame.display.set_mode(new_size)
    screen.blit(new_surface, (0, 0))
    pygame.display.flip()

# Hàm chuyển đổi cửa sổ với hiệu ứng phóng to
def switch_window():
    global current_window_index
    # Tăng chỉ số cửa sổ
    current_window_index = (current_window_index + 1) % len(window_sizes)
    # Gọi hàm hiệu ứng phóng to với kích thước cửa sổ mới
    zoom_in_transition(window_sizes[current_window_index])

# Vòng lặp chính
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                switch_window()

    # Lấy vị trí chuột
    mouse_pos = pygame.mouse.get_pos()

    # Vẽ nền (màu xám)
    screen.fill((30, 30, 30))

    # Kiểm tra nếu chuột đang trên nút và đổi màu khi hover
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, button_hover_color, button_rect)
    else:
        pygame.draw.rect(screen, button_color, button_rect)

    # Vẽ văn bản lên nút
    screen.blit(button_text, (button_rect.x + 10, button_rect.y + 10))

    # Cập nhật hiển thị
    pygame.display.flip()
    clock.tick(60)

# Thoát Pygame
pygame.quit()
sys.exit()
