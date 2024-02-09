from obstacles import Ground, EndGoal

# Level width includes max scroll plus screen width
level10Layout = {
  Ground(): (0, 450, 350, 50),
  Ground(): (0, 260, 700, 20),
  Ground(): (0, 200, 200, 40),
  Ground(): (250, 90, 5450, 20),
  Ground(): (450, 370, 350, 150),
  Ground(): (800, 450, 4900, 50),
  EndGoal(): (5600, 50, 20, 0)
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

level0 = [0, 5000, level0Layout]
level1 = [1, 5000, level1Layout]
level2 = [2, 5000, level2Layout]
level3 = [3, 5000, level3Layout]
level4 = [4, 5000, level4Layout]
level5 = [5, 5000, level5Layout]
level6 = [6, 5000, level6Layout]
level7 = [7, 5000, level7Layout]
level8 = [8, 5000, level8Layout]
level9 = [9, 5000, level9Layout]
level10 = [10, 5000, level10Layout]

levels = [level0, level1, level2, level3, level4, level5, level6, level7, level8, level9, level10]