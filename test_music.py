import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Cài đặt màn hình
screen = pygame.display.set_mode((800, 600))

# Tải hình ảnh nút loa
button_image_on = pygame.image.load(r"D:\Artificial Intelligent Foudation\Project 1 - Search\images\buttons\speaker_on_button.png")  # Nút loa bật
button_image_off = pygame.image.load(r"D:\Artificial Intelligent Foudation\Project 1 - Search\images\buttons\speaker_off_button.png")  # Nút loa tắt
button_image_on = pygame.transform.smoothscale(button_image_on, (50, 50))
button_image_off = pygame.transform.smoothscale(button_image_off, (50, 50))

button_rect = button_image_on.get_rect(topleft=(450, 300))  # Đặt vị trí nút loa

# Bật nhạc
pygame.mixer.music.load(r"D:\Artificial Intelligent Foudation\Project 1 - Search\sounds\さりい＿パレット .wav")  # Thay đổi đường dẫn theo file nhạc của bạn
pygame.mixer.music.play(-1)  # Phát nhạc lặp lại

# Biến trạng thái âm thanh
sound_on = True

# Vòng lặp chính
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                # Đổi trạng thái âm thanh
                if sound_on:
                    pygame.mixer.music.pause()  # Dừng nhạc
                    sound_on = False
                else:
                    pygame.mixer.music.unpause()  # Phát nhạc
                    sound_on = True

    # Vẽ lên màn hình
    screen.fill((255, 255, 255))  # Màu nền
    # Vẽ nút loa
    if sound_on:
        screen.blit(button_image_on, button_rect)  # Vẽ nút loa bật
    else:
        screen.blit(button_image_off, button_rect)  # Vẽ nút loa tắt

    pygame.display.flip()

# Thoát Pygame
pygame.quit()
sys.exit()
