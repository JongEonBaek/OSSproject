# main.py

import pygame
import sys
import os
import platform
from collections import deque  # 이동 큐를 위해 deque 사용
import avoid_star  # avoid_star.py 모듈 가져오기
import image_puzzle  # image_puzzle.py 모듈 가져오기

# 파이게임 초기화
pygame.init()

# 화면 크기 설정
screen_width = 750
screen_height = 750
screen = pygame.display.set_mode((screen_width, screen_height))

name = '백종언'
birthday = "2001-04-13"
# 창 제목 설정
pygame.display.set_caption("Happy Birthday " + name + "!")

# 색상 정의 (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 운영체제에 따라 폰트 경로 설정
if platform.system() == "Windows":
    font_path = "C:\\Windows\\Fonts\\malgun.ttf"  # 맑은 고딕
elif platform.system() == "Darwin":  # macOS
    font_path = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
else:  # Linux 등
    font_path = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"

# 프로젝트 폴더에 있는 폰트 파일을 우선적으로 사용
# 예: "NanumGothic.ttf"
local_font_path = "NanumGothic.ttf"

if os.path.exists(local_font_path):
    font_path = local_font_path

# 폰트 파일이 존재하는지 확인
if not os.path.exists(font_path):
    print(f"폰트 파일을 찾을 수 없습니다: {font_path}")
    print("프로젝트 폴더에 한글을 지원하는 폰트 파일을 추가하거나, 시스템 폰트를 사용하세요.")
    pygame.quit()
    sys.exit()

# 폰트 로드
try:
    font = pygame.font.Font(font_path, 25)  # 상단 텍스트용 폰트, 크기 15
    button_font = pygame.font.Font(font_path, 30)  # 버튼용 폰트, 크기 30
except pygame.error as e:
    print(f"폰트를 로드할 수 없습니다: {e}")
    pygame.quit()
    sys.exit()

# 초기 스테이지 설정
current_stage = 1  # 현재 스테이지
max_stages = 3  # 총 스테이지 수

def update_top_text():
    global top_text, top_text_surface
    if current_stage == 1:
        top_text = name + "이의 생일은 " + birthday + "이다. \n이 생일은 어떤 별자리에 속하는가!?!?"
    elif current_stage == 2:
        top_text = "스테이지 2: 새로운 도전이 기다리고 있다!"
    elif current_stage == 3:
        top_text = "스테이지 3: 마지막 도전! 모든 것을 이겨내라!"
    top_text_surface = font.render(top_text, True, WHITE)  # 흰색 텍스트

update_top_text()

# 캐릭터 이미지 로드
try:
    character_image = pygame.image.load("./image/character.png").convert_alpha()
except pygame.error as e:
    print(f"캐릭터 이미지를 로드할 수 없습니다: {e}")
    pygame.quit()
    sys.exit()

# 캐릭터 크기 조정 (필요 시)
character_width = 50
character_height = 50
character_image = pygame.transform.scale(character_image, (character_width, character_height))

# 화면 분할 비율 설정 (오른쪽 분할 제거)
left_view_width = screen_width  # 전체 화면을 왼쪽 화면으로 설정

