import pygame
import sys
import math 

# Initialize Pygame
pygame.init()

# Screen setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Text Overlay Example")

# Load background image and resize to fit screen
background_image = pygame.image.load(r"D:\Artificial Intelligent Foudation\Project 1 - Search\images\background\background.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

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
start_x = (screen_width - total_text_width) // 2
char_positions = [(start_x + sum(surface.get_width() for surface in text_surfaces[:i]), screen_height // 2) for i in range(len(text))]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the background
    screen.blit(background_image, (0, 0))

    for i, (surface, (x, y)) in enumerate(zip(text_surfaces, char_positions)):
        offset_y = amplitude * math.sin(frequency * (pygame.time.get_ticks() + i * 100))  # Tính độ lệch y cho mỗi chữ cái
        screen.blit(surface, (x, y + offset_y))


    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
