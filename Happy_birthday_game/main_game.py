import pygame
import sys
import os
import platform
from collections import deque  # 이동 큐를 위해 deque 사용
import avoid_star  # avoid_star.py 모듈 가져오기
import image_puzzle  # image_puzzle.py 모듈 가져오기
import rythm_game
import game_end

# 전역 변수들
screen_width = 750
screen_height = 750
screen = None
name = '김운환'
birthday = "2001-12-14"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 폰트 경로 및 폰트 변수
font_path = None
button_font = None
font = None
image_puzzle_font = None
panel_font = None

panel_active = True  # 판 활성화 여부
panel_text = "앞에 표지판이 보인다 가보자.(Enter)"

current_stage = 1  # 현재 스테이지
max_stages = 3  # 총 스테이지 수
top_text = ""
top_text_surface = []
top_image = None
top_image_rect = None

character_image = None
character_width = 50
character_height = 50

# 왼쪽 배경 이미지
background_image = None
background_width = 0
background_height = 0

central_x = 0
top_y = 0
camera_x = 0
camera_y = 0
camera_speed = 300
max_camera_x = 0
max_camera_y = 0

camera_moving = False
camera_target_x = 0
camera_target_y = 0

movement_queue = deque()

buttons = []
button_texts = []

avoid_star_game = None
image_puzzle_game = None
rythm_game_game = None

current_game_state = "main"

character_fixed_x = 0
character_fixed_y = 0


class Button:
    def __init__(self, text, pos, size, bg_color, text_color, hover_color=None, clicked_color=None, image=None):
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
        self.image = None

        if image:
            try:
                # 이미지 로드 및 크기 조정
                self.image = pygame.image.load(image).convert_alpha()
                self.image = pygame.transform.scale(self.image, size)  # 버튼 크기에 맞게 조정
            except pygame.error as e:
                print(f"이미지를 로드할 수 없습니다: {e}")

    def draw(self, surface):
        if self.image:
            # 이미지가 있으면 이미지를 그립니다.
            surface.blit(self.image, self.rect.topleft)
        else:
            # 이미지가 없으면 배경색으로 그립니다.
            pygame.draw.rect(surface, self.current_color, self.rect)
        # 텍스트는 항상 위에 그립니다.
        surface.blit(self.text_surf, self.text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.bg_color


def set_panel_text(new_text):
    global panel_text, panel_active
    panel_text = new_text
    panel_active = True

def draw_panel():
    global panel_active, panel_text, screen, panel_font
    if panel_active:
        # 흐린 배경 생성
        panel_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        panel_surface.fill((0, 0, 0, 180))  # 투명한 검은색
        screen.blit(panel_surface, (0, 0))

        # 텍스트 렌더링
        lines = panel_text.split("\n")
        for i, line in enumerate(lines):
            text_surface = panel_font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + i * 50))
            screen.blit(text_surface, text_rect)


