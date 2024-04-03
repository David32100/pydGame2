from game.obstacles import Ground, EndGoal, Enemy

# Level width includes max scroll plus screen width
level10Layout = {
  Ground(): [0, 450, 350, 50],
  Ground(): [0, 260, 700, 20],
  Ground(): [0, 200, 200, 60],
  Ground(): [250, 90, 5450, 20],
  Ground(): [450, 370, 350, 150],
  Ground(): [800, 450, 4900, 50],
  Ground(): [1000, 250, 100, 25],
  EndGoal(): [5600, 50, 20]
}

level11Layout = {
  Ground(): [134, 180, 115, 40],
  Ground(): [465, 246, 0, 0],
  Ground(): [270, 232, 103, 32],
  Enemy(): [302, 202, 43, 40],
  Enemy(): [409, 270, 59, 59],
  Ground(): [516, 340, 161, 96], 
  EndGoal(): [592, 293, 34]
}

level0Layout = {}
level1Layout = {}
level2Layout = {}
level3Layout = {}
level4Layout = {}
level5Layout = {}
level6Layout = {}
level7Layout = {}
level8Layout = {}
level9Layout = {}

level0 = [0, 5000, level0Layout, 100, 100]
level1 = [1, 5000, level1Layout, 100, 100]
level2 = [2, 5000, level2Layout, 100, 100]
level3 = [3, 5000, level3Layout, 100, 100]
level4 = [4, 5000, level4Layout, 100, 100]
level5 = [5, 5000, level5Layout, 100, 100]
level6 = [6, 5000, level6Layout, 100, 100]
level7 = [7, 5000, level7Layout, 100, 100]
level8 = [8, 5000, level8Layout, 100, 100]
level9 = [9, 5000, level9Layout, 100, 100]
level10 = [10, 5000, level10Layout, 140, 400]
level11 = [11, 0, level11Layout, 140, 130]

levels = [level0, level1, level2, level3, level4, level5, level6, level7, level8, level9, level10, level11]