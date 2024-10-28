import pygame
import copy
import os
import random
from PATHS import SPACES_VS_WALLS_PATH, BOXES_PATH, BUTTONS_PATH, GOALS_PATH , OTHER_IMAGES_PATH, TESTCASES_PATH, SOUNDS_PATH
from DFS import DFS
from BFS import BFS
from UCS import UCS
from State_and_Game import Game
from MetricsTracker import MetricsTracker


RIGHT = (0, 1)
LEFT = (0, -1)
UP = (-1, 0)
DOWN = (1, 0)


DFS_VALUE = 0
BFS_VALUE = 1
UCS_VALUE = 2
A_STAR_VALUE = 3

buttons = {}

grid = []
player_pos = ()
goal_pos = []

algorithm_option = DFS # Default is DFS


def load_grid_from_file(filename):
    """Load the game grid from a file"""
    grid = []
    with open(filename, 'r') as file:
        file.readline()  # Skip dimensions line
        for line in file:
            line = line[:-1]
            grid.append(list(line))  # Convert each line into a list of characters
    return grid


def convert_file_to_text(filename):
    string = ""
    with open(filename, 'r') as file:
        for line in file:
            string += line
    return string

# Define constants
TILE_SIZE = 80  # Size of each tile in the grid
GRID_COLOR = (200, 200, 200)

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# images
wall_image = pygame.image.load(os.path.join(SPACES_VS_WALLS_PATH, 'wall.png'))  # Replace with your image path
wall_image = pygame.transform.smoothscale(wall_image, (TILE_SIZE, TILE_SIZE))

space_image = pygame.image.load(os.path.join(SPACES_VS_WALLS_PATH, 'space.png'))  # Replace with your image path
space_image = pygame.transform.smoothscale(space_image, (TILE_SIZE, TILE_SIZE))

player_image = pygame.image.load(os.path.join(OTHER_IMAGES_PATH, 'player.png'))  # Replace with your image path
player_image = pygame.transform.smoothscale(player_image, (TILE_SIZE, TILE_SIZE))

# Buttons
play_button_image = pygame.image.load(os.path.join(BUTTONS_PATH, 'play_button.png'))  # Replace with your image path
play_button_image = pygame.transform.smoothscale(play_button_image, (TILE_SIZE, TILE_SIZE))

stop_button_image = pygame.image.load(os.path.join(BUTTONS_PATH, 'stop_button.png'))  # Replace with your image path
stop_button_image = pygame.transform.smoothscale(stop_button_image, (TILE_SIZE, TILE_SIZE))

home_button_image = pygame.image.load(os.path.join(BUTTONS_PATH, 'home_button.png'))  # Replace with your image path
home_button_image = pygame.transform.smoothscale(home_button_image, (TILE_SIZE, TILE_SIZE))

restart_button_image = pygame.image.load(os.path.join(BUTTONS_PATH, 'restart_button.png'))  # Replace with your image path
restart_button_image = pygame.transform.smoothscale(restart_button_image, (TILE_SIZE, TILE_SIZE))



DFS_button_image = pygame.image.load(os.path.join(BUTTONS_PATH, 'DFS.png'))  # Replace with your image path
DFS_button_image = pygame.transform.smoothscale(DFS_button_image, (120, 80))

BFS_button_image = pygame.image.load(os.path.join(BUTTONS_PATH, 'BFS.png'))  # Replace with your image path
BFS_button_image = pygame.transform.smoothscale(BFS_button_image, (120, 80))

UCS_button_image = pygame.image.load(os.path.join(BUTTONS_PATH, 'UCS.png'))  # Replace with your image path
UCS_button_image = pygame.transform.smoothscale(UCS_button_image, (120, 80))

A_star_button_imag = pygame.image.load(os.path.join(BUTTONS_PATH, 'A_star.png'))  # Replace with your image path
A_star_button_imag = pygame.transform.smoothscale(A_star_button_imag, (120, 80))

# Set up game display
def create_display():
    global grid
    rows, cols = len(grid), len(grid[0])
    return pygame.display.set_mode((cols * TILE_SIZE * 1.2, rows * TILE_SIZE * 1.2))

