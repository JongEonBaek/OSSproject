import pygame
import sys

def main():
    # 화면 크기 설정
    screen_width = 800
    screen_height = 750

    # 색상 정의
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("End Stage")
    clock = pygame.time.Clock()

    font_path = "ChosunCentennial_ttf.ttf"
    button_font = pygame.font.Font(font_path, 36)
    message_font = pygame.font.Font(font_path, 36)  # 메시지용 폰트

    # 배경 및 캐릭터 이미지 로드(예외처리는 생략)
    background_image = pygame.image.load("./image/home.png").convert()
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    character_image = pygame.image.load("./image/character.png").convert_alpha()
    character_image = pygame.transform.scale(character_image, (50, 50))

    character_x = screen_width // 2 - 25
    character_y = screen_height - 100
    character_speed = 5

    # 버튼 관련 설정
    button_width = 500  # 기존보다 크게
    button_height = 100 # 기존보다 크게
    buttons = []
    button_texts = ["선물 확인하기"]

    # 이미지 대신 메시지 문자열
    button_messages = [
        "카카오톡 > 선물함 > 선물코드등록\n\n SZCKKJVEXP 등록\n\n 등록 후 ENTER"
        
    ]
    button_images = ["./image/wood_button.png"]

    buttons_visible = False
    selected_message = None
    enter_to_exit = False
    panel_active = True
    panel_text = "연주를 마치니 구석에 있던 보물상자가 열렸다 \n 상자에 가까이 가보자. \n \nENTER키를 누르시오."
    second_panel_active = False
    second_panel_text = "생일 축하한다!\n\n운환아 좋은 하루 되고 행복해라.\n[용사 힘멜]\n\nTHE END.\nENTER키를 눌러 종료."

    message_box_width = screen_width * 3 // 4
    message_box_height = screen_height * 3 // 4

    def create_buttons():
        # 하나의 버튼만 중앙에 배치
        for i, (text, image_path) in enumerate(zip(button_texts, button_images)):
            x = (screen_width - button_width) // 2
            y = (screen_height - button_height) // 2
            button_rect = pygame.Rect(x, y, button_width, button_height)
            try:
                button_image = pygame.image.load(image_path).convert_alpha()
                button_image = pygame.transform.scale(button_image, (button_width, button_height))
            except pygame.error:
                button_image = None
            buttons.append((button_rect, text, button_image))

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

    def draw_message_box():
        box_x = (screen_width - message_box_width) // 2
        box_y = (screen_height - message_box_height) // 2
        pygame.draw.rect(screen, WHITE, (box_x, box_y, message_box_width, message_box_height))
        pygame.draw.rect(screen, BLACK, (box_x, box_y, message_box_width, message_box_height), 3)

        if selected_message:
            # 메시지 문자열 렌더링
            lines = selected_message.split("\n")
            line_height = 50
            # 텍스트 시작 지점
            start_y = box_y + (message_box_height - (line_height * len(lines))) // 2
            for i, line in enumerate(lines):
                line_surface = message_font.render(line, True, BLACK)
                line_rect = line_surface.get_rect(center=(box_x + message_box_width // 2, start_y + i * line_height))
                screen.blit(line_surface, line_rect)

    def draw_panel():
        if panel_active:
            panel_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            panel_surface.fill((0, 0, 0, 180))
            screen.blit(panel_surface, (0, 0))
            lines = panel_text.split("\n")
            for i, line in enumerate(lines):
                text_surface = button_font.render(line, True, WHITE)
                text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + i * 50))
                screen.blit(text_surface, text_rect)

    def draw_second_panel():
        if second_panel_active:
            panel_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            panel_surface.fill((0, 0, 0, 180))
            screen.blit(panel_surface, (0, 0))

            lines = second_panel_text.split("\n")
            for i, line in enumerate(lines):
                text_surface = button_font.render(line, True, WHITE)
                text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + i * 50))
                screen.blit(text_surface, text_rect)

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
                # 엔딩 패널에서 Enter 키를 누르면 종료
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

                if event.type == pygame.KEYDOWN and enter_to_exit:
                    if event.key == pygame.K_RETURN:
                        second_panel_active = True
                        enter_to_exit = False

        keys = pygame.key.get_pressed()

        # 캐릭터 이동 및 버튼 표시 조건
        if not buttons_visible and not enter_to_exit and not panel_active and not second_panel_active:
            if keys[pygame.K_LEFT]:
                character_x -= character_speed
            if keys[pygame.K_RIGHT]:
                character_x += character_speed
            if keys[pygame.K_UP]:
                character_y -= character_speed
            if keys[pygame.K_DOWN]:
                character_y += character_speed

            character_x = max(0, min(screen_width - 50, character_x))
            character_y = max(0, min(screen_height - 50, character_y))

            # 캐릭터가 상단 중앙 근처 도달 시 버튼 표시
            if (screen_width // 2 - 25 <= character_x <= screen_width // 2 + 25) and character_y <= 50:
                buttons_visible = True

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

