import pygame
import copy
import os
import random
from PATHS import SPACES_VS_WALLS_PATH, BOXES_PATH, BUTTONS_PATH, GOALS_PATH , OTHER_IMAGES_PATH, TESTCASES_PATH, SOUNDS_PATH, FONTS_PATH
from Algo_DFS import DFS
from Algo_BFS import BFS
from Algo_UCS import UCS
from Algo_AStar import AStar
from State_and_Game import Game
from Metrics_Tracker import MetricsTracker


max_grid_len = 0
max_grid_height = 0


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
    global max_grid_len, max_grid_height

    """Load the game grid from a file"""
    grid = []
    with open(filename, 'r') as file:
        file.readline()  # Skip dimensions line
        for line in file:
            line = line[:-1]
            grid.append(list(line))  # Convert each line into a list of characters
            max_grid_len = max(max_grid_len, len(line))
        max_grid_height = len(grid)
    
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

player_empty_right_image = pygame.image.load(os.path.join(OTHER_IMAGES_PATH, 'player_empty_right.png'))  # Replace with your image path
player_empty_right_image = pygame.transform.smoothscale(player_empty_right_image, (TILE_SIZE, TILE_SIZE))

player_empty_left_image = pygame.image.load(os.path.join(OTHER_IMAGES_PATH, 'player_empty_left.png'))  # Replace with your image path
player_empty_left_image = pygame.transform.smoothscale(player_empty_left_image, (TILE_SIZE, TILE_SIZE))

player_right_image = pygame.image.load(os.path.join(OTHER_IMAGES_PATH, 'player_right.png'))  # Replace with your image path
player_right_image = pygame.transform.smoothscale(player_right_image, (TILE_SIZE, TILE_SIZE))

player_left_image = pygame.image.load(os.path.join(OTHER_IMAGES_PATH, 'player_left.png'))  # Replace with your image path
player_left_image = pygame.transform.smoothscale(player_left_image, (TILE_SIZE, TILE_SIZE))

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

A_star_button_image = pygame.image.load(os.path.join(BUTTONS_PATH, 'A_star.png'))  # Replace with your image path
A_star_button_image = pygame.transform.smoothscale(A_star_button_image, (120, 80))


# Clicked algorithm img
clicked_DFS_button_image = pygame.image.load(os.path.join(BUTTONS_PATH, 'clicked_DFS.png'))  # Replace with your image path
clicked_DFS_button_image = pygame.transform.smoothscale(clicked_DFS_button_image, (120, 80))

clicked_BFS_button_image = pygame.image.load(os.path.join(BUTTONS_PATH, 'clicked_BFS.png'))  # Replace with your image path
clicked_BFS_button_image = pygame.transform.smoothscale(clicked_BFS_button_image, (120, 80))

clicked_UCS_button_image = pygame.image.load(os.path.join(BUTTONS_PATH, 'clicked_UCS.png'))  # Replace with your image path
clicked_UCS_button_image = pygame.transform.smoothscale(clicked_UCS_button_image, (120, 80))

clicked_A_star_button_image = pygame.image.load(os.path.join(BUTTONS_PATH, 'clicked_A_star.png'))  # Replace with your image path
clicked_A_star_button_image = pygame.transform.smoothscale(clicked_A_star_button_image, (120, 80))




# Set up game display
def create_display():
    global grid,  max_grid_len, max_grid_height
    rows, cols = max_grid_height, max_grid_len
    return pygame.display.set_mode((cols * TILE_SIZE * 1.2, rows * TILE_SIZE * 1.2))

# Load grid and set initial player position
def load_game(filename):
    global grid, player_pos
    grid = load_grid_from_file(filename)
    for x in range(max_grid_height):
        for y in range(len(grid[x])):
            if grid[x][y] == '@':
                player_pos = (x, y)
            # if grid[x][y] == '$' or grid[x][y] == '*':
            #     box_images[(x, y)] = random.randint(1, 3)
            if grid[x][y] == '.':
                goal_pos.append((x, y))
            

