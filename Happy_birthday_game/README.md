이 게임은 "생일축하 게임"으로 친구에게 그냥 선물을 주는 것이 아니라,
게임을 클리어하면 선물을 주고 싶어서 만들어봤습니다!

<파일 구성>
1. game_start.py :  게임시작화면으로 직접적으로 실행하는 파일입니다. ENTER를 누를 시 종료 후 main.py파일이 실행됩니다.
2. main.py : 메인 스테이지로 표지판에 도달 시 퀴즈를 맞추는 스테이지입니다. 총 3개의 퀴즈문제가 있습니다.
3. avoid_star.py : 별피하기 게임으로 하늘에서 떨어지는 별을 피하는 첫번 째 미니게임입니다.
4. image_puzzle.py : 친구이미지(예시로 별사진 넣어둠)를 넣어 3X3으로 그리드를 나누어 순서를 섞은다음 다시 원상복구하는 미니게임입니다.
5. rythm_game.py : 리듬게임으로 생일축하노래가 끝날 때까지 피아노건반을 두들겨 살아남는 미니게임입니다.
6. game_end.py : 게임 마지막 스테이지로, 보상을 선택할 수 있는 공간입니다. 상자의 접촉 시 보상(생일선물)을 선택하고 게임을 종료하게 됩니다!


퀴즈 3개, 미니게임 3개 이렇게 총 6개의 스테이지로 진행됩니다.

<흐름>
1. 게임시작을 하고 enter를 누르면 main_stage로 이동합니다.
2. 앞으로 직진해 표지판을 만나면 첫번째 퀴즈를 만납니다.
3. 퀴즈의 정답을 맞추면 이에 맞는 집으로 이동해, 미니게임을 시작합니다.
4. 퀴즈의 정답을 맞추지 못하면, 다시 원점으로 돌아갑니다.
5. 미니게임을 클리어하면 다음 메인 스테이지로 넘어갑니다.
6. 또다시 표지판을 만나면 두번 째 퀴즈가 있습니다.
7. 맞추면 미니게임 시작, 못맞추면 원점으로 돌아갑니다.
8. 두 번째 미니게임을 클리어 하면, 마지막 퀴즈를 맞춥니다.
9. 마지막 퀴즈를 맞추면 마지막 미니게임을 하게 되고, 이를 클리어시 선물의 방으로 이동합니다.
10. 선물의 방에서 보물상자에 접촉 시 3개의 보상중에 한개를 선택할 수 있습니다.
11. 각 보상마다 기프티콘 사진을 넣어둘 생각이며, 이렇게 게임이 종료됩니다.

Images provided by Freepik (https://www.freepik.com) under their free license.
