# - ROBOT PLAYER 1

import math  # noqa: F401
import utils
from rsg_player_robot import RSGPlayerRobot, TIME_STEP


"""
Player 3 has a striker's role: 
    - chase the ball when the ball is in range and try to score
    - give up the ball to a team mate (player 1) only when in defense zone
    - strategically place itself in oppenent's danger zone when can't locate the ball

    `heading`
        pi
-pi/2   .   pi/2
        0
* abs(heading) > 2 means player is facing opponents goal  
* abs(heading) < 0.7 means player is facing its own goal  
"""


class MyPlayer3(RSGPlayerRobot):
    def run(self):
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

                while self.is_new_team_data():
                    team_data = self.get_new_team_data()  # noqa: F841
                    # Do something with team data

                if self.is_new_ball_data():
                    ball_data = self.get_new_ball_data()
                else:
                    # robot does not see the ball
                    # robot try to position itself in opponents danger zone.
                    if -.59 <= robot_pos[1]:
                        if abs(heading) >= 2.4:
                            self.left_motor.setVelocity(1)
                            self.right_motor.setVelocity(1)

                        elif abs(heading) <= 0.7:
                            self.left_motor.setVelocity(-1)
                            self.right_motor.setVelocity(-1)
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