# Draw the game grid
def draw_grid(screen, direction):
    global grid

    screen.fill(GRID_COLOR)
    for row in range(max_grid_height):
        for col in range(len(grid[row])):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if grid[row][col] == '#':
                screen.blit(wall_image, rect)
            elif grid[row][col] == '@':
                if direction == 'L':
                    screen.blit(player_left_image, rect)
                elif direction == 'R':
                    screen.blit(player_right_image, rect)
                elif direction == 'l':
                    screen.blit(player_empty_left_image, rect)
                else:
                    screen.blit(player_empty_right_image, rect)
                

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
step_total = 0

# Set up font
font_path = os.path.join(FONTS_PATH, "BothWays.ttf")  # Replace with your font file path
font_size = 50
font = pygame.font.Font(font_path, font_size)

text_color = (0, 0, 0)  # White color for the main text

is_playing = False
is_moving = True


# Hàm hiển thị điểm lên màn hình
def display_score(screen, level, right_buttons_x):
    global weight_total, step_total
    level_text = font.render(f"Level: {level}", True, text_color)
    screen.blit(level_text, (right_buttons_x - 35, 60))

    step_text = font.render(f"Steps: {step_total}", True, text_color)
    screen.blit(step_text, (right_buttons_x - 35, 100))

    weight_text = font.render(f"Weights: {weight_total}", True, text_color)
    screen.blit(weight_text, (right_buttons_x - 35, 140))


