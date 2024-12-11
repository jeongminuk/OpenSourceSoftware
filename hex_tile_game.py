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
time_limit = 5 # 시간 제한 (초)
start_ticks = None  # 게임 시작 시간

# 타일 클래스 정의
class Tile:
    def __init__(self, color):
        self.color = color  # 타일의 색상

# 그림자와 그라데이션을 포함한 육각형 타일 그리기 함수
def draw_hexagon(surface, color, center, size, border=3):
    # 그림자 추가
    shadow_color = (50, 50, 50)  # 그림자 색상
    shadow_offset = 5  # 그림자 오프셋
    points = [
        (center[0] + size * math.cos(math.radians(angle)),
         center[1] + size * math.sin(math.radians(angle)))
        for angle in range(0, 360, 60)
    ]
    shadow_points = [(x + shadow_offset, y + shadow_offset) for x, y in points]
    pygame.draw.polygon(surface, shadow_color, shadow_points)  # 그림자

    # 타일 그라데이션 효과
    gradient = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
    for i in range(size, 0, -1):
        alpha = int((i / size) * 255)  # 투명도 조정
        pygame.draw.polygon(
            gradient,
            (*color, alpha),  # 색상 + 투명도
            [
                (size + i * math.cos(math.radians(angle)),
                 size + i * math.sin(math.radians(angle)))
                for angle in range(0, 360, 60)
            ]
        )
    surface.blit(gradient, (center[0] - size, center[1] - size))

    # 타일 테두리 그리기
    pygame.draw.polygon(surface, BLACK, points, border)

# 보드를 화면에 그리는 함수
def draw_board(surface, board, size):
    for row_index, row in enumerate(board):
        for col_index, tile_stack in enumerate(row):
            x = col_index * size * 1.5 + 100
            y = row_index * size * math.sqrt(3) + 100 + (col_index % 2) * size * math.sqrt(3) / 2
            draw_hexagon(surface, GRAY, (x, y), size, border=1)
            for i, tile in enumerate(tile_stack):
                draw_hexagon(surface, tile.color, (x, y - i * (size * 0.1)), size)

# 랜덤한 타일 세트 생성 함수
def generate_tile_set(level):
    num_tiles = random.randint(2, 4 + level // 2)  # 레벨에 따라 타일 수 증가
    colors = random.sample(COLORS, min(level, len(COLORS)))  # 레벨에 따라 색상 증가
    return [Tile(random.choice(colors)) for _ in range(num_tiles)]

# 이웃 타일의 좌표를 찾는 함수
def get_neighbors(board, row, col):
    # 짝수 열과 홀수 열에 따른 이웃 방향 정의
    if col % 2 == 0:  # 짝수 열
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1)]
    else:  # 홀수 열
        directions = [(-1, 1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]
    neighbors = []
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < len(board) and 0 <= c < len(board[r]):
            neighbors.append((r, c))
    return neighbors

def find_connected_tiles(board, row, col, color, visited=None):
    if visited is None:
        visited = set()

    # 이미 방문한 셀은 제외
    if (row, col) in visited:
        return []

    visited.add((row, col))
    connected = [(row, col)]

    # 6방향 탐색
    for r, c in get_neighbors(board, row, col):
        if board[r][c] and board[r][c][-1].color == color:
            connected += find_connected_tiles(board, r, c, color, visited)

    return connected

# 타일 제거 함수
def remove_tiles(board, tiles):
    for r, c in tiles:
        if board[r][c]:
            board[r][c].pop()

def check_for_removal(board):
    global score
    global level

    # 보드의 각 셀을 순회하며 스택이 6개 이상인 위치를 찾음
    for row_index, row in enumerate(board):
        for col_index, cell in enumerate(row):
            if len(cell) >= 6:  # 스택 높이가 6 이상인 경우
                score += len(cell)  # 스택에 쌓인 타일 개수만큼 점수 추가
                board[row_index][col_index] = []  # 해당 위치의 스택 비우기

                # 레벨 증가 조건 확인
                if score >= level * 10 and level < max_level:
                    level += 1

# 게임 종료 조건 체크 함수
def check_game_over(board):
    for row in board:
        for cell in row:
            if len(cell) < 6:  # 여유 공간이 있는 경우
                return False
    return True

# 타일 이동 함수
def move_tile(board, row, col):
    tile_stack = board[row][col]
    if not tile_stack:
        return
    while tile_stack:
        tile = tile_stack.pop()
        neighbors = get_neighbors(board, row, col)
        for r, c in neighbors:
            neighbor_stack = board[r][c]
            if neighbor_stack and neighbor_stack[-1].color == tile.color:
                board[r][c].append(tile)
                break
        else:
            board[row][col].append(tile)
            break

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
    global tile_sets, dragging_set, dragging_position, score, level, is_game_over
    tile_sets = [generate_tile_set(level) for _ in range(3)]
    dragging_set = None
    dragging_position = None
    score = 0
    level = 1
    is_game_over = False
    start_ticks = pygame.time.get_ticks()  # 게임 시작 시간 초기화

# 메인 게임 루프
running = True
start_game()
while running:
    screen.fill(WHITE)
    
    draw_board(screen, board, TILE_SIZE)

    # UI 표시
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    remaining_text = font.render(f"Remaining Sets: {len(tile_sets)}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))
    screen.blit(remaining_text, (10, 70))

    # 게임 종료 확인
    if check_game_over(board):
        game_over_text = font.render("Game Over! Press R to Restart", True, (255, 0, 0))
        screen.blit(game_over_text, (200, 300))
        is_game_over = True

    # 현재 타일 세트를 화면에 그리기
    for set_index, tile_set in enumerate(tile_sets):
        x = 600
        y = 150 + set_index * (TILE_SIZE * 3)
        for i, tile in enumerate(tile_set):
            draw_hexagon(screen, tile.color, (x, y - i * (TILE_SIZE * 0.4)), TILE_SIZE)

    # 드래그 중인 세트를 화면에 그리기
    if dragging_set:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i, tile in enumerate(dragging_set):
            draw_hexagon(screen, tile.color, (mouse_x, mouse_y - i * (TILE_SIZE * 0.4)), TILE_SIZE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and is_game_over:
                start_game()
        elif not is_game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for set_index, tile_set in enumerate(tile_sets):
                x = 600
                y = 150 + set_index * (TILE_SIZE * 3)
                if tile_set and math.sqrt((mouse_x - x)**2 + (mouse_y - y)**2) < TILE_SIZE:
                    dragging_set = tile_set
                    dragging_position = (set_index, tile_set)
                    tile_sets[set_index] = []
                    break
        elif not is_game_over and event.type == pygame.MOUSEBUTTONUP:
            if dragging_set:
                mouse_x, mouse_y = event.pos
                placed = False
                for row_index, row in enumerate(board):
                    for col_index, cell in enumerate(row):
                        x = col_index * TILE_SIZE * 1.5 + 100
                        y = row_index * TILE_SIZE * math.sqrt(3) + 100 + (col_index % 2) * TILE_SIZE * math.sqrt(3) / 2
                        if math.sqrt((mouse_x - x)**2 + (mouse_y - y)**2) < TILE_SIZE:
                            cell.extend(dragging_set)
                            move_tile(board, row_index, col_index)
                            dragging_set = None
                            placed = True
                            break
                    if placed:
                        break
                if not placed:
                    set_index, tile_set = dragging_position
                    tile_sets[set_index] = dragging_set
                    dragging_set = None

    if all(len(tile_set) == 0 for tile_set in tile_sets):
        tile_sets = [generate_tile_set(level) for _ in range(3)]

    check_for_removal(board)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()