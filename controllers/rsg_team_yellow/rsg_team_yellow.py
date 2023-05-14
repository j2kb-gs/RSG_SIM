from controller import Robot
from player1 import MyPlayer1
from player2 import MyPlayer2
from player3 import MyPlayer3


robot = Robot()
name = robot.getName()
robot_number = int(name[1])

if robot_number == 1:
    robot_controller = MyPlayer1(robot)
elif robot_number == 2:
    robot_controller = MyPlayer2(robot)
else:
    robot_controller = MyPlayer3(robot)

robot_controller.run()
