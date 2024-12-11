import pygame
import sys

# 화면 크기 설정
screen_width = 800
screen_height = 600

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 게임 초기화
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("End Stage")
clock = pygame.time.Clock()

# 배경 이미지 로드
try:
    background_image = pygame.image.load("./image/home.png").convert()
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
except pygame.error as e:
    print(f"배경 이미지를 로드할 수 없습니다: {e}")
    pygame.quit()
    sys.exit()

# 캐릭터 설정
try:
    character_image = pygame.image.load("./image/character.png").convert_alpha()
    character_image = pygame.transform.scale(character_image, (50, 50))
except pygame.error as e:
    print(f"캐릭터 이미지를 로드할 수 없습니다: {e}")
    pygame.quit()
    sys.exit()

character_x = screen_width // 2 - 25
character_y = screen_height - 100
character_speed = 5
font_path = "ChosunCentennial_ttf.ttf"
# 버튼 설정
button_width = 400
button_height = 70
button_gap = 50
buttons = []
button_font = pygame.font.Font(font_path, 36)
button_texts = ["GIFT 1", "GIFT 2", "GIFT 3"]
button_messages = ["치킨 기프티콘 사진", "햄버거 기프티콘 사진", "베라 기프티콘 사진"]
button_images = ["./image/wood_button.png", "./image/wood_button.png", "./image/wood_button.png"]
buttons_visible = False
selected_message = None
enter_to_exit = False
panel_active = True
panel_text = "연주를 마치니 구석에 있던 보물상자가 열렸다 \n 상자에 가까이 가보자. \n \nENTER키를 누르시오."
second_panel_active = False
second_panel_text = "생일축하한다. \n \n THE END. \n\n ENTER키를 눌러 종료."

# 메시지 창 설정
message_box_width = screen_width * 3 // 4
message_box_height = screen_height * 3 // 4

# 버튼 생성 함수
def create_buttons():
    for i, (text, image_path) in enumerate(zip(button_texts, button_images)):
        x = (screen_width - button_width) // 2
        y = (screen_height // 2 - (len(button_texts) * (button_height + button_gap)) // 2) + i * (button_height + button_gap)
        button_rect = pygame.Rect(x, y, button_width, button_height)

        try:
            button_image = pygame.image.load(image_path).convert_alpha()
            button_image = pygame.transform.scale(button_image, (button_width, button_height))
        except pygame.error as e:
            print(f"버튼 이미지를 로드할 수 없습니다: {e}")
            button_image = None

        buttons.append((button_rect, text, button_image))

# 버튼 그리기 함수
def draw_buttons():
    for button_rect, text, button_image in buttons:
        if button_image:
            screen.blit(button_image, button_rect.topleft)
        else:
            pygame.draw.rect(screen, WHITE, button_rect)
            pygame.draw.rect(screen, BLACK, button_rect, 2)
        
        text_surface = button_font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

# 메시지 창 그리기 함수
def draw_message_box():
    box_x = (screen_width - message_box_width) // 2
    box_y = (screen_height - message_box_height) // 2
    pygame.draw.rect(screen, WHITE, (box_x, box_y, message_box_width, message_box_height))
    pygame.draw.rect(screen, BLACK, (box_x, box_y, message_box_width, message_box_height), 3)

    if selected_message:
        message_font = pygame.font.Font(font_path, 48)
        message_surface = message_font.render(selected_message, True, BLACK)
        message_rect = message_surface.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(message_surface, message_rect)

# 판넬 그리기 함수
def draw_panel():
    global panel_active
    if panel_active:
        panel_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        panel_surface.fill((0, 0, 0, 180))  # 반투명 검정색
        screen.blit(panel_surface, (0, 0))

        lines = panel_text.split("\n")
        for i, line in enumerate(lines):
            text_surface = button_font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + i * 50))
            screen.blit(text_surface, text_rect)

# 두 번째 판넬 그리기 함수
def draw_second_panel():
    global second_panel_active
    if second_panel_active:
        panel_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        panel_surface.fill((0, 0, 0, 180))  # 반투명 검정색
        screen.blit(panel_surface, (0, 0))

        lines = second_panel_text.split("\n")
        for i, line in enumerate(lines):
            text_surface = button_font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + i * 50))
            screen.blit(text_surface, text_rect)

# 메인 함수
def main():
    global character_x, character_y, buttons_visible, selected_message, enter_to_exit, panel_active, second_panel_active

    create_buttons()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if panel_active and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                panel_active = False

            elif second_panel_active and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pygame.quit()
                sys.exit()

            elif not panel_active and not second_panel_active:
                if event.type == pygame.MOUSEBUTTONDOWN and buttons_visible:
                    mouse_pos = event.pos
                    for i, (button_rect, text, button_image) in enumerate(buttons):
                        if button_rect.collidepoint(mouse_pos):
                            selected_message = button_messages[i]
                            buttons_visible = False
                            enter_to_exit = True
                            break

                if event.type == pygame.KEYDOWN and enter_to_exit and event.key == pygame.K_RETURN:
                    second_panel_active = True
                    enter_to_exit = False

        keys = pygame.key.get_pressed()

        if not buttons_visible and not enter_to_exit and not panel_active and not second_panel_active:
            if keys[pygame.K_LEFT]:
                character_x -= character_speed
            if keys[pygame.K_RIGHT]:
                character_x += character_speed
            if keys[pygame.K_UP]:
                character_y -= character_speed
            if keys[pygame.K_DOWN]:
                character_y += character_speed

            # 화면 경계 처리
            character_x = max(0, min(screen_width - 50, character_x))
            character_y = max(0, min(screen_height - 50, character_y))

            # 캐릭터가 위쪽 가운데에 도달하면 버튼 표시
            if (screen_width // 2 - 25 <= character_x <= screen_width // 2 + 25) and character_y <= 50:
                buttons_visible = True

        # 화면 그리기
        screen.blit(background_image, (0, 0))
        screen.blit(character_image, (character_x, character_y))

        if panel_active:
            draw_panel()
        elif second_panel_active:
            draw_second_panel()
        elif buttons_visible and not enter_to_exit:
            draw_buttons()
        elif enter_to_exit:
            draw_message_box()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