def update_top_text():
    global top_text, top_text_surface, top_image_rect, current_stage, name, birthday, top_image, font, screen_width
    # 단계별 텍스트 정의
    if current_stage == 1:
        top_text = name + "이의 생일은 " + birthday + "이다. \n이 생일은 어떤 별자리에 속하는가??"
    elif current_stage == 2:
        top_text = "백종언과 " + name + "이가 처음 만난 날은 2014년 3월이다. \n우리가 친해졌다고 느낀 시기는 언제인가??"
    elif current_stage == 3:
        top_text = "당신은 길거리 유명 기획사에게 밴드멤버로 캐스팅을 \n제안받았다.다음 중 어느 역할을 맡고 싶은가??"

    if top_image:
        top_image_rect = top_image.get_rect(center=(screen_width // 2, 70))  # 이미지 화면 중앙 상단 배치

    # 텍스트 렌더링 및 위치 계산
    lines = top_text.split("\n")
    surfaces = []
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, BLACK)
        text_x = top_image_rect.centerx - (text_surface.get_width() // 2)
        text_y = top_image_rect.centery - (len(lines) * (font.size(line)[1] + 5) // 2) + i * (font.size(line)[1] + 5)
        surfaces.append((text_surface, (text_x, text_y)))

    top_text_surface = surfaces
    return top_text_surface


def update_buttons():
    global buttons, button_texts, current_stage, screen_width, button_font, BLACK
    if current_stage == 1:
        button_texts = ["궁수자리", "쌍둥이자리", "처녀자리", "물병자리"]
        button_images = [
            "./image/wood_button.png",
            "./image/wood_button.png",
            "./image/wood_button.png",
            "./image/wood_button.png"
        ]
    elif current_stage == 2:
        button_texts = ["2014년 7월", "2014년 3월", "2014년 7월", "2014년 4월"]
        button_images = [
            "./image/wood_button.png",
            "./image/wood_button.png",
            "./image/wood_button.png",
            "./image/wood_button.png"
        ]
    elif current_stage == 3:
        button_texts = ["기타", "드럼", "트럼펫", "피아노"]
        button_images = [
            "./image/wood_button.png",
            "./image/wood_button.png",
            "./image/wood_button.png",
            "./image/wood_button.png"
        ]

    buttons.clear()
    button_width = 700
    button_height = 90
    button_gap = 40
    button_start_x = (screen_width - button_width) // 2
    button_start_y = 190

    for i, text in enumerate(button_texts):
        btn_x = button_start_x
        btn_y = button_start_y + i * (button_height + button_gap)
        button = Button(
            text=text,
            pos=(btn_x, btn_y),
            size=(button_width, button_height),
            bg_color=(70, 130, 180),
            text_color=BLACK,
            hover_color=(100, 149, 237),
            clicked_color=(25, 25, 112),
            image=button_images[i]  # 이미지 경로 전달
        )
        buttons.append(button)


def process_camera_move(delta_time):
    global camera_x, camera_y, camera_moving, camera_target_x, camera_target_y, camera_speed
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


def process_movement(delta_time):
    global camera_moving, camera_target_x, camera_target_y, movement_queue
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


def move_camera(direction, amount=30):
    global movement_queue
    movement_queue.append(("camera_move", direction, amount))


def start_avoid_star_game():
    global current_game_state, avoid_star_game
    print("Avoid Star 게임을 시작합니다.")
    avoid_star_game.reset_to_main()  # 게임 초기화
    current_game_state = "avoid_star"


def start_image_puzzle_game():
    global current_game_state, image_puzzle_game
    print("이미지 퍼즐 게임을 시작합니다.")
    image_puzzle_game.reset_to_main()  # 게임 초기화
    current_game_state = "image_puzzle"


def start_rythm_game():
    global current_game_state, rythm_game_game
    print("리듬 게임을 시작합니다.")
    rythm_game_game.reset_to_main()  # 게임 초기화
    current_game_state = "rythm_game"


def start_game(game_type):
    if game_type == "avoid_star":
        start_avoid_star_game()
    elif game_type == "image_puzzle":
        start_image_puzzle_game()
    elif game_type == "rythm_game":
        start_rythm_game()


def handle_button_click(index):
    global current_stage
    if index == 0:  # 첫 번째 버튼
        if current_stage == 1:
            move_camera("left", 430) # 430
            move_camera("up", 270) # 270
            movement_queue.append(("start_game", "avoid_star"))
        else:
            wronganswer()
    elif index == 1:  # 두 번째 버튼
        wronganswer()
    elif index == 2:  # 세 번째 버튼
        if current_stage == 2:
            move_camera("right", 185)
            move_camera("up", 270)
            movement_queue.append(("start_game", "image_puzzle"))
        else:
            wronganswer()
    elif index == 3:  # 네 번째 버튼
        if current_stage == 3:
            move_camera("right", 420)
            move_camera("up", 270)
            movement_queue.append(("start_game", "rythm_game"))
        else:
            wronganswer()


def wronganswer():
    global camera_x, camera_y, camera_target_x, camera_target_y, camera_moving, screen
    print("갈!")
    wrong_message = True
    message_font = pygame.font.Font(font_path, 50)
    message_surface = message_font.render("갈!", True, (255, 0, 0))
    message_rect = message_surface.get_rect(center=(screen_width // 2, screen_height // 2))

    target_x = central_x
    target_y = max_camera_y
    camera_moving = True

    clock = pygame.time.Clock()
    while camera_moving:
        delta_time = clock.tick(60) / 1000.0
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0), pygame.Rect(int(camera_x), int(camera_y), screen_width, screen_height))

        # 카메라 이동 처리
        if camera_x < target_x:
            camera_x += camera_speed * delta_time
            if camera_x > target_x:
                camera_x = target_x
        elif camera_x > target_x:
            camera_x -= camera_speed * delta_time
            if camera_x < target_x:
                camera_x = target_x

        if camera_y < target_y:
            camera_y += camera_speed * delta_time
            if camera_y > target_y:
                camera_y = target_y
        elif camera_y > target_y:
            camera_y -= camera_speed * delta_time
            if camera_y < target_y:
                camera_y = target_y

        if camera_x == target_x and camera_y == target_y:
            camera_moving = False

        if wrong_message:
            screen.blit(message_surface, message_rect)

        screen.blit(character_image, (character_fixed_x, character_fixed_y))
        pygame.display.flip()

    wrong_message = False
    pygame.display.flip()


def reset_position():
    global camera_x, camera_y, camera_moving, camera_target_x, camera_target_y, central_x, max_camera_y
    camera_x = central_x
    camera_y = max_camera_y
    camera_target_x = central_x
    camera_target_y = max_camera_y
    camera_moving = False


def reset_to_main():
    global current_stage, panel_active
    if current_stage < max_stages:
        current_stage += 1
        update_top_text()
        update_buttons()
        reset_position()
        if(current_stage == 2):
            set_panel_text("후 별맞아 죽을 뻔했네. 다시 앞으로 가보자")
        elif(current_stage == 3):
            set_panel_text("추억이 떠오른다. 마지막 표지판으로 가보자")
    else:
        print("모든 스테이지를 완료했습니다! 축하합니다!")
        game_end.main()
        # pygame.quit()
        # sys.exit


def main():
    global screen, name, birthday, font_path, font, button_font, image_puzzle_font, panel_font
    global top_image, top_image_rect, background_image, background_width, background_height
    global central_x, top_y, camera_x, camera_y, camera_target_x, camera_target_y, max_camera_x, max_camera_y
    global character_image, character_fixed_x, character_fixed_y
    global avoid_star_game, image_puzzle_game, rythm_game_game
    global current_game_state
    global panel_active

    # 파이게임 초기화
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))

    # 창 제목 설정
    pygame.display.set_caption("Happy Birthday " + name + "!")

    # 운영체제에 따라 폰트 경로 설정
    if platform.system() == "Windows":
        font_path = "C:\\Windows\\Fonts\\BRITANIC.ttf"
    elif platform.system() == "Darwin":  # macOS
        font_path = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
    else:  # Linux 등
        font_path = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"

    local_font_path = "ChosunCentennial_ttf.ttf"
    if os.path.exists(local_font_path):
        font_path = local_font_path

    if not os.path.exists(font_path):
        print(f"폰트 파일을 찾을 수 없습니다: {font_path}")
        pygame.quit()
        sys.exit()

    try:
        font = pygame.font.Font(font_path, 30)
        button_font = pygame.font.Font(font_path, 35)
        image_puzzle_font = pygame.font.Font(font_path, 25)
        panel_font = pygame.font.Font(font_path, 40)
    except pygame.error as e:
        print(f"폰트를 로드할 수 없습니다: {e}")
        pygame.quit()
        sys.exit()

    # 상단 이미지 로드
    try:
        top_image = pygame.image.load("./image/wood_title.png").convert_alpha()
        top_image = pygame.transform.scale(top_image, (700, 140))
    except pygame.error as e:
        print(f"상단 이미지를 로드할 수 없습니다: {e}")
        top_image = None

    update_top_text()

    # 캐릭터 이미지 로드
    try:
        character_image_local = pygame.image.load("./image/character.png").convert_alpha()
    except pygame.error as e:
        print(f"캐릭터 이미지를 로드할 수 없습니다: {e}")
        pygame.quit()
        sys.exit()
    character_image = pygame.transform.scale(character_image_local, (character_width, character_height))

    # 배경 이미지 로드
    try:
        background_image_local = pygame.image.load("./image/background.png").convert_alpha()
    except pygame.error as e:
        print(f"왼쪽 배경 이미지를 로드할 수 없습니다: {e}")
        pygame.quit()
        sys.exit()

    background_image = background_image_local
    background_width, background_height = background_image.get_size()

    central_x = (background_width - screen_width) / 2
    top_y = 0
    camera_x = central_x
    camera_y = background_height - screen_height
    camera_target_x = camera_x
    camera_target_y = camera_y
    max_camera_x = background_width - screen_width
    max_camera_y = background_height - screen_height

    character_fixed_x = (screen_width // 2) - (character_width // 2)
    character_fixed_y = 4 * (screen_height // 5) - (character_height // 2)

    update_buttons()

    # 게임 인스턴스 생성
    avoid_star_game = avoid_star.AvoidStarGame(screen, screen_width, screen_height, image_puzzle_font, character_image)
    image_puzzle_game = image_puzzle.ImagePuzzleGame(screen, screen_width, screen_height, image_puzzle_font)
    rythm_game_game = rythm_game.RhythmGame(screen, screen_width, screen_height, image_puzzle_font, character_image)

    running = True
    clock = pygame.time.Clock()

    while running:
        delta_time = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and panel_active:
                    # 엔터로 패널 닫기
                    
                    panel_active = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if current_game_state == "main":
                    central_x_threshold = 5
                    camera_y_threshold = 5
                    if (abs(camera_x - central_x) < central_x_threshold and
                        abs(camera_y - top_y - 360) < camera_y_threshold and
                        not camera_moving and
                        not movement_queue):
                        for i, button in enumerate(buttons):
                            if button.is_clicked(mouse_pos):
                                print(f"버튼 {i + 1}이 클릭되었습니다.")
                                handle_button_click(i)
                elif current_game_state == "image_puzzle":
                    if image_puzzle_game.show_instructions:
                        image_puzzle_game.handle_event(event)
                    elif image_puzzle_game.full_image:
                        image_puzzle_game.handle_click((mouse_pos[0], mouse_pos[1]))

        keys = pygame.key.get_pressed()

        if not panel_active and current_game_state == "main":
            if keys[pygame.K_UP]:
                move_camera("up", 300 * delta_time)
            if keys[pygame.K_DOWN]:
                move_camera("down", 300 * delta_time)

            process_movement(delta_time)

        elif current_game_state == "avoid_star":
            avoid_star_game.update(delta_time, keys)
            if keys[pygame.K_r] and avoid_star_game.game_over:
                avoid_star_game.reset_to_main()
                current_game_state = "avoid_star"
            elif keys[pygame.K_RETURN] and avoid_star_game.game_complete:
                avoid_star_game.reset_to_main()
                reset_to_main()
                current_game_state = "main"
            elif keys[pygame.K_p]:
                avoid_star_game.game_complete = True
                avoid_star_game.reset_to_main()
                reset_to_main()
                current_game_state = "main"

        elif current_game_state == "image_puzzle":
            image_puzzle_game.update(delta_time, keys)
            if keys[pygame.K_RETURN] and image_puzzle_game.game_complete:
                image_puzzle_game.reset_to_main()
                reset_to_main()
                current_game_state = "main"
            elif keys[pygame.K_p]:
                image_puzzle_game.game_complete = True
                image_puzzle_game.reset_to_main()
                reset_to_main()
                current_game_state = "main"

        elif current_game_state == "rythm_game":
            rythm_game_game.update(delta_time, keys)
            if keys[pygame.K_r] and rythm_game_game.game_over:
                rythm_game_game.reset_to_main()
                current_game_state = "rythm_game"
            elif keys[pygame.K_RETURN] and rythm_game_game.game_complete:
                rythm_game_game.reset_to_main()
                reset_to_main()
                current_game_state = "main"
            elif keys[pygame.K_p]:
                rythm_game_game.game_complete = True
                rythm_game_game.reset_to_main()
                reset_to_main()
                current_game_state = "main"

        # 화면 그리기
        if current_game_state == "main":
            screen.fill(WHITE)
            screen.blit(background_image, (0, 0), pygame.Rect(int(camera_x), int(camera_y), screen_width, screen_height))

            if panel_active:
                draw_panel()

            show_panel = False
            central_x_threshold = 5
            camera_y_threshold = 5
            if (abs(camera_x - central_x) < central_x_threshold and
                abs(camera_y - top_y - 360) < camera_y_threshold and
                not camera_moving and
                not movement_queue):
                show_panel = True

            if show_panel:
                panel_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
                panel_surface.fill((0, 0, 0, 180))
                screen.blit(panel_surface, (0, 0))

                if top_image:
                    screen.blit(top_image, top_image_rect)

                for surface, pos in top_text_surface:
                    screen.blit(surface, pos)

                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    button.update(mouse_pos)
                    button.draw(screen)

            screen.blit(character_image, (character_fixed_x, character_fixed_y))
        elif current_game_state == "avoid_star":
            avoid_star_game.draw()
        elif current_game_state == "image_puzzle":
            if image_puzzle_game.full_image:
                image_puzzle_game.draw()
            else:
                error_text = font.render("퍼즐 이미지를 로드할 수 없습니다.", True, WHITE)
                text_rect = error_text.get_rect(center=(screen_width // 2, screen_height // 2))
                screen.blit(error_text, text_rect)
        elif current_game_state == "rythm_game":
            rythm_game_game.draw()

        pygame.display.flip()


if __name__ == "__main__":
    main()
