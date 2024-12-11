import pygame
import random

class RhythmGame:
    def __init__(self, screen, screen_width, screen_height, font, character_image):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.character_image = character_image

        # 게임 상태 변수
        self.notes = []  # 리듬 노트 저장
        self.note_spawn_delay = 500  # 밀리초 단위
        self.last_note_spawn_time = pygame.time.get_ticks()
        self.score = 0
        self.game_over = False
        self.game_complete = False
        self.show_instructions = True  # 설명 박스 표시 여부

        # 타임리밋 설정
        self.time_limit = 45  # 초 단위 45
        self.start_time = None

        # 피아노 건반 설정
        self.keys = []  # 피아노 건반
        self.num_keys = 5
        self.key_width = self.screen_width // self.num_keys
        self.key_height = 100
        self.key_bindings = [pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v, pygame.K_b]
        for i in range(self.num_keys):
            self.keys.append(pygame.Rect(i * self.key_width, self.screen_height - self.key_height, self.key_width, self.key_height))

        # 캐릭터 설정
        self.character_width = self.character_image.get_width()
        self.character_height = self.character_image.get_height()
        self.character_x = 0
        self.character_y = 50  # 가로선에 위치

        # 배경 및 노트 이미지
        try:
            self.note_image = pygame.image.load("./image/star.png").convert_alpha()
            self.note_image = pygame.transform.scale(self.note_image, (self.key_width // 2, self.key_height // 2))
        except pygame.error as e:
            print(f"노트 이미지를 로드할 수 없습니다: {e}")
            self.note_image = None

        # 음악 설정
        try:
            pygame.mixer.init()
            self.background_music = "./music/song.mp3"
        except pygame.error as e:
            print(f"음악을 로드할 수 없습니다: {e}")
            self.background_music = None

    def play_music(self):
        if self.background_music:
            pygame.mixer.music.load(self.background_music)
            pygame.mixer.music.play(-1)  # 무한 반복

    def stop_music(self):
        if self.background_music:
            pygame.mixer.music.stop()

    def spawn_note(self):
        # 노트 생성 (랜덤한 건반 위치에 맞게 생성)
        key_index = random.randint(0, self.num_keys - 1)
        x = self.keys[key_index].centerx - (self.key_width // 4)
        y = -self.key_height // 2
        note_rect = pygame.Rect(x, y, self.key_width // 2, self.key_height // 2)
        self.notes.append({'rect': note_rect, 'key_index': key_index})

    def update(self, delta_time, keys):
        if self.show_instructions:
            if keys[pygame.K_RETURN]:
                self.show_instructions = False
                self.start_time = pygame.time.get_ticks()  # 타이머 시작
                self.play_music()  # ENTER를 눌러 게임이 시작되면 음악 재생
            return

        # 게임 오버 상태 처리
        if self.game_over or self.game_complete:
            self.stop_music()  # 게임 오버나 클리어 시 음악 멈춤
            return

        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000 if self.start_time else 0

        if elapsed_time >= self.time_limit:
            self.game_complete = True

        current_time = pygame.time.get_ticks()
        if current_time - self.last_note_spawn_time > self.note_spawn_delay:
            self.spawn_note()
            self.last_note_spawn_time = current_time

        # 노트 위치 업데이트
        notes_to_remove = []
        for note in self.notes:
            note['rect'].y += 300 * delta_time  # 노트가 내려오는 속도
            if note['rect'].y > self.screen_height:
                notes_to_remove.append(note)

        for note in notes_to_remove:
            self.notes.remove(note)
            self.game_over = True
            break  # 게임 오버 상태로 진입했으면 추가 처리를 중단

        # 캐릭터 움직임 업데이트
        self.character_x += 200 * delta_time  # 캐릭터가 가로선 위를 움직이는 속도
        if self.character_x > self.screen_width:
            self.character_x = 0

        # 키 입력 처리
        for event_key, key in enumerate(self.key_bindings):
            if keys[key]:
                for note in self.notes:
                    if note['key_index'] == event_key and self.keys[event_key].colliderect(note['rect']):
                        self.notes.remove(note)
                        self.score += 1
                        break

    def draw_instruction_box(self):
        # 설명 박스 그리기
        box_width = 3 * self.screen_width // 4
        box_height = 3 * self.screen_height // 4
        box_x = (self.screen_width - box_width) // 2
        box_y = (self.screen_height - box_height) // 2

        # 반투명 흰색 사각형
        box_color = (255, 255, 255, 220)  # RGBA
        instruction_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        instruction_surface.fill(box_color)

        # 게임 설명 텍스트
        instructions = [
            "방에 들어오니 피아노와 악보가 보인다.",
            "그래 내 어렸을 적 꿈은 피아니스트였지...",
            "연주해보시겠습니까? ",
            "",
            "<게임설명>",
            "1. 위에서 내려오는 음표들이 내려옵니다.",
            "2. 음표가 건반에 도착할 때 해당하는 키를 누르세요.",
            "3. 노래가 끝날때까지 살아있으면 clear!",
            "키 할당:",
            "Z, X, C, V, B",
            "게임을 시작하려면 ENTER를 누르세요."
        ]

        padding = 20
        for i, line in enumerate(instructions):
            text_surf = self.font.render(line, True, (0, 0, 0))
            instruction_surface.blit(text_surf, (padding, padding + i * 30))

        self.screen.blit(instruction_surface, (box_x, box_y))

    def draw(self):
        if self.show_instructions and not self.game_complete:
            self.screen.fill((0, 0, 0))  # 게임 화면으로 전환
            self.draw_instruction_box()
            return

        # 배경 그리기
        self.screen.fill((0, 0, 0))  # 검정색 배경

        # 피아노 건반 그리기
        for i, key in enumerate(self.keys):
            color = (255, 255, 255) if i % 2 == 0 else (200, 200, 200)  # 건반 색상
            pygame.draw.rect(self.screen, color, key)
            pygame.draw.rect(self.screen, (0, 0, 0), key, 2)  # 경계선

        # 노트 그리기
        for note in self.notes:
            if self.note_image:
                self.screen.blit(self.note_image, note['rect'].topleft)
            else:
                pygame.draw.ellipse(self.screen, (255, 0, 0), note['rect'])  # 노트 기본 도형

        # 캐릭터 그리기
        self.screen.blit(self.character_image, (self.character_x, self.character_y))

        # 점수 표시
        score_text = self.font.render(f"점수: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 20))

        # 타임리밋 표시
        if not self.game_over and self.start_time:
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000 if self.start_time else 0
            time_remaining = max(0, self.time_limit - elapsed_time)
            time_text = self.font.render(f"남은 시간: {int(time_remaining)}초", True, (255, 255, 255))
            self.screen.blit(time_text, (20, 50))

        # 게임 오버 표시
        if self.game_over:
            game_over_text = self.font.render("게임 오버! R을 눌러 재시작", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(game_over_text, text_rect)

        # 게임 클리어 표시
        if self.game_complete:
            game_complete_text = self.font.render("게임 클리어! Enter를 눌러 메인으로", True, (0, 255, 0))
            text_rect = game_complete_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(game_complete_text, text_rect)

    def reset_to_main(self):
        self.notes.clear()
        self.score = 0
        self.game_over = False
        self.game_complete = False
        self.show_instructions = True
        self.start_time = None
        self.character_x = 0
        self.stop_music()
