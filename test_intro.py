import pygame
import sys
import math

# Khởi tạo Pygame
pygame.init()

# Cài đặt màn hình
window_sizes = [(800, 600), (800, 600)]
current_window_index = 0

background_image = pygame.image.load(r"D:\Artificial Intelligent Foudation\Project 1 - Search\images\background\background.jpg")
background_image = pygame.transform.smoothscale(background_image, (800, 600))

# Tải hình ảnh
image = pygame.image.load(r"D:\Artificial Intelligent Foudation\Project 1 - Search\images\background\player_intro.png")  # Thay đổi đường dẫn đến bức ảnh của bạn
image_rect = image.get_rect(center=(100, 450))  # Đặt vị trí ban đầu của bức ảnh

# Thiết lập biến điều khiển
direction = 1  # 1: di chuyển từ trái sang phải, -1: di chuyển từ phải sang trái
speed = 5  # Tốc độ di chuyển
flip_image = False  # Biến để xác định liệu hình ảnh đã bị lật ngược chưa


# Tải bức ảnh ở giữa và lấy kích thước gốc
center_image = pygame.image.load(r"D:\Artificial Intelligent Foudation\Project 1 - Search\images\buttons\play_button.png")  # Thay đổi đường dẫn đến bức ảnh của bạn
center_image = pygame.transform.smoothscale(center_image, (100, 100))
original_size = center_image.get_size()
max_scale = 0.8  # Tỉ lệ phóng to tối đa
min_scale = 0.7  # Tỉ lệ thu nhỏ tối thiểu
scale = 1.0  # Tỉ lệ ban đầu
scale_step = 0.005  # Bước thay đổi tỉ lệ


# Biến điều khiển để phóng to hoặc thu nhỏ
scaling_up = True


# Tải hình ảnh nút loa
button_image_on = pygame.image.load(r"D:\Artificial Intelligent Foudation\Project 1 - Search\images\buttons\speaker_on_button.png")  # Nút loa bật
button_image_off = pygame.image.load(r"D:\Artificial Intelligent Foudation\Project 1 - Search\images\buttons\speaker_off_button.png")  # Nút loa tắt
button_image_on = pygame.transform.smoothscale(button_image_on, (60, 60))
button_image_off = pygame.transform.smoothscale(button_image_off, (60, 60))

button_rect = button_image_on.get_rect(topleft=(650, 50))  # Đặt vị trí nút loa

# Bật nhạc
pygame.mixer.music.load(r"D:\Artificial Intelligent Foudation\Project 1 - Search\sounds\さりい＿パレット .wav")  # Thay đổi đường dẫn theo file nhạc của bạn
pygame.mixer.music.play(-1)  # Phát nhạc lặp lại

# Biến trạng thái âm thanh
sound_on = True

# Set up font
font_path = r"D:\Artificial Intelligent Foudation\Project 1 - Search\fonts\BothWays.ttf"  # Replace with your font file path
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



# Hàm hiệu ứng phóng to từ giữa
def Window2(new_size):
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
    Window2(window_sizes[current_window_index])


screen = pygame.display.set_mode(window_sizes[current_window_index])



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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if center_image.collidepoint(event.pos):
                switch_window()

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
    scaled_width = int(original_size[0] * scale)
    scaled_height = int(original_size[1] * scale)
    scaled_image = pygame.transform.smoothscale(center_image, (scaled_width, scaled_height))

    # Cập nhật vị trí để ảnh luôn ở giữa màn hình
    play_button_intro = scaled_image.get_rect(center=(800 // 2, 600 // 2))

    # Cập nhật vị trí của bức ảnh
    image_rect.x += speed * direction

    # Kiểm tra xem bức ảnh đã đến mép màn hình chưa
    if direction == 1 and image_rect.right >= 800:  # Đến mép phải
        direction = -1  # Đổi hướng di chuyển
        flip_image = True  # Đánh dấu rằng hình ảnh sẽ bị lật
    elif direction == -1 and image_rect.left <= 0:  # Đến mép trái
        direction = 1  # Đổi hướng di chuyển
        flip_image = True  # Đánh dấu rằng hình ảnh sẽ bị lật

    # Nếu bức ảnh đã được đánh dấu để lật, lật hình ảnh
    if flip_image:
        image = pygame.transform.flip(image, True, False)  # Lật ngược hình ảnh theo chiều ngang
        flip_image = False  # Đặt lại trạng thái lật

    # Vẽ lên màn hình

    screen.blit(background_image, (0, 0))  # Vẽ bức ảnh nền
    screen.blit(scaled_image, play_button_intro)
    screen.blit(image, image_rect)  # Vẽ bức ảnh
    if sound_on:
        screen.blit(button_image_on, button_rect)  # Vẽ nút loa bật
    else:
        screen.blit(button_image_off, button_rect)  # Vẽ nút loa tắt


    for i, (surface, (x, y)) in enumerate(zip(text_surfaces, char_positions)):
        offset_y = amplitude * math.sin(frequency * (pygame.time.get_ticks() + i * 100))  # Tính độ lệch y cho mỗi chữ cái
        screen.blit(surface, (x, y + offset_y))
    pygame.display.flip()
    pygame.time.delay(20)  # Delay để điều chỉnh tốc độ di chuyển

# Thoát Pygame
pygame.quit()
sys.exit()
