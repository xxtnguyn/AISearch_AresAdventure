import pygame
import sys
import os
from waves_draw import draw_waves
from PATHS import BACKGROUND_PATH, LEVELS_PATH, SOUNDS_PATH


pygame.mixer.init()


# Hàm hiệu ứng phóng to từ giữa
def Window2(new_size):

    waves = []

    background_image = pygame.image.load(os.path.join(BACKGROUND_PATH, "level_background.jpg"))
    background_image = pygame.transform.smoothscale(background_image, (800, 600))

    # Tải hình ảnh nút màn chơi
    level_images = []
    for i in range(1, 17):  # Tải 16 hình ảnh
        level_image = pygame.image.load(os.path.join(LEVELS_PATH, f"level{i}.png"))
        level_image = pygame.transform.smoothscale(level_image, (120, 120))  # Thay đổi kích thước hình ảnh
        level_images.append(level_image)

    # Kích thước nút và ma trận
    button_width = 120
    button_height = 120
    rows = 4
    cols = 4
    buttons = []

    clicked_button_music = pygame.mixer.Sound(os.path.join(SOUNDS_PATH,"clicked_button_sound.mp3"))  # Thay đổi đường dẫn theo file nhạc của bạn
    clicked_button_music.set_volume(0.3)

    # Tạo danh sách các nút
    for row in range(rows):
        for col in range(cols):
            button_rect = pygame.Rect(
                (new_size[0] // 2 - (cols * (button_width + 10)) // 2) + col * (button_width + 10),  # X
                row * (button_height + 10) + 50,  # Y
                button_width,                       # Width
                button_height                       # Height
            )
            buttons.append(button_rect)

    # Tạo cửa sổ mới với kích thước đã cho
    screen = pygame.display.set_mode(new_size)
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

    # Vòng lặp chính
    running = True
    while running:
        cursor_changed = False 


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                waves.append([mouse_pos, 0])
                
                for i in range(0, 16):
                    if buttons[i].collidepoint(event.pos):
                        clicked_button_music.play()
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        from window3 import Window3
                        Window3(i + 1)

        # Vẽ bức ảnh nền
        # screen.blit(new_surface, (0, 0))
        screen.blit(background_image, (0, 0))  # Vẽ bức ảnh nền

        # vẽ sóng
        # Cập nhật các sóng
        for wave in waves:
            wave[1] += 1  # Tăng bán kính để tạo hiệu ứng lan rộng

        # Loại bỏ các sóng có bán kính quá lớn (để tránh danh sách quá dài)
        waves = [wave for wave in waves if wave[1] < 20]


        # Vẽ các nút với hình ảnh level
        for index, button in enumerate(buttons): 
            # Vẽ hình ảnh level vào nút
            if index < len(level_images):  # Kiểm tra xem có đủ hình ảnh
                level_rect = level_images[index].get_rect(center=button.center)
                screen.blit(level_images[index], level_rect)

        for button in buttons:
            if button.collidepoint(pygame.mouse.get_pos()):
                cursor_changed = True
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Con trỏ hình bàn tay

            if not cursor_changed:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        draw_waves(screen, waves)

        pygame.display.flip()
        pygame.time.delay(20)

    # Thoát Pygame
    pygame.quit()
    sys.exit()