def Window3(level):
    global grid, path, player_pos, is_playing, algorithm_option, weight_total, step_total, goal_pos

    pygame.display.set_caption("Sokoban Game")

    if level < 10:
        load_game(os.path.join(TESTCASES_PATH, f'input-0{level}.txt'))
    else:
        load_game(os.path.join(TESTCASES_PATH, f'input-{level}.txt'))

    # Tạo màn hình chính và tính toán khoảng trống cho các nút
    screen = create_display()
    button_space_width = screen.get_size()[0] - (max_grid_len * TILE_SIZE)  # Khoảng trống chiều ngang bên phải grid
    button_area_y = max_grid_height * TILE_SIZE  # Phần dưới của grid để đặt các nút

    # show_button_image = pygame.image.load(os.path.join(BUTTONS_PATH, 'show_button.png'))  # Replace with your image path
    # show_button_image = pygame.transform.smoothscale(show_button_image, (button_space_width - 20, 100))

    # Cài đặt các nút ở bên phải
    button_width = 80
    button_height = 80
    gap_y_right = 20  # Khoảng cách dọc giữa các nút ở bên phải
    right_buttons_x = max_grid_len * TILE_SIZE + (button_space_width - button_width) // 2

    # show_button = pygame.Rect(right_buttons_x, 150, button_width, button_height)
    play_button = pygame.Rect(right_buttons_x, 150 + button_height + gap_y_right, button_width, button_height)
    stop_button = pygame.Rect(right_buttons_x, 150 + button_height + gap_y_right, button_width, button_height)
    restart_button = pygame.Rect(right_buttons_x, 150 + 2 * (button_height + gap_y_right), button_width, button_height)
    home_button = pygame.Rect(right_buttons_x, 150 + 3 * (button_height + gap_y_right), button_width, button_height)

    # Cài đặt các nút ở dưới cùng
    bottom_buttons_y = button_area_y + 20  # Khoảng cách trên cùng từ grid đến hàng nút dưới
    gap_x_bottom = 80  # Khoảng cách ngang giữa các nút ở dưới
    bottom_buttons_x_start = (screen.get_size()[0] - (4 * button_width + 3 * gap_x_bottom)) // 2

    DFS_button = pygame.Rect(bottom_buttons_x_start, bottom_buttons_y, button_width + 40, button_height)
    clicked_DFS_button = pygame.Rect(bottom_buttons_x_start, bottom_buttons_y, button_width + 40, button_height)

    BFS_button = pygame.Rect(bottom_buttons_x_start + button_width + gap_x_bottom, bottom_buttons_y, button_width + 40, button_height)
    clicked_BFS_button = pygame.Rect(bottom_buttons_x_start + button_width + gap_x_bottom, bottom_buttons_y, button_width + 40, button_height)

    UCS_button = pygame.Rect(bottom_buttons_x_start + 2 * (button_width + gap_x_bottom), bottom_buttons_y, button_width + 40, button_height)
    clicked_UCS_button = pygame.Rect(bottom_buttons_x_start + 2 * (button_width + gap_x_bottom), bottom_buttons_y, button_width + 40, button_height)

    A_star_button = pygame.Rect(bottom_buttons_x_start + 3 * (button_width + gap_x_bottom), bottom_buttons_y, button_width + 40, button_height)
    clicked_A_star_button = pygame.Rect(bottom_buttons_x_start + 3 * (button_width + gap_x_bottom), bottom_buttons_y, button_width + 40, button_height)

    # Thêm các nút vào danh sách
    buttons[play_button_image] = play_button
    buttons[restart_button_image] = restart_button
    buttons[home_button_image] = home_button

    buttons[DFS_button_image] = DFS_button
    buttons[BFS_button_image] = BFS_button
    buttons[UCS_button_image] = UCS_button
    buttons[A_star_button_image] = A_star_button

    # buttons[clicked_BFS_button_image] = clicked_BFS_button
    # buttons[clicked_UCS_button_image] = clicked_UCS_button
    # buttons[clicked_DFS_button_image] = clicked_DFS_button
    # buttons[clicked_A_star_button_image] = clicked_A_star_button


    clicked_button_music = pygame.mixer.Sound(os.path.join(SOUNDS_PATH,"clicked_button_sound.mp3"))  # Thay đổi đường dẫn theo file nhạc của bạn
    clicked_button_music.set_volume(0.3)

    win_sound = pygame.mixer.Sound(os.path.join(SOUNDS_PATH,"win_sound.mp3"))  # Thay đổi đường dẫn theo file nhạc của bạn
    win_sound.set_volume(0.3)

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

                if buttons[restart_button_image].collidepoint(event.pos):
                    
                    weight_total = 0
                    step_total = 0

                    clicked_button_music.play()

                    is_playing= False
                    is_moving = False

                    path = []

                    if level < 10:
                        load_game(os.path.join(TESTCASES_PATH, f'input-0{level}.txt'))
                    else:
                        load_game(os.path.join(TESTCASES_PATH, f'input-{level}.txt'))
                    
                    if stop_button_image in buttons:
                        buttons[play_button_image] = play_button

                        buttons.pop(stop_button_image, None)
                
                elif buttons[home_button_image].collidepoint(event.pos):
                    
                    grid = []
                    goal_pos = []

                    # Đưa các nút còn lại về mặt định
                    buttons[DFS_button_image] = DFS_button
                    buttons[BFS_button_image] = BFS_button
                    buttons[UCS_button_image] = UCS_button
                    buttons[A_star_button_image] = A_star_button

                    # Xóa các nút đã chọn ra khỏi button
                    buttons.pop(clicked_DFS_button_image, None)
                    buttons.pop(clicked_BFS_button_image, None)
                    buttons.pop(clicked_UCS_button_image, None)
                    buttons.pop(clicked_A_star_button_image, None)
                    
                    weight_total = 0
                    step_total = 0

                    clicked_button_music.play()
                    
                    from window2 import Window2
                    Window2((800, 600))

                elif play_button_image in buttons and buttons[play_button_image].collidepoint(event.pos):
                    clicked_button_music.play()
                    is_moving = True

                    if is_playing == False:
                        is_playing = True
                        
                        
                        buttons.pop(play_button_image, None)
                        buttons[stop_button_image] = stop_button

                        # Run game
                        if algorithm_option == DFS_VALUE:
                            if level < 10:
                                load_game(os.path.join(TESTCASES_PATH, f'input-0{level}.txt'))
                            else:
                                load_game(os.path.join(TESTCASES_PATH, f'input-{level}.txt'))

                            if level < 10:
                                string_map = convert_file_to_text(os.path.join(TESTCASES_PATH, f'input-0{level}.txt'))
                            else:
                                string_map = convert_file_to_text(os.path.join(TESTCASES_PATH, f'input-{level}.txt'))

                            print(string_map)
                            game = Game()
                            game.read_map_from_string(string_map)
                            tracker = MetricsTracker()
                            path = DFS(game, tracker)
                            tracker.print_metrics()
                            tracker.reset()
                        
                        elif algorithm_option == BFS_VALUE:
                            
                            if level < 10:
                                load_game(os.path.join(TESTCASES_PATH, f'input-0{level}.txt'))
                            else:
                                load_game(os.path.join(TESTCASES_PATH, f'input-{level}.txt'))


                            if level < 10:
                                string_map = convert_file_to_text(os.path.join(TESTCASES_PATH, f'input-0{level}.txt'))
                            else:
                                string_map = convert_file_to_text(os.path.join(TESTCASES_PATH, f'input-{level}.txt'))

                            print(string_map)
                            game = Game()
                            game.read_map_from_string(string_map)
                            tracker = MetricsTracker()
                            path = BFS(game, tracker)
                            tracker.print_metrics()
                            tracker.reset()

                        elif algorithm_option == UCS_VALUE:

                            if level < 10:
                                load_game(os.path.join(TESTCASES_PATH, f'input-0{level}.txt'))
                            else:
                                load_game(os.path.join(TESTCASES_PATH, f'input-{level}.txt'))

                            if level < 10:
                                string_map = convert_file_to_text(os.path.join(TESTCASES_PATH, f'input-0{level}.txt'))
                            else:
                                string_map = convert_file_to_text(os.path.join(TESTCASES_PATH, f'input-{level}.txt'))

                            print(string_map)
                            game = Game()
                            game.read_map_from_string(string_map)
                            tracker = MetricsTracker()
                            path = UCS(game, tracker)
                            tracker.print_metrics()
                            tracker.reset()
                        
                        elif algorithm_option == A_STAR_VALUE:

                            if level < 10:
                                load_game(os.path.join(TESTCASES_PATH, f'input-0{level}.txt'))
                            else:
                                load_game(os.path.join(TESTCASES_PATH, f'input-{level}.txt'))

                            if level < 10:
                                string_map = convert_file_to_text(os.path.join(TESTCASES_PATH, f'input-0{level}.txt'))
                            else:
                                string_map = convert_file_to_text(os.path.join(TESTCASES_PATH, f'input-{level}.txt'))

                            print(string_map)
                            game = Game()
                            game.read_map_from_string(string_map)
                            tracker = MetricsTracker()
                            path = AStar(game, tracker)
                            tracker.print_metrics()
                            tracker.reset()
                    else: # dang choi
                        buttons.pop(play_button_image, None)
                        buttons[stop_button_image] = stop_button


                elif stop_button_image in buttons and buttons[stop_button_image].collidepoint(event.pos):
                    clicked_button_music.play()

                    is_moving = False

                    buttons.pop(stop_button_image, None)
                    buttons[play_button_image] = play_button
                
                elif DFS_button_image in buttons and buttons[DFS_button_image].collidepoint(event.pos):
                    clicked_button_music.play()

                    algorithm_option = DFS_VALUE
                    is_playing = False

                    # Đưa các nút còn lại về mặt định
                    buttons[DFS_button_image] = DFS_button
                    buttons[BFS_button_image] = BFS_button
                    buttons[UCS_button_image] = UCS_button
                    buttons[A_star_button_image] = A_star_button

                    # Xóa các nút đã chọn ra khỏi button
                    buttons.pop(clicked_DFS_button_image, None)
                    buttons.pop(clicked_BFS_button_image, None)
                    buttons.pop(clicked_UCS_button_image, None)
                    buttons.pop(clicked_A_star_button_image, None)


                    # Hủy nút hiện tại
                    buttons.pop(DFS_button_image, None)

                    # Thay nút hiện tại -> đã chọn
                    buttons[clicked_DFS_button_image] = clicked_DFS_button

                    print("Click DFS")
                elif BFS_button.collidepoint(event.pos):

                    clicked_button_music.play()

                    algorithm_option = BFS_VALUE
                    is_playing = False

                    # Đưa các nút còn lại về mặt định
                    buttons[DFS_button_image] = DFS_button
                    buttons[BFS_button_image] = BFS_button
                    buttons[UCS_button_image] = UCS_button
                    buttons[A_star_button_image] = A_star_button

                    # Xóa các nút đã chọn ra khỏi button
                    buttons.pop(clicked_DFS_button_image, None)
                    buttons.pop(clicked_BFS_button_image, None)
                    buttons.pop(clicked_UCS_button_image, None)
                    buttons.pop(clicked_A_star_button_image, None)


                    # Hủy nút hiện tại
                    buttons.pop(BFS_button_image, None)

                    # Thay nút hiện tại -> đã chọn
                    buttons[clicked_BFS_button_image] = clicked_BFS_button

                    print("Click BFS")
                elif UCS_button.collidepoint(event.pos):
                    clicked_button_music.play()

                    algorithm_option = UCS_VALUE
                    is_playing = False

                    # Đưa các nút còn lại về mặt định
                    buttons[DFS_button_image] = DFS_button
                    buttons[BFS_button_image] = BFS_button
                    buttons[UCS_button_image] = UCS_button
                    buttons[A_star_button_image] = A_star_button

                    # Xóa các nút đã chọn ra khỏi button
                    buttons.pop(clicked_DFS_button_image, None)
                    buttons.pop(clicked_BFS_button_image, None)
                    buttons.pop(clicked_UCS_button_image, None)
                    buttons.pop(clicked_A_star_button_image, None)


                    # Hủy nút hiện tại
                    buttons.pop(UCS_button_image, None)

                    # Thay nút hiện tại -> đã chọn
                    buttons[clicked_UCS_button_image] = clicked_UCS_button

                    print("Click UCS")
                elif A_star_button.collidepoint(event.pos):
                    clicked_button_music.play()

                    algorithm_option = A_STAR_VALUE
                    is_playing = False

                    # Đưa các nút còn lại về mặt định
                    buttons[DFS_button_image] = DFS_button
                    buttons[BFS_button_image] = BFS_button
                    buttons[UCS_button_image] = UCS_button
                    buttons[A_star_button_image] = A_star_button

                    # Xóa các nút đã chọn ra khỏi button
                    buttons.pop(clicked_DFS_button_image, None)
                    buttons.pop(clicked_BFS_button_image, None)
                    buttons.pop(clicked_UCS_button_image, None)
                    buttons.pop(clicked_A_star_button_image, None)


                    # Hủy nút hiện tại
                    buttons.pop(A_star_button_image, None)

                    # Thay nút hiện tại -> đã chọn
                    buttons[clicked_A_star_button_image] = clicked_A_star_button

                    print("Click A star")

                # Nếu nhấn nút hủy chọn thuật toán
                elif clicked_DFS_button_image in buttons and buttons[clicked_DFS_button_image].collidepoint(event.pos):
                    clicked_button_music.play()

                    algorithm_option = DFS

                    buttons.pop(clicked_DFS_button_image, None)
                    buttons[DFS_button_image] = DFS_button
                elif clicked_BFS_button_image in buttons and buttons[clicked_BFS_button_image].collidepoint(event.pos):
                    clicked_button_music.play()

                    algorithm_option = DFS

                    buttons.pop(clicked_BFS_button_image, None)
                    buttons[BFS_button_image] = BFS_button
                elif clicked_UCS_button_image in buttons and buttons[clicked_UCS_button_image].collidepoint(event.pos):
                    clicked_button_music.play()

                    algorithm_option = DFS

                    buttons.pop(clicked_UCS_button_image, None)
                    buttons[UCS_button_image] = UCS_button
                elif clicked_A_star_button_image in buttons and buttons[clicked_A_star_button_image].collidepoint(event.pos):
                    clicked_button_music.play()
                    
                    algorithm_option = DFS

                    buttons.pop(clicked_A_star_button_image, None)
                    buttons[A_star_button_image] = A_star_button

                # for button_image, button in buttons.items():

                #     if button.collidepoint(event.pos):  # Kiểm tra nếu chuột nhấn vào nút
                #         print("Button activated")


        # Di chuyển theo path
        direction = 'l'
        if len(path) > 0 and is_moving:
            direction, weight = path.pop(0)

            weight_total += weight
            step_total += 1

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

        elif len(path) == 0 and is_playing:
            win_sound.play()
            is_playing = False


        draw_grid(screen, direction)

        # Vẽ lưới và nút lên màn hình
        for button_image, button in buttons.items():
            screen.blit(button_image, button)

        # screen.blit(show_button_image, (right_buttons_x - 40, 50))

        for button_image, button in buttons.items():
            if button.collidepoint(pygame.mouse.get_pos()):
                cursor_changed = True
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Con trỏ hình bàn tay

            if not cursor_changed:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        display_score(screen, level, right_buttons_x)

        pygame.display.flip()
        clock.tick(10)  # Giới hạn FPS là 30

    pygame.quit()