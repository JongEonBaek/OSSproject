# 생일축하 게임 🎉

이 게임은 친구에게 선물을 단순히 주는 것이 아니라, 게임을 클리어해야 선물을 받을 수 있도록 설계된 "생일축하 게임"입니다!

---

## 파일 구성 📂

1. **`game_start.py`** : 게임 시작 화면을 담당하며, 이 파일을 실행하면 시작됩니다. `ENTER`를 누르면 종료 후 `main.py` 파일이 실행됩니다.
2. **`main.py`** : 메인 스테이지로, 표지판에 도달하면 퀴즈를 푸는 스테이지입니다. 총 3개의 퀴즈 문제가 포함되어 있습니다.
3. **`avoid_star.py`** : 별 피하기 게임으로, 하늘에서 떨어지는 별을 피하는 첫 번째 미니게임입니다.
4. **`image_puzzle.py`** : 친구의 이미지를 활용한 퍼즐 게임으로, 이미지를 3x3 그리드로 나눈 뒤 순서를 섞어 원상복구하는 미니게임입니다. (현재는 예시로 별 이미지를 사용)
5. **`rythm_game.py`** : 리듬 게임으로, 생일 축하 노래가 끝날 때까지 피아노 건반을 두드리며 살아남는 미니게임입니다.
6. **`game_end.py`** : 게임 마지막 스테이지로, 보상을 선택할 수 있는 공간입니다. 상자의 접촉 시 보상(생일선물)을 선택하고 게임을 종료하게 됩니다!

---

## 게임 흐름 🕹️

게임은 퀴즈 3개와 미니게임 3개로 구성되어 있으며, 총 6개의 스테이지로 진행됩니다.

1. **게임 시작**
   - `game_start.py` 실행 후, `ENTER`를 누르면 메인 스테이지로 이동합니다.

2. **첫 번째 퀴즈**
   - 앞으로 직진해 표지판을 만나면 첫 번째 퀴즈를 시작합니다.
   - 정답을 맞추면 해당 집으로 이동해 미니게임을 시작합니다.
   - 정답을 맞추지 못하면 원점으로 돌아갑니다.

3. **첫 번째 미니게임**
   - 별 피하기 게임(`avoid_star.py`)을 클리어하면 다음 메인 스테이지로 넘어갑니다.

4. **두 번째 퀴즈**
   - 다음 표지판에서 두 번째 퀴즈를 시작합니다.
   - 정답을 맞추면 미니게임을 시작하며, 틀리면 원점으로 돌아갑니다.

5. **두 번째 미니게임**
   - 퍼즐 게임(`image_puzzle.py`)을 클리어하면 마지막 메인 스테이지로 넘어갑니다.

6. **세 번째 퀴즈**
   - 마지막 표지판에서 세 번째 퀴즈를 맞춥니다.
   - 정답을 맞추면 마지막 미니게임을 시작합니다.

7. **마지막 미니게임**
   - 리듬 게임(`rythm_game.py`)을 클리어하면 선물의 방으로 이동합니다.

8. **선물의 방**
   - 보물상자에 접촉하면 3개의 보상 중 하나를 선택할 수 있습니다.
   - 각 보상에는 기프티콘 사진이 포함될 예정입니다.

---

## 게임의 목표 🎯

친구에게 재미있고 특별한 경험을 제공하며, 게임을 통해 선물을 받을 수 있는 감동을 선사하는 것입니다!

---
Images provided by Freepik (https://www.freepik.com) under their free license.