# 캐릭터 위치 (고정된 위치 설정)
character_fixed_x = (left_view_width // 2) - (character_width // 2)  # 화면 중앙에 고정
character_fixed_y = 4 * (screen_height // 5) - (character_height // 2)

# 왼쪽 배경 이미지 로드 (원래 크기 유지)
try:
    background_image = pygame.image.load("./image/background.png").convert_alpha()
except pygame.error as e:
    print(f"왼쪽 배경 이미지를 로드할 수 없습니다: {e}")
    pygame.quit()
    sys.exit()

# 배경 이미지 크기
background_width, background_height = background_image.get_size()

central_x = (background_width - screen_width) / 2
top_y = 0

# 카메라 이동 속도 (초당 픽셀 수)
camera_speed = 300  # 예: 300 pixels per second

# 카메라 이동 제한 설정
max_camera_x = background_width - screen_width
max_camera_y = background_height - screen_height

camera_x = central_x
camera_y = max_camera_y

# 카메라 이동 애니메이션 변수 초기화
camera_moving = False
camera_target_x = camera_x
camera_target_y = camera_y

# 버튼 클래스 정의
class Button:
    def __init__(self, text, pos, size, bg_color, text_color, hover_color=None, clicked_color=None):
        self.text = text
        self.pos = pos  # (x, y)
        self.size = size  # (width, height)
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color if hover_color else bg_color
        self.clicked_color = clicked_color if clicked_color else bg_color
        self.current_color = bg_color
        self.rect = pygame.Rect(pos, size)
        self.text_surf = button_font.render(text, True, text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.clicked = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect)
        surface.blit(self.text_surf, self.text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.bg_color

buttons = []
def update_buttons():
    global buttons, button_texts
    if current_stage == 1:
        button_texts = ["선택지 1", "선택지 2", "선택지 3", "선택지 4"]
    elif current_stage == 2:
        button_texts = ["스테이지 2 - 선택지 1", "스테이지 2 - 선택지 2", "스테이지 2 - 선택지 3", "스테이지 2 - 선택지 4"]
    elif current_stage == 3:
        button_texts = ["스테이지 3 - 선택지 1", "스테이지 3 - 선택지 2", "스테이지 3 - 선택지 3", "스테이지 3 - 선택지 4"]

    buttons.clear()
    button_width = 200
    button_height = 40
    button_gap = 20
    button_start_x = (screen_width - button_width) // 2
    button_start_y = 100

    for i, text in enumerate(button_texts):
        btn_x = button_start_x
        btn_y = button_start_y + i * (button_height + button_gap)
        button = Button(
            text=text,
            pos=(btn_x, btn_y),
            size=(button_width, button_height),
            bg_color=(70, 130, 180),
            text_color=WHITE,
            hover_color=(100, 149, 237),
            clicked_color=(25, 25, 112)
        )
        buttons.append(button)
update_buttons()

# 이동 큐 초기화
movement_queue = deque()

# 버튼 클릭 시 카메라 이동 또는 게임 시작 함수 정의
def start_avoid_star_game():
    global current_game_state
    print("Avoid Star 게임을 시작합니다.")
    avoid_star_game.reset_to_main()  # 게임 초기화
    current_game_state = "avoid_star"

def start_image_puzzle_game():
    global current_game_state
    print("이미지 퍼즐 게임을 시작합니다.")
    image_puzzle_game.reset_to_main()  # 게임 초기화
    current_game_state = "image_puzzle"

def move_camera(direction, amount=30):
    movement_queue.append(("camera_move", direction, amount))

def start_game(game_type):
    if game_type == "avoid_star":
        start_avoid_star_game()
    elif game_type == "image_puzzle":
        start_image_puzzle_game()

# 카메라 이동 애니메이션 처리 함수
def process_camera_move(delta_time):
    global camera_x, camera_y, camera_moving, camera_target_x, camera_target_y

    if camera_moving:
        # X 축 이동
        if camera_x < camera_target_x:
            camera_x += camera_speed * delta_time
            if camera_x > camera_target_x:
                camera_x = camera_target_x
        elif camera_x > camera_target_x:
            camera_x -= camera_speed * delta_time
            if camera_x < camera_target_x:
                camera_x = camera_target_x
        # Y 축 이동
        if camera_y < camera_target_y:
            camera_y += camera_speed * delta_time
            if camera_y > camera_target_y:
                camera_y = camera_target_y
        elif camera_y > camera_target_y:
            camera_y -= camera_speed * delta_time
            if camera_y < camera_target_y:
                camera_y = camera_target_y
        # 이동 완료 시 멈춤
        if camera_x == camera_target_x and camera_y == camera_target_y:
            camera_moving = False

# 이동 큐 처리 함수
def process_movement(delta_time):
    global camera_moving, camera_target_x, camera_target_y, current_game_state
    if movement_queue and not camera_moving:
        current_move = movement_queue.popleft()
        if current_move[0] == "camera_move":
            _, direction, amount = current_move
            # 카메라 이동 설정
            if direction == "down":
                target_y = camera_y + amount
                target_y = min(target_y, max_camera_y)
                camera_target_y = target_y
                camera_target_x = camera_x
            elif direction == "up":
                target_y = camera_y - amount
                target_y = max(target_y, 0)
                camera_target_y = target_y
                camera_target_x = camera_x
            elif direction == "left":
                target_x = camera_x - amount
                target_x = max(target_x, 0)
                camera_target_x = target_x
                camera_target_y = camera_y
            elif direction == "right":
                target_x = camera_x + amount
                target_x = min(target_x, max_camera_x)
                camera_target_x = target_x
                camera_target_y = camera_y
            elif direction == "reset":
                camera_target_x = central_x
                camera_target_y = top_y
            else:
                print(f"알 수 없는 방향: {direction}")
                return  # 알 수 없는 방향이면 무시

            # 이동 시작
            camera_moving = True
        elif current_move[0] == "start_game":
            _, game_type = current_move
            start_game(game_type)

    # 카메라 이동 처리
    if camera_moving:
        process_camera_move(delta_time)

# 버튼 클릭 시 카메라 이동 또는 게임 시작 함수 정의
def handle_button_click(index):
    if index == 0:  # 첫 번째 버튼
        move_camera("left", 430)
        move_camera("up", 270)
        movement_queue.append(("start_game", "avoid_star"))
    elif index == 1:  # 두 번째 버튼
        move_camera("left", 210)
        move_camera("up", 270)
        movement_queue.append(("start_game", "image_puzzle"))
    elif index == 2:  # 세 번째 버튼
        move_camera("left", 150)
    elif index == 3:  # 네 번째 버튼
        move_camera("right", 150)

def reset_position():
    global camera_x, camera_y, camera_moving, camera_target_x, camera_target_y
    # 카메라 초기화
    camera_x = central_x
    camera_y = max_camera_y
    camera_target_x = central_x
    camera_target_y = max_camera_y
    camera_moving = False  # 이동 애니메이션 중지

# 스테이지 초기화 함수
def reset_to_main():
    global current_stage
    if current_stage < max_stages:
        current_stage += 1
        update_top_text()
        update_buttons()
        reset_position()
    else:
        print("모든 스테이지를 완료했습니다! 축하합니다!")
        pygame.quit()
        sys.exit()

# AvoidStarGame 인스턴스 생성
avoid_star_game = avoid_star.AvoidStarGame(screen, screen_width, screen_height, font, character_image)

# ImagePuzzleGame 인스턴스 생성
image_puzzle_game = image_puzzle.ImagePuzzleGame(screen, screen_width, screen_height, font)

# 게임 루프 제어를 위한 변수
running = True
clock = pygame.time.Clock()

# 게임 상태 변수
current_game_state = "main"  # "main", "avoid_star", 또는 "image_puzzle"

# 게임 루프
while running:
    # delta_time 계산 (초 단위)
    delta_time = clock.tick(60) / 1000.0  # 60 FPS 기준

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 왼쪽 마우스 클릭
            mouse_pos = event.pos
            if current_game_state == "main":
                # 패널이 표시되고 있을 때만 버튼 클릭을 처리
                # 카메라가 모두 이동 중이지 않고, 패널이 표시될 때
                central_x_threshold = 5  # 허용 오차
                camera_y_threshold = 5  # 허용 오차
                if (abs(camera_x - central_x) < central_x_threshold and
                    abs(camera_y - top_y - 360) < camera_y_threshold and
                    not camera_moving and
                    not movement_queue):
                    for i, button in enumerate(buttons):
                        if button.is_clicked(mouse_pos):
                            print(f"버튼 {i + 1}이 클릭되었습니다.")
                            handle_button_click(i)
            elif current_game_state == "avoid_star":
                pass  # Avoid Star 게임 내에서의 클릭 처리 (필요 시 추가)
            elif current_game_state == "image_puzzle":
                if image_puzzle_game.show_instructions:
                    image_puzzle_game.handle_event(event)
                elif image_puzzle_game.full_image:
                    image_puzzle_game.handle_click((mouse_pos[0], mouse_pos[1]))

    # 키 입력 처리
    keys = pygame.key.get_pressed()

    if current_game_state == "main":
        # 키보드 입력으로 카메라 이동 처리
        if keys[pygame.K_LEFT]:
            move_camera("left", 300 * delta_time)
        if keys[pygame.K_RIGHT]:
            move_camera("right", 300 * delta_time)
        if keys[pygame.K_UP]:
            move_camera("up", 300 * delta_time)
        if keys[pygame.K_DOWN]:
            move_camera("down", 300 * delta_time)

        # 카메라 위치 제한 (이미 move_camera 함수에서 처리)
        camera_x = max(0, min(camera_x, max_camera_x))
        camera_y = max(0, min(camera_y, max_camera_y))

        # 이동 큐 처리
        process_movement(delta_time)

    elif current_game_state == "avoid_star":
        # Avoid Star 게임 업데이트
        avoid_star_game.update(delta_time, keys)

        # Avoid Star 게임 내에서 키 입력 처리
        if keys[pygame.K_r] and avoid_star_game.game_over:
            avoid_star_game.reset_to_main()  # 게임 초기화
            current_game_state = "avoid_star"
        elif keys[pygame.K_RETURN] and avoid_star_game.game_complete:  # Enter 키로 메인 화면으로 복귀
            avoid_star_game.reset_to_main()  # 게임 상태 초기화
            reset_to_main()
            current_game_state = "main"  # 메인 화면으로 전환
    elif current_game_state == "image_puzzle":
        # 이미지 퍼즐 게임 업데이트
        image_puzzle_game.update(delta_time, keys)

        # 퍼즐 게임 내에서 키 입력 처리 (Enter 키로 메인 화면으로 복귀)
        if keys[pygame.K_RETURN] and image_puzzle_game.game_complete:
            image_puzzle_game.reset_to_main()
            reset_to_main()
            current_game_state = "main"

    # 화면 그리기
    if current_game_state == "main":
        screen.fill(WHITE)  # 전체 배경색 채우기

        # 배경 이미지 그리기 (카메라 위치에 따라)
        screen.blit(background_image, (0, 0), pygame.Rect(int(camera_x), int(camera_y), left_view_width, screen_height))

        # 패널 표시 조건
        # 카메라의 x가 중앙에, y가 최상단에 도달했는지 확인
        show_panel = False
        central_x_threshold = 5  # x가 중앙에 근접했는지 확인하는 허용 오차
        camera_y_threshold = 5  # y가 최상단에 근접했는지 확인하는 허용 오차
        if (abs(camera_x - central_x) < central_x_threshold and
            abs(camera_y - top_y - 360) < camera_y_threshold and
            not camera_moving and
            not movement_queue):
            show_panel = True

        if show_panel:
            # 패널 배경 그리기 (반투명 검은색)
            panel_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            panel_surface.fill((0, 0, 0, 180))  # RGBA, 마지막 값이 투명도
            screen.blit(panel_surface, (0, 0))

            # 상단 텍스트 그리기 (화면 중앙 상단)
            top_text_x = (screen_width - top_text_surface.get_width()) // 2
            top_text_y = 20
            screen.blit(top_text_surface, (top_text_x, top_text_y))

            # 버튼 그리기 및 업데이트
            mouse_pos = pygame.mouse.get_pos()
            for button in buttons:
                button.update(mouse_pos)
                button.draw(screen)

        # 캐릭터 그리기 (고정된 위치)
        screen.blit(character_image, (character_fixed_x, character_fixed_y))
    elif current_game_state == "avoid_star":
        # Avoid Star 게임 화면 그리기
        avoid_star_game.draw()
    elif current_game_state == "image_puzzle":
        # 이미지 퍼즐 게임 화면 그리기
        if image_puzzle_game.full_image:
            image_puzzle_game.draw()
        else:
            # 이미지 로드 실패 시 메시지 표시
            error_text = font.render("퍼즐 이미지를 로드할 수 없습니다.", True, WHITE)
            text_rect = error_text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(error_text, text_rect)

    # 화면 업데이트
    pygame.display.flip()

# 파이게임 종료
pygame.quit()
sys.exit()