# Load grid and set initial player position
def load_game(filename):
    global grid, player_pos
    grid = load_grid_from_file(filename)
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == '@':
                player_pos = (x, y)
            # if grid[x][y] == '$' or grid[x][y] == '*':
            #     box_images[(x, y)] = random.randint(1, 3)
            if grid[x][y] == '.':
                goal_pos.append((x, y))
            

# Draw the game grid
def draw_grid(screen):
    global grid

    screen.fill(GRID_COLOR)
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if grid[row][col] == '#':
                screen.blit(wall_image, rect)
            elif grid[row][col] == '@':
                screen.blit(player_image, rect)
            elif grid[row][col] == '$':
                box_image = pygame.image.load(os.path.join(BOXES_PATH, f'box3.png'))  # Replace with your image path
                box_image = pygame.transform.smoothscale(box_image, (TILE_SIZE, TILE_SIZE))
                screen.blit(box_image, rect)
            elif grid[row][col] == '.':
                goal_image = pygame.image.load(os.path.join(GOALS_PATH, f'goal2.png'))  # Replace with your image path
                goal_image = pygame.transform.smoothscale(goal_image, (TILE_SIZE, TILE_SIZE))
                screen.blit(goal_image, rect)
            elif grid[row][col] == ' ':
                screen.blit(space_image, rect)
            elif grid[row][col] == '*':
                finish_goal_image = pygame.image.load(os.path.join(GOALS_PATH, f'finish_goal.png'))  # Replace with your image path
                finish_goal_image = pygame.transform.smoothscale(finish_goal_image, (TILE_SIZE, TILE_SIZE))
                screen.blit(finish_goal_image, rect)

path = []
weight_total = 0

