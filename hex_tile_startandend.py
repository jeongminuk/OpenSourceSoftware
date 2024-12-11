import pygame
import math
import random

# Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Hex Tile Game")
clock = pygame.time.Clock()

# 색상 정의
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
COLORS = [
    (255, 0, 0),  # 빨강
    (0, 255, 0),  # 초록
    (0, 0, 255),  # 파랑
    (255, 255, 0),  # 노랑
    (128, 0, 128),  # 보라
]

# 폰트 초기화
pygame.font.init()
font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 48, bold=True)

# 타일과 보드 속성
TILE_SIZE = 40
BOARD_ROWS = 5
BOARD_COLS = 5

# 보드는 행(row), 열(col), 그리고 각 위치에서의 타일 스택을 표현하는 3차원 배열로 구성
board = [[[ ] for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# 게임 변수
tile_sets = []
dragging_set = None
dragging_position = None
score = 0
level = 1
max_level = 10
is_game_over = False
game_state = "start"  # 게임 상태: start, playing, game_over
time_limit = 3 # 시간 제한 (초)
start_ticks = None  # 게임 시작 시간

# 타일 클래스 정의
class Tile:
    def __init__(self, color):
        self.color = color  # 타일의 색상

# 육각형 타일 그리기 함수
def draw_hexagon(surface, color, center, size, border=3):
    points = [
        (center[0] + size * math.cos(math.radians(angle)),
         center[1] + size * math.sin(math.radians(angle)))
        for angle in range(0, 360, 60)
    ]
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, BLACK, points, border)

# 보드를 화면에 그리기
def draw_board(surface, board, size):
    for row_index, row in enumerate(board):
        for col_index, tile_stack in enumerate(row):
            x = col_index * size * 1.5 + 100
            y = row_index * size * math.sqrt(3) + 100 + (col_index % 2) * size * math.sqrt(3) / 2
            draw_hexagon(surface, GRAY, (x, y), size, border=1)
            for i, tile in enumerate(tile_stack):
                draw_hexagon(surface, tile.color, (x, y - i * (size * 0.1)), size)

# 시작 화면 그리기
def draw_start_screen():
    screen.fill(WHITE)
    title = title_font.render("Hex Tile Game", True, BLACK)
    instruction = font.render("Press SPACE to Start", True, BLACK)
    screen.blit(title, (400 - title.get_width() // 2, 200))
    screen.blit(instruction, (400 - instruction.get_width() // 2, 300))

# 게임 종료 화면 그리기
def draw_game_over_screen():
    screen.fill(WHITE)
    title = title_font.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Final Score: {score}", True, BLACK)
    instruction = font.render("Press R to Restart", True, BLACK)
    screen.blit(title, (400 - title.get_width() // 2, 200))
    screen.blit(score_text, (400 - score_text.get_width() // 2, 300))
    screen.blit(instruction, (400 - instruction.get_width() // 2, 400))

# 게임 시작 함수
def start_game():
    global tile_sets, dragging_set, dragging_position, score, level, is_game_over, start_ticks
    tile_sets = [generate_tile_set(level) for _ in range(3)]
    dragging_set = None
    dragging_position = None
    score = 0
    level = 1
    is_game_over = False
    start_ticks = pygame.time.get_ticks()  # 게임 시작 시간 초기화

# 랜덤한 타일 세트 생성 함수
def generate_tile_set(level):
    num_tiles = random.randint(2, 4 + level // 2)
    colors = random.sample(COLORS, min(level, len(COLORS)))
    return [Tile(random.choice(colors)) for _ in range(num_tiles)]

# 드래그 중인 타일을 화면에 그리기
def draw_dragging_tiles(surface, dragging_set, position):
    if dragging_set:
        x, y = position
        for i, tile in enumerate(dragging_set):
            draw_hexagon(surface, tile.color, (x, y - i * (TILE_SIZE * 0.4)), TILE_SIZE)

# 드래그 중인 타일 세트를 보드에 배치
def place_tiles_on_board(board, dragging_set, mouse_pos):
    global dragging_position
    placed = False
    for row_index, row in enumerate(board):
        for col_index, cell in enumerate(row):
            x = col_index * TILE_SIZE * 1.5 + 100
            y = row_index * TILE_SIZE * math.sqrt(3) + 100 + (col_index % 2) * TILE_SIZE * math.sqrt(3) / 2
            if math.sqrt((mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2) < TILE_SIZE:
                cell.extend(dragging_set)
                dragging_set = None
                placed = True
                break
        if placed:
            break
    if not placed:  # 드래그 실패 시 원래 위치로 돌아감
        dragging_set = None

# 메인 게임 루프
running = True
while running:
    screen.fill(WHITE)

    if game_state == "start":
        draw_start_screen()
    elif game_state == "playing":
        elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = max(0, time_limit - elapsed_time)
        screen.blit(font.render(f"Time Left: {remaining_time}s", True, (255, 0, 0)), (10, 10))
        draw_board(screen, board, TILE_SIZE)
        draw_dragging_tiles(screen, dragging_set, pygame.mouse.get_pos())

        if remaining_time <= 0:
            game_state = "game_over"
    elif game_state == "game_over":
        draw_game_over_screen()

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == "start" and event.key == pygame.K_SPACE:
                game_state = "playing"
                start_game()
            elif game_state == "game_over" and event.key == pygame.K_r:
                game_state = "start"
        elif game_state == "playing" and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for set_index, tile_set in enumerate(tile_sets):
                x = 600
                y = 150 + set_index * TILE_SIZE * 3
                if math.sqrt((mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2) < TILE_SIZE:
                    dragging_set = tile_set
                    tile_sets[set_index] = []
                    dragging_position = (set_index, tile_set)
                    break
        elif game_state == "playing" and event.type == pygame.MOUSEBUTTONUP:
            if dragging_set:
                place_tiles_on_board(board, dragging_set, event.pos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
