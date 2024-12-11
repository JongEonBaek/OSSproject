# main.py

import pygame
import sys
import os
import platform
import avoid_star  # avoid_star.py 모듈 가져오기

# 파이게임 초기화
pygame.init()

# 화면 크기 설정
screen_width = 750
screen_height = 750
screen = pygame.display.set_mode((screen_width, screen_height))

# 창 제목 설정
pygame.display.set_caption("화면 분할 및 카메라 이동")

# 색상 정의 (RGB)
WHITE = (255, 255, 255)
LEFT_COLOR = (173, 216, 230)   # 연한 파란색 (왼쪽 화면 배경 색)
RIGHT_COLOR = (0, 0, 0)  # 검은색 (오른쪽 화면)
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
    font = pygame.font.Font(font_path, 15)  # 상단 텍스트용 폰트, 크기 15
    button_font = pygame.font.Font(font_path, 30)  # 버튼용 폰트, 크기 30
except pygame.error as e:
    print(f"폰트를 로드할 수 없습니다: {e}")
    pygame.quit()
    sys.exit()

# 상단 텍스트 렌더링
top_text = "세상에서 제일 힘이 쎈 동물은>"
top_text_surface = font.render(top_text, True, WHITE)  # 흰색 텍스트

# 캐릭터 이미지 로드
try:
    character_image = pygame.image.load("character.png").convert_alpha()
except pygame.error as e:
    print(f"캐릭터 이미지를 로드할 수 없습니다: {e}")
    pygame.quit()
    sys.exit()

# 캐릭터 크기 조정 (필요 시)
character_width = 50
character_height = 50
character_image = pygame.transform.scale(character_image, (character_width, character_height))

# 화면 분할 비율 설정
left_view_width = (screen_width * 2) // 3  # 2/3
right_view_width = screen_width - left_view_width  # 1/3