def Window3(level):
    global grid, path, player_pos

    pygame.display.set_caption("Sokoban Game")

    if level < 10:
        load_game(os.path.join(TESTCASES_PATH, f'input-0{level}.txt'))
    else:
        load_game(os.path.join(TESTCASES_PATH, f'input-{level}.txt'))

    # Tạo màn hình chính và tính toán khoảng trống cho các nút
    screen = create_display()
    button_space_width = screen.get_size()[0] - (len(grid[0]) * TILE_SIZE)  # Khoảng trống chiều ngang bên phải grid
    button_area_y = len(grid) * TILE_SIZE  # Phần dưới của grid để đặt các nút

    # Cài đặt các nút ở bên phải
    button_width = 80
    button_height = 80
    gap_y_right = 20  # Khoảng cách dọc giữa các nút ở bên phải
    right_buttons_x = len(grid[0]) * TILE_SIZE + (button_space_width - button_width) // 2

    play_button = pygame.Rect(right_buttons_x, 150, button_width, button_height)
    stop_button = pygame.Rect(right_buttons_x, 150, button_width, button_height)
    restart_button = pygame.Rect(right_buttons_x, 150 + button_height + gap_y_right, button_width, button_height)
    home_button = pygame.Rect(right_buttons_x, 150 + 2 * (button_height + gap_y_right), button_width, button_height)

    # Cài đặt các nút ở dưới cùng
    bottom_buttons_y = button_area_y + 20  # Khoảng cách trên cùng từ grid đến hàng nút dưới
    gap_x_bottom = 80  # Khoảng cách ngang giữa các nút ở dưới
    bottom_buttons_x_start = (screen.get_size()[0] - (4 * button_width + 3 * gap_x_bottom)) // 2

    DFS_button = pygame.Rect(bottom_buttons_x_start, bottom_buttons_y, button_width + 40, button_height)
    BFS_button = pygame.Rect(bottom_buttons_x_start + button_width + gap_x_bottom, bottom_buttons_y, button_width + 40, button_height)
    UCS_button = pygame.Rect(bottom_buttons_x_start + 2 * (button_width + gap_x_bottom), bottom_buttons_y, button_width + 40, button_height)
    A_star_button = pygame.Rect(bottom_buttons_x_start + 3 * (button_width + gap_x_bottom), bottom_buttons_y, button_width + 40, button_height)

    # Thêm các nút vào danh sách
    buttons[play_button_image] = play_button
    buttons[restart_button_image] = restart_button
    buttons[home_button_image] = home_button

    buttons[DFS_button_image] = DFS_button
    buttons[BFS_button_image] = BFS_button
    buttons[UCS_button_image] = UCS_button
    buttons[A_star_button_imag] = A_star_button


    clicked_button_music = pygame.mixer.Sound(os.path.join(SOUNDS_PATH,"clicked_button_sound.mp3"))  # Thay đổi đường dẫn theo file nhạc của bạn
    clicked_button_music.set_volume(0.3)

    # Vòng lặp chính
    running = True
    clock = pygame.time.Clock()
    while running:

        cursor_changed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            # Kiểm tra sự kiện nhấn chuột
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_image in buttons and buttons[play_button_image].collidepoint(event.pos):
                    clicked_button_music.play()

                    buttons.pop(play_button_image, None)
                    buttons[stop_button_image] = stop_button

                    # Run game
                    if algorithm_option == DFS_VALUE:
                        string_map = convert_file_to_text(os.path.join(TESTCASES_PATH, f'input-0{level}.txt'))
                        print(string_map)
                        game = Game()
                        game.read_map_from_string(string_map)
                        tracker = MetricsTracker()
                        path = DFS(game, tracker)
                        tracker.print_metrics()
                        tracker.reset()
                        

                elif stop_button_image in buttons and buttons[stop_button_image].collidepoint(event.pos):
                    clicked_button_music.play()

                    buttons.pop(stop_button_image, None)
                    buttons[play_button_image] = play_button
                
                elif DFS_button.collidepoint(event.pos):
                    algorithm_option = DFS_VALUE
                    print("Click DFS")
                elif BFS_button.collidepoint(event.pos):
                    algorithm_option = BFS_VALUE
                elif UCS_button.collidepoint(event.pos):
                    algorithm_option = UCS_VALUE
                elif A_star_button.collidepoint(event.pos):
                    algorithm_option = A_STAR_VALUE


                # for button_image, button in buttons.items():

                #     if button.collidepoint(event.pos):  # Kiểm tra nếu chuột nhấn vào nút
                #         print("Button activated")


        # Di chuyển theo path
        if len(path) > 0:
            direction, weight = path.pop(0)

            next_player_pos = ()
            
            
            if direction in ['r', 'R']:
                if direction == 'R':
                    current_box = (player_pos[0] + RIGHT[0], player_pos[1] + RIGHT[1])
                    next_box = (current_box[0] + RIGHT[0], current_box[1] + RIGHT[1])

                    # update vi tri hop moi
                    if grid[next_box[0]][next_box[1]] == '.':
                        grid[next_box[0]][next_box[1]] = '*'
                    else:
                        grid[next_box[0]][next_box[1]] = '$'

                    # Update vi tri hop cu
                    if current_box in goal_pos:
                        grid[current_box[0]][current_box[1]] = '.'
                    else:
                        grid[current_box[0]][current_box[1]] = ' '

                # update vi tri player moi
                next_player_pos = (player_pos[0] + RIGHT[0], player_pos[1] + RIGHT[1])
                if grid[next_player_pos[0]][next_player_pos[1]] == '.':
                    grid[next_player_pos[0]][next_player_pos[1]] = '+'
                else:
                    grid[next_player_pos[0]][next_player_pos[1]] = '@'
                
                # update vi tri player cu
                if grid[player_pos[0]][player_pos[1]] == '+':
                    grid[player_pos[0]][player_pos[1]] = '.'
                else:
                    grid[player_pos[0]][player_pos[1]] = ' '


            elif direction in ['l', 'L']:
                if direction == 'L':
                    current_box = (player_pos[0] + LEFT[0], player_pos[1] + LEFT[1])
                    next_box = (current_box[0] + LEFT[0], current_box[1] + LEFT[1])

                    # update vi tri hop moi
                    if grid[next_box[0]][next_box[1]] == '.':
                        grid[next_box[0]][next_box[1]] = '*'
                    else:
                        grid[next_box[0]][next_box[1]] = '$'
                    
                    # Update vi tri hop cu
                    if current_box in goal_pos:
                        grid[current_box[0]][current_box[1]] = '.'
                    else:
                        grid[current_box[0]][current_box[1]] = ' '

                # update vi tri player moi
                next_player_pos = (player_pos[0] + LEFT[0], player_pos[1] + LEFT[1])
                if grid[next_player_pos[0]][next_player_pos[1]] == '.':
                    grid[next_player_pos[0]][next_player_pos[1]] = '+'
                else:
                    grid[next_player_pos[0]][next_player_pos[1]] = '@'
                
                # update vi tri player cu
                if grid[player_pos[0]][player_pos[1]] == '+':
                    grid[player_pos[0]][player_pos[1]] = '.'
                else:
                    grid[player_pos[0]][player_pos[1]] = ' '

            elif direction in ['u', 'U']:
                if direction == 'U':
                    current_box = (player_pos[0] + UP[0], player_pos[1] + UP[1])
                    next_box = (current_box[0] + UP[0], current_box[1] + UP[1])

                    # update vi tri hop moi
                    if grid[next_box[0]][next_box[1]] == '.':
                        grid[next_box[0]][next_box[1]] = '*'
                    else:
                        grid[next_box[0]][next_box[1]] = '$'
                    
                    # Update vi tri hop cu
                    if current_box in goal_pos:
                        grid[current_box[0]][current_box[1]] = '.'
                    else:
                        grid[current_box[0]][current_box[1]] = ' '

                # update vi tri player moi
                next_player_pos = (player_pos[0] + UP[0], player_pos[1] + UP[1])

                if grid[next_player_pos[0]][next_player_pos[1]] == '.':
                    grid[next_player_pos[0]][next_player_pos[1]] = '+'
                else:
                    grid[next_player_pos[0]][next_player_pos[1]] = '@'
                
                # update vi tri player cu
                if grid[player_pos[0]][player_pos[1]] == '+':
                    grid[player_pos[0]][player_pos[1]] = '.'
                else:
                    grid[player_pos[0]][player_pos[1]] = ' '
            elif direction in ['d', 'D']:

                if direction == 'D':
                    current_box = (player_pos[0] + DOWN[0], player_pos[1] + DOWN[1])
                    next_box = (current_box[0] + DOWN[0], current_box[1] + DOWN[1])

                    # update vi tri hop moi
                    if grid[next_box[0]][next_box[1]] == '.':
                        grid[next_box[0]][next_box[1]] = '*'
                    else:
                        grid[next_box[0]][next_box[1]] = '$'

                    # Update vi tri hop cu
                    if current_box in goal_pos:
                        grid[current_box[0]][current_box[1]] = '.'
                    else:
                        grid[current_box[0]][current_box[1]] = ' '

                # update vi tri player moi
                next_player_pos = (player_pos[0] + DOWN[0], player_pos[1] + DOWN[1])
                if grid[next_player_pos[0]][next_player_pos[1]] == '.':
                    grid[next_player_pos[0]][next_player_pos[1]] = '+'
                else:
                    grid[next_player_pos[0]][next_player_pos[1]] = '@'
                
                # update vi tri player cu
                if grid[player_pos[0]][player_pos[1]] == '+':
                    grid[player_pos[0]][player_pos[1]] = '.'
                else:
                    grid[player_pos[0]][player_pos[1]] = ' '


            player_pos = next_player_pos


        draw_grid(screen)
        # Vẽ lưới và nút lên màn hình
        for button_image, button in buttons.items():
            screen.blit(button_image, button)



        for button_image, button in buttons.items():
            if button.collidepoint(pygame.mouse.get_pos()):
                cursor_changed = True
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Con trỏ hình bàn tay

            if not cursor_changed:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.flip()
        clock.tick(10)  # Giới hạn FPS là 30

    pygame.quit()