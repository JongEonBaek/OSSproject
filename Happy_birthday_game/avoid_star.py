import pygame
import random

class AvoidStarGame:
    def __init__(self, screen, screen_width, screen_height, font, character_image):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.character_image = character_image  # 캐릭터 이미지

        # 게임 상태
        self.stars = []
        self.star_spawn_delay = 1000  # 밀리초 단위
        self.last_star_spawn_time = pygame.time.get_ticks()
        self.score = 0
        self.game_over = False
        self.game_complete = False  # 게임 완료 플래그

        # 추가된 상태 변수
        self.show_instructions = True  # 설명 박스 표시 여부

        # 배경 이미지 로드
        try:
            self.background_image = pygame.image.load("./image/star_background.png").convert_alpha()
            self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        except pygame.error as e:
            print(f"배경 이미지를 로드할 수 없습니다: {e}")
            self.background_image = None  # 배경 이미지가 없을 경우 검정색으로 채움

        # 별 이미지 로드
        try:
            self.star_image = pygame.image.load("./image/star.png").convert_alpha()
        except pygame.error as e:
            print(f"별 이미지를 로드할 수 없습니다: {e}")
            self.star_image = None

        # 별 크기 조정
        if self.star_image:
            self.star_width = 30
            self.star_height = 30
            self.star_image = pygame.transform.scale(self.star_image, (self.star_width, self.star_height))

        # 캐릭터 설정
        self.character_width = self.character_image.get_width()
        self.character_height = self.character_image.get_height()
        self.character_x = (self.screen_width - self.character_width) // 2
        self.character_y = self.screen_height - self.character_height - 10  # 바닥에서 10픽셀 위
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 300  # 초당 픽셀 수
        self.jump_speed = 600  # 점프 속도
        self.gravity = 1500  # 중력 가속도 (초당 제곱 픽셀)
        self.on_ground = True

        # 캐릭터 Rect 초기화
        self.character_rect = pygame.Rect(self.character_x, self.character_y, self.character_width, self.character_height)

    def spawn_star(self):
        if self.star_image:
            x = random.randint(0, self.screen_width - self.star_width)
            y = -self.star_height
            speed_y = random.randint(400, 600)  # 픽셀/초 (속도 증가)
            speed_x = 200  # 픽셀/초
            direction = 1  # 오른쪽으로 시작
            star_rect = pygame.Rect(x, y, self.star_width, self.star_height)
            star = {
                'rect': star_rect,
                'speed_y': speed_y,
                'speed_x': speed_x,
                'direction': direction,
                'state': 'falling',  # 'falling' 또는 'horizontal'
                'wall_hit_count': 0  # 벽 충돌 횟수
            }
            self.stars.append(star)

    def update(self, delta_time, keys):
        if self.game_over or self.game_complete:
            return

        if self.show_instructions:
            if keys[pygame.K_SPACE]:
                self.show_instructions = False
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_star_spawn_time > self.star_spawn_delay:
            self.spawn_star()
            self.last_star_spawn_time = current_time

        stars_to_remove = []

        # 별의 위치 업데이트
        for star in self.stars:
            if star['state'] == 'falling':
                star['rect'].y += star['speed_y'] * delta_time
                # 바닥에 닿으면 상태 변경
                if star['rect'].y >= self.screen_height - star['rect'].height - 10:
                    star['rect'].y = self.screen_height - star['rect'].height - 10
                    star['state'] = 'horizontal'
            elif star['state'] == 'horizontal':
                star['rect'].x += star['speed_x'] * star['direction'] * delta_time
                # 벽에 닿으면 방향 전환 또는 별 제거
                if star['rect'].x <= 0 or star['rect'].x >= self.screen_width - star['rect'].width:
                    star['wall_hit_count'] += 1
                    if star['wall_hit_count'] < 2:
                        # 방향 전환
                        if star['rect'].x <= 0:
                            star['rect'].x = 0
                        elif star['rect'].x >= self.screen_width - star['rect'].width:
                            star['rect'].x = self.screen_width - star['rect'].width
                        star['direction'] *= -1
                    else:
                        # 두 번 벽에 닿았으므로 별 제거
                        stars_to_remove.append(star)

        # 별 제거 및 점수 증가
        for star in stars_to_remove:
            if star in self.stars:
                self.stars.remove(star)
                self.score += 1  # 별이 사라질 때 점수 증가

                # 점수가 30점에 도달하면 게임 완료
                if self.score >= 25:
                    self.game_complete = True

        # 충돌 감지
        for star in self.stars:
            if self.character_rect.colliderect(star['rect']):
                self.game_over = True
                break

        # 캐릭터 이동 처리
        self.handle_movement(delta_time, keys)

    def handle_movement(self, delta_time, keys):
        # Horizontal movement
        self.velocity_x = 0
        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed

        # Jumping
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -self.jump_speed
            self.on_ground = False

        # Apply gravity
        if not self.on_ground:
            self.velocity_y += self.gravity * delta_time

        # Update position
        self.character_x += self.velocity_x * delta_time
        self.character_y += self.velocity_y * delta_time

        # Ground collision
        if self.character_y >= self.screen_height - self.character_height - 10:
            self.character_y = self.screen_height - self.character_height - 10
            self.velocity_y = 0
            self.on_ground = True

        # Boundary checks (전체 화면 내에서만 이동 가능)
        if self.character_x < 0:
            self.character_x = 0
        if self.character_x > self.screen_width - self.character_width:
            self.character_x = self.screen_width - self.character_width

        # Update character_rect
        self.character_rect.topleft = (self.character_x, self.character_y)

    def draw_instruction_box(self):
        # 반정도의 크기
        box_width = 3 * self.screen_width // 4
        box_height = 3 * self.screen_height // 4
        box_x = (self.screen_width - box_width) // 2
        box_y = (self.screen_height - box_height) // 2

        # 사각형 그리기 (반투명 흰색)
        box_color = (255, 255, 255, 220)  # RGBA
        instruction_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        instruction_surface.fill(box_color)

        # 게임 방법 텍스트
        instructions = [
            "2001년 12월 14일....",
            "작고 귀여운 아이가 하나 태어났다...",
            "그날의 기억을 들여다보자.",
            "남쪽하늘에는 궁수 자리가 반짝이고 있었지 음음...",
            "수많은 별똥별들이 내렸었지...",
            "소원을 빌고 눈을 뜬 순간",
            "별똥별이 내 쪽으로 오고 있다는 걸 알았지..",
            "",
            "<게임 설명>",
            "1. 화면에 떨어지는 별을 피하세요.",
            "2. 방향키를 통해 좌우로 움직일 수 있습니다.",
            "3. 점프는 SPACE 바를 사용합니다.",
            "4. 별과 충돌하지 않고 점수를 얻으세요.",
            "5. 점수가 25점에 도달하면 게임이 완료됩니다.",
            "",
            "게임을 시작하려면 SPACE 바를 누르세요.",
            "",
            "#게임 도중 너무 어려워 못하겠으면 P를 눌러 탈출#"
        ]

        # 텍스트 렌더링
        padding = 20
        for i, line in enumerate(instructions):
            text_surf = self.font.render(line, True, (0, 0, 0))
            instruction_surface.blit(text_surf, (padding, padding + i * 25))

        # 화면에 그리기
        self.screen.blit(instruction_surface, (box_x, box_y))

    def draw(self):
        # 배경 그리기
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill((0, 0, 0))  # 검정색 배경

        # 별 그리기
        if self.star_image:
            for star in self.stars:
                self.screen.blit(self.star_image, star['rect'])

        # 캐릭터 그리기
        self.screen.blit(self.character_image, (self.character_x, self.character_y))

        # 점수 표시
        WHITE = (255, 255, 255)
        score_text = self.font.render(f"점수: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))

        # 게임 오버 표시
        if self.game_over:
            game_over_text = self.font.render("게임 오버! R 키를 눌러 재시작.", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(game_over_text, text_rect)

        # 게임 완료 표시
        if self.game_complete:
            game_complete_text = self.font.render("축하합니다! Enter 키를 눌러 메인 화면으로 돌아갑니다.", True, (0, 255, 0))
            text_rect = game_complete_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(game_complete_text, text_rect)

        # 설명 박스 그리기
        if self.show_instructions:
            self.draw_instruction_box()

    def reset_to_main(self):
        self.stars.clear()
        self.score = 0
        self.game_over = False
        self.game_complete = False  # 게임 완료 플래그 초기화
        self.show_instructions = True  # 설명 박스 다시 표시
        self.last_star_spawn_time = pygame.time.get_ticks()
        # Reset character position
        self.character_x = (self.screen_width - self.character_width) // 2
        self.character_y = self.screen_height - self.character_height - 10
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = True
        self.character_rect.topleft = (self.character_x, self.character_y)
