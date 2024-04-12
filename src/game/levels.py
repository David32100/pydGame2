from game.obstacles import Ground, EndGoal, Enemy, Text

# Level width includes max scroll plus screen width
level10Layout = {
  Text(): ["freesansbold.ttf", 30, "Hi", (0, 0, 0), [100, 100], 1, None],
  Ground(): [0, 450, 350, 50],
  Ground(): [0, 260, 700, 20],
  Ground(): [0, 200, 200, 60],
  Ground(): [250, 90, 5450, 20],
  Ground(): [450, 370, 350, 150],
  Ground(): [800, 450, 4900, 50],
  Ground(): [1000, 250, 100, 25],
  EndGoal(): [5600, 50, 20]
}

level0Layout = {}
level1Layout = {}
level2Layout = {}
level3Layout = {}
level4Layout = {}
level5Layout = {}
level6Layout = {}
level7Layout = {}

level8Layout = {
  Ground(): [0, 101, 140, 58], 
  Enemy(): [260, 120, 20, 62], 
  Ground(): [200, 180, 119, 41], 
  Ground(): [342, 239, 79, 45], 
  Ground(): [460, 382, 80, 56], 
  Ground(): [580, 320, 59, 39], 
  Ground(): [619, 239, 20, 82], 
  Ground(): [642, 162, 16, 198], 
  EndGoal(): [657, 116, 28], 
  Ground(): [639, 161, 57, 199], 
  Enemy(): [486, 322, 34, 61], 
  Enemy(): [239, 125, 59, 57], 
  Enemy(): [482, 182, 40, 18], 
  Text(): ['freesansbold.ttf', 30, "Shai's level!", (0, 0, 0), [357, 62], 1, None]
}

level9Layout = {
  Ground(): [128, 0, 32, 392],
  Ground(): [1, 461, 696, 37], 
  Ground(): [281, 443, 18, 17], 
  Ground(): [321, 402, 19, 58], 
  Ground(): [386, 363, 13, 96], 
  Ground(): [441, 322, 18, 141], 
  Ground(): [482, 284, 13, 179], 
  EndGoal(): [171, 303, 26], 
  Ground(): [543, 241, 15, 218]
}

level11Layout = {
  Ground(): [134, 180, 115, 40],
  Enemy(): [302, 202, 43, 40],
  Ground(): [270, 232, 103, 32],
  Enemy(): [409, 270, 59, 59],
  Ground(): [516, 340, 161, 96], 
  EndGoal(): [592, 293, 34]
}

level0 = [0, 5000, level0Layout, 100, 100]
level1 = [1, 5000, level1Layout, 100, 100]
level2 = [2, 5000, level2Layout, 100, 100]
level3 = [3, 5000, level3Layout, 100, 100]
level4 = [4, 5000, level4Layout, 100, 100]
level5 = [5, 5000, level5Layout, 100, 100]
level6 = [6, 5000, level6Layout, 100, 100]
level7 = [7, 5000, level7Layout, 100, 100]
level8 = [8, 0, level8Layout, 40, 40]
level9 = [9, 0, level9Layout, 100, 100]
level10 = [10, 5000, level10Layout, 140, 400]
level11 = [11, 0, level11Layout, 140, 130]

levels = [level0, level1, level2, level3, level4, level5, level6, level7, level8, level9, level10, level11]