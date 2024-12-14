import pygame
import sys
import main_game as game_module# 기존 subprocess 대신 main.py를 import

# 화면 크기 설정
screen_width = 750
screen_height = 750

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSPARENT_BLACK = (0, 0, 0, 180)  # RGBA (흐림 정도 80%)

# 게임 초기화
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Start Stage")
clock = pygame.time.Clock()

# 배경 이미지 로드
try:
    background_image = pygame.image.load("./image/start_background.png").convert()
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
except pygame.error as e:
    print(f"배경 이미지를 로드할 수 없습니다: {e}")
    pygame.quit()
    sys.exit()

# 텍스트 설정
font_path = "ChosunCentennial_ttf.ttf"
font = pygame.font.Font(font_path, 50)
message = "ENTER 키를 눌러 시작하세요"
message_surface = font.render(message, True, (0, 0, 0))
message_rect = message_surface.get_rect(center=(screen_width // 2, screen_height - 70))

# 가운데 네모 텍스트 설정
center_message = "음음 그래, 운환아 생일을 축하한다.\n너를 위해 간단한 게임을 준비했으니,\n 열심히 해주면 고맙겠어.\n\n 간단히 설명하면 3개의 문제\n 3개의 미니게임으로 \n총 6개의 문제를 풀면 된단다.\n 화이팅"
center_font = pygame.font.Font(font_path, 23)

# 가운데 네모 설정
center_box_width = screen_width // 2
center_box_height = screen_height // 2
center_box_x = (screen_width - center_box_width) // 2
center_box_y = (screen_height - center_box_height) // 2


def render_multiline_text(text, font, color, rect):
    lines = text.split("\n")
    surfaces = []
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect(center=(rect.centerx, rect.top + (i + 1) * (font.size(line)[1] + 5)))
        surfaces.append((text_surface, text_rect))
    return surfaces


# 메인 함수
def main_game():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # ENTER 키를 누르면 main.py의 main() 호출
                    print("메인 게임을 시작합니다!")
                    pygame.quit()  # 현재 pygame 창 종료
                    game_module.main()  # main.py의 main() 함수 호출
                    sys.exit()  # game_start.py 종료

        # 화면 그리기
        screen.blit(background_image, (0, 0))

        # 가운데 네모 그리기
        box_surface = pygame.Surface((center_box_width, center_box_height), pygame.SRCALPHA)
        box_surface.fill(TRANSPARENT_BLACK)
        screen.blit(box_surface, (center_box_x, center_box_y))

        # 가운데 네모 텍스트 그리기
        center_box_rect = pygame.Rect(center_box_x, center_box_y, center_box_width, center_box_height)
        multiline_text_surfaces = render_multiline_text(center_message, center_font, WHITE, center_box_rect)
        for surface, rect in multiline_text_surfaces:
            screen.blit(surface, rect)

        # 하단 메시지 그리기
        screen.blit(message_surface, message_rect)

        # 화면 업데이트
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main_game()
