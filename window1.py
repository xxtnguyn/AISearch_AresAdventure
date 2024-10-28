import pygame
import sys
import math
from window2 import Window2
from waves_draw import draw_waves
from PATHS import BACKGROUND_PATH, BUTTONS_PATH, SOUNDS_PATH, FONTS_PATH
import os

# Khởi tạo Pygame
pygame.init()
pygame.mixer.init()

# Cài đặt màn hình
window_sizes = [(800, 600), (800, 600)]
current_window_index = 0


# Hàm chuyển đổi cửa sổ với hiệu ứng phóng to
def switch_window(background_image):
    global current_window_index
    # Tăng chỉ số cửa sổ
    current_window_index = (current_window_index + 1) % len(window_sizes)
    # Gọi hàm hiệu ứng phóng to với kích thước cửa sổ mới
    Window2((800, 600))


screen = pygame.display.set_mode(window_sizes[current_window_index])


def Window1():
    waves = []

    background_image = pygame.image.load(os.path.join(BACKGROUND_PATH, "background.jpg"))
    background_image = pygame.transform.smoothscale(background_image, (800, 600))

    # Tải hình ảnh
    player_intro_image = pygame.image.load(os.path.join(BACKGROUND_PATH, "player_intro.png"))  # Thay đổi đường dẫn đến bức ảnh của bạn
    player_intro_image_rect = player_intro_image.get_rect(center=(100, 450))  # Đặt vị trí ban đầu của bức ảnh

    # Thiết lập biến điều khiển cho playeer_intro
    direction = 1  # 1: di chuyển từ trái sang phải, -1: di chuyển từ phải sang trái
    speed = 5  # Tốc độ di chuyển
    flip_image = False  # Biến để xác định liệu hình ảnh đã bị lật ngược chưa


    # Tải bức ảnh ở giữa và lấy kích thước gốc
    play_intro_button_image = pygame.image.load(os.path.join(BUTTONS_PATH, "play_button.png"))  # Thay đổi đường dẫn đến bức ảnh của bạn
    play_intro_button_image = pygame.transform.smoothscale(play_intro_button_image, (100, 100))
    play_intro_button_original_size = play_intro_button_image.get_size()
    play_intro_button_scaled_image = pygame.transform.smoothscale(play_intro_button_image, (play_intro_button_original_size[0], play_intro_button_original_size[1]))
    play_button_intro_rect = play_intro_button_scaled_image.get_rect(center=(800 // 2, 600 // 2))

    max_scale = 0.8  # Tỉ lệ phóng to tối đa
    min_scale = 0.7  # Tỉ lệ thu nhỏ tối thiểu
    scale = 1.0  # Tỉ lệ ban đầu
    scale_step = 0.005  # Bước thay đổi tỉ lệ
    scaling_up = True # Biến điều khiển để phóng to hoặc thu nhỏ


    # Tải hình ảnh nút loa
    speaker_on_image = pygame.image.load(os.path.join(BUTTONS_PATH, "speaker_on_button.png"))  # Nút loa bật
    speaker_off_image = pygame.image.load(os.path.join(BUTTONS_PATH, "speaker_off_button.png"))  # Nút loa tắt
    speaker_on_image = pygame.transform.smoothscale(speaker_on_image, (60, 60))
    speaker_off_image = pygame.transform.smoothscale(speaker_off_image, (60, 60))

    speaker_button_rect = speaker_on_image.get_rect(topleft=(650, 50))  # Đặt vị trí nút loa

    # Bật nhạc
    game_music = pygame.mixer.Sound(os.path.join(SOUNDS_PATH,"さりい＿パレット .wav"))  # Thay đổi đường dẫn theo file nhạc của bạn
    clicked_button_music = pygame.mixer.Sound(os.path.join(SOUNDS_PATH,"clicked_button_sound.mp3"))  # Thay đổi đường dẫn theo file nhạc của bạn
    clicked_button_music.set_volume(0.3)

    game_music.play(-1)  # Phát nhạc lặp lại

    # Biến trạng thái âm thanh
    game_music_on = True

    # Set up font
    font_path = os.path.join(FONTS_PATH, "BothWays.ttf")  # Replace with your font file path
    font_size = 60
    font = pygame.font.Font(font_path, font_size)

    # Text and color setup
    text = "Santa's Giftgiving Adventure"
    text_color = (255, 255, 255)  # White color for the main text
    shadow_color = (0, 0, 0)       # Black color for shadow
    shadow_offset = (3, 3)          # Offset for shadow position
    amplitude = 10  # Biên độ dao động
    frequency = 0.005  # Tần số dao động
    # Tính toán vị trí ban đầu của mỗi chữ cái để nó được căn giữa
    text_surfaces = [font.render(char, True, text_color) for char in text]
    total_text_width = sum(surface.get_width() for surface in text_surfaces)
    start_x = (800 - total_text_width) // 2
    char_positions = [(start_x + sum(surface.get_width() for surface in text_surfaces[:i]), 600 // 3.5) for i in range(len(text))]

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

                if speaker_button_rect.collidepoint(event.pos):
                    clicked_button_music.play()
                    if game_music_on:
                        game_music.stop()
                        # pygame.mixer.music.pause()  # Dừng nhạc
                        game_music_on = False
                    else:
                        # pygame.mixer.music.unpause()  # Phát nhạc
                        game_music.play(-1)
                        game_music_on = True
                if play_button_intro_rect.collidepoint(event.pos):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    clicked_button_music.play()

                    switch_window(background_image)

        # vẽ sóng

        # Cập nhật các sóng
        for wave in waves:
            wave[1] += 1  # Tăng bán kính để tạo hiệu ứng lan rộng

        # Loại bỏ các sóng có bán kính quá lớn (để tránh danh sách quá dài)
        waves = [wave for wave in waves if wave[1] < 20]

        # Cập nhật tỉ lệ ảnh
        if scaling_up:
            scale += scale_step
            if scale >= max_scale:
                scale = max_scale
                scaling_up = False  # Đổi hướng sang thu nhỏ
        else:
            scale -= scale_step
            if scale <= min_scale:
                scale = min_scale
                scaling_up = True  # Đổi hướng sang phóng to

        # Thay đổi kích thước bức ảnh
        play_intro_button_scaled_width = int(play_intro_button_original_size[0] * scale)
        play_intro_button_scaled_height = int(play_intro_button_original_size[1] * scale)
        play_intro_button_scaled_image = pygame.transform.smoothscale(play_intro_button_image, (play_intro_button_scaled_width, play_intro_button_scaled_height))

        # Cập nhật vị trí để ảnh luôn ở giữa màn hình
        play_button_intro_rect = play_intro_button_scaled_image.get_rect(center=(800 // 2, 600 // 2))



        # Cập nhật vị trí của bức ảnh
        player_intro_image_rect.x += speed * direction

        # Kiểm tra xem bức ảnh đã đến mép màn hình chưa
        if direction == 1 and player_intro_image_rect.right >= 800:  # Đến mép phải
            direction = -1  # Đổi hướng di chuyển
            flip_image = True  # Đánh dấu rằng hình ảnh sẽ bị lật
        elif direction == -1 and player_intro_image_rect.left <= 0:  # Đến mép trái
            direction = 1  # Đổi hướng di chuyển
            flip_image = True  # Đánh dấu rằng hình ảnh sẽ bị lật

        # Nếu bức ảnh đã được đánh dấu để lật, lật hình ảnh
        if flip_image:
            player_intro_image = pygame.transform.flip(player_intro_image, True, False)  # Lật ngược hình ảnh theo chiều ngang
            flip_image = False  # Đặt lại trạng thái lật


        # Vẽ con trỏ chuột

        if speaker_button_rect.collidepoint(pygame.mouse.get_pos()) or play_button_intro_rect.collidepoint(pygame.mouse.get_pos()):
            cursor_changed = True
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Con trỏ hình bàn tay

        if not cursor_changed:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


        # Vẽ lên màn hình

        screen.blit(background_image, (0, 0))  # Vẽ bức ảnh nền

        screen.blit(play_intro_button_scaled_image, play_button_intro_rect)  # Vẽ nút play

        screen.blit(player_intro_image, player_intro_image_rect)  # Vẽ bức ảnh
        if game_music_on:
            screen.blit(speaker_on_image, speaker_button_rect)  # Vẽ nút loa bật
        else:
            screen.blit(speaker_off_image, speaker_button_rect)  # Vẽ nút loa tắt

        draw_waves(screen, waves)

        for i, (surface, (x, y)) in enumerate(zip(text_surfaces, char_positions)):
            offset_y = amplitude * math.sin(frequency * (pygame.time.get_ticks() + i * 100))  # Tính độ lệch y cho mỗi chữ cái
            screen.blit(surface, (x, y + offset_y))
        pygame.display.flip()
        pygame.time.delay(20)  # Delay để điều chỉnh tốc độ di chuyển

    # Thoát Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    Window1()