# 캐릭터 위치 (메인 화면에서의 위치)
character_x = (left_view_width // 2) - (character_width // 2)  # 왼쪽 화면 중앙에 위치
character_y = 4 * (screen_height // 5) - (character_height // 2)

# 왼쪽 배경 이미지 로드 (원래 크기 유지)
try:
    background_image = pygame.image.load("left_background.png").convert_alpha()
except pygame.error as e:
    print(f"왼쪽 배경 이미지를 로드할 수 없습니다: {e}")
    pygame.quit()
    sys.exit()

# 배경 이미지 크기
background_width, background_height = background_image.get_size()

# 카메라(뷰포트) 설정
camera_x = 0
camera_y = 0

# 카메라 이동 속도 (초당 픽셀 수)
camera_speed = 300  # 예: 300 pixels per second

# 카메라 이동 제한 설정
max_camera_x = background_width - left_view_width
max_camera_y = background_height - screen_height

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

# 버튼 리스트 초기화
buttons = []
button_texts = ["선택지 1", "선택지 2", "선택지 3", "선택지 4", "선택지 5"]  # "별 피하기 게임 시작" 버튼 제거
button_width = 200
button_height = 40
button_gap = 20

# 오른쪽 화면의 시작 y 위치 계산
right_start_x = left_view_width + (right_view_width - button_width) // 2  # 오른쪽 화면 중앙 x
right_start_y = 100  # 상단 텍스트 아래 y 위치

for i, text in enumerate(button_texts):
    btn_x = left_view_width + (right_view_width - button_width) // 2
    btn_y = right_start_y + i * (button_height + button_gap)
    button = Button(
        text=text,
        pos=(btn_x, btn_y),
        size=(button_width, button_height),
        bg_color=(70, 130, 180),  # 스틸 블루
        text_color=WHITE,
        hover_color=(100, 149, 237),  # 커먼 블루
        clicked_color=(25, 25, 112)  # 미드나잇 블루
    )
    buttons.append(button)

# 버튼 클릭 시 카메라 이동 또는 게임 시작 함수 정의
def start_avoid_star_game():
    global current_game_state
    print("Avoid Star 게임을 시작합니다.")
    avoid_star_game.reset_to_main()  # 게임 초기화
    current_game_state = "avoid_star"

def move_camera(direction, amount=30):
    global camera_x, camera_y
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
        camera_target_x = 0
        camera_target_y = 0
    else:
        return  # 알 수 없는 방향

    # 애니메이션을 위해 타겟 위치 설정
    set_camera_target(camera_target_x, camera_target_y)

# 카메라 애니메이션 변수
camera_moving = False
camera_target_x = camera_x
camera_target_y = camera_y

def set_camera_target(target_x, target_y):
    global camera_moving, camera_target_x, camera_target_y
    camera_target_x = target_x
    camera_target_y = target_y
    camera_moving = True

def update_camera_move(delta_time):
    global camera_x, camera_y, camera_moving
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

# 버튼에 따른 동작 매핑
button_actions = {
    "선택지 1": start_avoid_star_game,  # "선택지 1"을 Avoid Star 게임 시작으로 변경
    "선택지 2": lambda: move_camera("up", 150),
    "선택지 3": lambda: move_camera("left", 150),
    "선택지 4": lambda: move_camera("right", 150),
    "선택지 5": lambda: move_camera("reset"),
}

# AvoidStarGame 인스턴스 생성 (수정됨)
avoid_star_game = avoid_star.AvoidStarGame(screen, screen_width, screen_height, font, character_image)

# 게임 루프 제어를 위한 변수
running = True
clock = pygame.time.Clock()

# 게임 상태 변수
current_game_state = "main"  # "main" 또는 "avoid_star"

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
                for button in buttons:
                    if button.is_clicked(mouse_pos):
                        print(f"'{button.text}' 버튼이 클릭되었습니다.")
                        # 버튼 클릭 시 수행할 동작을 실행
                        action = button_actions.get(button.text)
                        if action:
                            action()
            elif current_game_state == "avoid_star":
                pass  # 별 피하기 게임 내에서의 클릭 처리 (필요 시 추가)

    # 키 입력 처리
    keys = pygame.key.get_pressed()

    if current_game_state == "main":
        if keys[pygame.K_LEFT]:
            move_camera("left", 300 * delta_time)  # 추가: 키보드로 카메라 이동
        if keys[pygame.K_RIGHT]:
            move_camera("right", 300 * delta_time)
        if keys[pygame.K_UP]:
            move_camera("up", 300 * delta_time)
        if keys[pygame.K_DOWN]:
            move_camera("down", 300 * delta_time)

        # 카메라 위치 제한
        camera_x = max(0, min(camera_x, max_camera_x))
        camera_y = max(0, min(camera_y, max_camera_y))

        # 카메라 애니메이션 업데이트
        update_camera_move(delta_time)
    elif current_game_state == "avoid_star":
        # 별 피하기 게임 업데이트
        avoid_star_game.update(delta_time, keys)

        # 별 피하기 게임 내에서 키 입력 처리
        if keys[pygame.K_r] and avoid_star_game.game_over:
            avoid_star_game.reset_to_main()  # 게임 초기화
        elif keys[pygame.K_RETURN] and avoid_star_game.game_complete:  # Enter 키로 메인 화면으로 복귀
            avoid_star_game.reset_to_main()  # 게임 상태 초기화
            current_game_state = "main"  # 메인 화면으로 전환


    # 화면 그리기
    if current_game_state == "main":
        screen.fill(WHITE)  # 전체 배경색 채우기

        # 왼쪽 화면 배경 그리기 (카메라 뷰포트에 맞춰서)
        screen.blit(background_image, (0, 0), pygame.Rect(int(camera_x), int(camera_y), left_view_width, screen_height))

        # 오른쪽 화면 단색으로 채우기
        pygame.draw.rect(screen, RIGHT_COLOR, (left_view_width, 0, right_view_width, screen_height))

        # 상단 텍스트 그리기 (오른쪽 화면 중앙 상단)
        top_text_x = left_view_width + (right_view_width - top_text_surface.get_width()) // 2
        top_text_y = 20
        screen.blit(top_text_surface, (top_text_x, top_text_y))

        # 버튼 그리기 및 업데이트
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.update(mouse_pos)
            button.draw(screen)

        # 캐릭터 그리기 (고정된 위치)
        screen.blit(character_image, (character_x, character_y))
    elif current_game_state == "avoid_star":
        # 별 피하기 게임 화면 그리기
        avoid_star_game.draw()

    # 화면 업데이트
    pygame.display.flip()

# 파이게임 종료
pygame.quit()
sys.exit()

