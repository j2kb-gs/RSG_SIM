# - ROBOT PLAYER 1

import math  # noqa: F401
import utils
import consts
from rsg_player_robot import RSGPlayerRobot, TIME_STEP
from controller import Keyboard

"""
Player 1 has a defensive role: 
    - chase the ball when the ball is in range and try to score
    - give up the ball when another team player is already on the ball in offense zone
    - get back to the defense zone when it can't see the ball

    `heading`
        pi
-pi/2   .   pi/2
        0
* abs(heading) > 2 means player is facing opponents goal  
* abs(heading) < 0.7 means player is facing its own goal  
"""


class MyPlayer1(RSGPlayerRobot):

    def back_dir(self, robot_pos):
        if -.35 <= robot_pos[0] <= .35:
            return 0
        return -1 if robot_pos[0] < 0 else 1

    def run(self):
        # self.keyboard = RSGPlayerRobot.getKeyboard()
        # self.keyboard.enable(TIME_STEP * 10)
        while self.robot.step(TIME_STEP) != -1:

            if self.is_new_data():
                data = self.get_new_data()  # noqa: F841
                team_data = None

                # Get data from compass
                heading = self.get_compass_heading()  # noqa: F841

                # Get GPS coordinates of the robot
                robot_pos = self.get_gps_coordinates()  # noqa: F841

                # Get data from sonars
                sonar_values = self.get_sonar_values()  # noqa: F841

                # while True:
                #     key = self.keyboard.getKey()

                #     if key == Keyboard.LEFT:
                #         print("Yooooooooooo")

                while self.is_new_team_data():
                    team_data = self.get_new_team_data()  # noqa: F841
                    # Do something with team data

                if self.is_new_ball_data():
                    ball_data = self.get_new_ball_data()
                else:
                    # robot does not see the ball
                    # goes back to defense slowly
                    if robot_pos[1] <= 0.59:
                        if abs(heading) >= 2.4:
                            self.left_motor.setVelocity(-1)
                            self.right_motor.setVelocity(-1)

                        elif abs(heading) <= 0.7:
                            self.left_motor.setVelocity(1)
                            self.right_motor.setVelocity(1)
                        else:
                            # If robot facing its own gaal, rotate [scan for ball]
                            self.left_motor.setVelocity(1)
                            self.right_motor.setVelocity(-1)

                    else:
                        # If robot facing its own gaal, rotate [scan for ball]
                        self.left_motor.setVelocity(1)
                        self.right_motor.setVelocity(-1)

                    continue

                # Compute the speed for motors
                direction = utils.get_direction(ball_data["direction"])

                # If the robot has the ball right in front of it, go forward,
                # rotate otherwise
                if direction == 0:
                    # advance slowly to avoid scoring against its own goal
                    # when close
                    if abs(heading) < 0.7 and robot_pos[1] > 0.59:
                        left_speed = 1
                        right_speed = 1

                    # back up when a team mate is already on the ball in offense zone.
                    if team_data and robot_pos[1] < 0:
                        left_speed = -1
                        right_speed = -1

                    else:
                        # increase the speed of the robot to move towards the ball
                        left_speed = 7
                        right_speed = 7

                else:
                    left_speed = direction * 4
                    right_speed = direction * -4

                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)

                # Send message to team robots
                self.send_data_to_team(self.player_id)
