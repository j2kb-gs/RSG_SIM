from controller import Robot, Keyboard
from rsg_player_robot import TIME_STEP
from player1 import MyPlayer1
from player2 import MyPlayer2
from player3 import MyPlayer3
from player4 import MyPlayer4
import random

robot = Robot()
name = robot.getName()
robot_number = int(name[1])

# strategy = random.randint(1, 3)
# if strategy == 1:
#     print("Team Blue is playing a Defensive Strategy")
# elif strategy == 2:
#     print("Team Blue is playing an Offensive Strategy")
# else:
#     print("Team Blue is playing a Collaborative Strategy")


if robot_number == 1:
    robot_controller = MyPlayer1(robot)
    print("1")
elif robot_number == 2:
    robot_controller = MyPlayer2(robot)
    print("2")
else:
    robot_controller = MyPlayer3(robot)
    print("3")

robot_controller.run()
