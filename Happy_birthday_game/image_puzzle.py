# image_puzzle.py

import pygame
import sys
import random

class Tile:
    def __init__(self, image, correct_position, current_position):
        self.image = image
        self.correct_position = correct_position  # (row, col)
        self.current_position = current_position  # (row, col)

    def draw(self, surface, tile_size, offset_x, offset_y):
        row, col = self.current_position
        surface.blit(self.image, (offset_x + col * tile_size, offset_y + row * tile_size))

    def is_correct(self):
        return self.correct_position == self.current_position

class ImagePuzzleGame:
    def __init__(self, screen, screen_width, screen_height, font):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font

        # 게임 상태
        self.tiles = []
        self.empty_pos = (2, 2)  # 초기 빈 칸 위치 (마지막 그리드)
        self.tile_size = min(screen_width, screen_height) // 3
        self.game_over = False
        self.game_complete = False

        # 추가된 상태 변수
        self.show_instructions = True  # 설명 박스 표시 여부

        # 이미지 로드
        try:
            self.full_image = pygame.image.load("./image/김운환.png").convert_alpha()
            self.full_image = pygame.transform.scale(self.full_image, (self.tile_size * 3, self.tile_size * 3))
        except pygame.error as e:
            print(f"퍼즐 이미지를 로드할 수 없습니다: {e}")
            self.full_image = None

        if self.full_image:
            self.create_tiles()
            self.shuffle_tiles()

    def create_tiles(self):
        self.tiles.clear()
        for row in range(3):
            for col in range(3):
                if (row, col) != self.empty_pos:
                    rect = pygame.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
                    tile_image = self.full_image.subsurface(rect).copy()
                    tile = Tile(
                        image=tile_image,
                        correct_position=(row, col),
                        current_position=(row, col)
                    )
                    self.tiles.append(tile)

    def shuffle_tiles(self):
        # 섞기: 무작위로 빈 칸과 인접한 타일을 이동시키는 방식으로 섞음
        moves = ["up", "down", "left", "right"]
        for _ in range(100):
            move = random.choice(moves)
            self.move_empty(move, shuffle=True)

    def move_empty(self, direction, shuffle=False):
        row, col = self.empty_pos
        target = None
        if direction == "up" and row < 2:
            target = (row + 1, col)
        elif direction == "down" and row > 0:
            target = (row - 1, col)
        elif direction == "left" and col < 2:
            target = (row, col + 1)
        elif direction == "right" and col > 0:
            target = (row, col - 1)

        if target:
            # 빈 칸과 이동할 타일의 위치를 교환
            for tile in self.tiles:
                if tile.current_position == target:
                    tile.current_position = self.empty_pos
                    break
            self.empty_pos = target
            if not shuffle:
                self.check_completion()

    def handle_click(self, pos):
        if self.game_over or self.game_complete or self.show_instructions:
            return

        x, y = pos
        row = y // self.tile_size
        col = x // self.tile_size
        clicked_pos = (row, col)

        if self.is_adjacent(clicked_pos, self.empty_pos):
            # 클릭한 타일과 빈 칸을 교환
            for tile in self.tiles:
                if tile.current_position == clicked_pos:
                    tile.current_position = self.empty_pos
                    break
            self.empty_pos = clicked_pos
            self.check_completion()

    def is_adjacent(self, pos1, pos2):
        row1, col1 = pos1
        row2, col2 = pos2
        return (abs(row1 - row2) == 1 and col1 == col2) or (abs(col1 - col2) == 1 and row1 == row2)

    def check_completion(self):
        for tile in self.tiles:
            if not tile.is_correct():
                return
        self.game_complete = True

    def update(self, delta_time, keys):
        if self.game_complete:
            pass  # 게임 완료 상태에서 추가 동작 가능
        # 추가적인 업데이트 로직이 필요하다면 여기에 작성

    def draw_instruction_box(self):
        # 반정도의 크기
        box_width = 3*self.screen_width // 4
        box_height = 3* self.screen_height // 4
        box_x = (self.screen_width - box_width) // 2
        box_y = (self.screen_height - box_height) // 2

        # 사각형 그리기 (반투명 흰색)
        box_color = (255, 255, 255, 220)  # RGBA
        instruction_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        instruction_surface.fill(box_color)

        # 게임 방법 텍스트
        instructions = [
            "<백종언 일기장 중 일부..>"
            "2014년 3월.... ",
            "중학교에 입학한 나는 운환이를 만났다",
            "작고귀여운 밤톨 같은 녀석..첫인상이다.",
            "시간이 지나 2014-7월",
            "어느덧 운환이와 친해지게 되었다...",
            "운환아... 그 곳에서도 편안하지...?",
            "",
            "이는 백종언이 아끼는 당신의 사진이지만,",
            "불의의 사고로 손상되었다.",
            "이미지를 복원시켜 우리의 추억을 간직하자.",
            "",
            "<게임 설명>",
            "1. 8개의 이미지 조각과 하나의 빈 칸이 있습니다.",
            "2. 이미지 조각을 클릭하여 빈 칸으로 이동시킵니다.",
            "3. 조각을 올바른 순서로 맞추면 게임이 완료됩니다.",
            "게임을 시작하려면 '계속' 버튼을 누르세요.",
            "",
            "#게임 도중 너무 어려워 못하겠으면 P를 눌러 탈출#"
        ]

        # 텍스트 렌더링
        padding = 20
        for i, line in enumerate(instructions):
            text_surf = self.font.render(line, True, (0, 0, 0))
            instruction_surface.blit(text_surf, (padding, padding + i * 25))

        # '계속' 버튼 그리기
        button_width = 100
        button_height = 40
        button_x = (box_width - button_width) // 2
        button_y = box_height - button_height - 20
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(instruction_surface, (70, 130, 180), button_rect)  # 스틸 블루 버튼
        continue_text = self.font.render("계속", True, (255, 255, 255))
        continue_text_rect = continue_text.get_rect(center=button_rect.center)
        instruction_surface.blit(continue_text, continue_text_rect)

        # 화면에 그리기
        self.screen.blit(instruction_surface, (box_x, box_y))

    def handle_instruction_click(self, pos):
        # 박스 크기와 위치 (draw_instruction_box와 동일한 크기 설정)
        box_width = 3 * self.screen_width // 4
        box_height = 3 * self.screen_height // 4
        box_x = (self.screen_width - box_width) // 2
        box_y = (self.screen_height - box_height) // 2

        # '계속' 버튼 영역
        button_width = 100
        button_height = 40
        button_x = box_x + (box_width - button_width) // 2
        button_y = box_y + box_height - button_height - 20
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        # 클릭한 위치가 버튼 안에 있는지 확인
        if button_rect.collidepoint(pos):
            self.show_instructions = False  # 설명 박스 숨기기

    def draw(self):
        # 배경 그리기
        self.screen.fill((0, 0, 0))  # 검정색 배경

        # 타일 그리기
        for tile in self.tiles:
            tile.draw(self.screen, self.tile_size, 0, 0)

        # 게임 완료 메시지
        if self.game_complete:
            GREEN = (0, 255, 0)
            msg = "퍼즐 완료! Enter 키를 눌러 메인 화면으로 돌아갑니다."
            text_surf = self.font.render(msg, True, GREEN)
            text_rect = text_surf.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(text_surf, text_rect)

        # 설명 박스 그리기
        if self.show_instructions:
            self.draw_instruction_box()

    def reset_to_main(self):
        self.tiles.clear()
        self.empty_pos = (2, 2)
        self.game_over = False
        self.game_complete = False
        self.show_instructions = True  # 설명 박스 다시 표시
        if self.full_image:
            self.create_tiles()
            self.shuffle_tiles()
        

    # handle_keydown 메서드 제거
    # def handle_keydown(self, key):
    #     if key == pygame.K_RETURN and self.game_complete:
    #         self.reset_to_main()

    def handle_event(self, event):
        if self.show_instructions and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_instruction_click(event.pos)
