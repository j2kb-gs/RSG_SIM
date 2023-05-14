# - ROBOT PLAYER 2

import math
import time  # noqa: F401
import utils
from rsg_player_robot import RSGPlayerRobot, TIME_STEP

"""
----------------------------- defensive -------------------------------------
Player 2 has a defensive role: 
    - chase the ball when the ball is in range and try to score
    - give up the ball when another team player is already on the ball in offense zone
    - get back to the defense zone when it can't see the ball

----------------------------- offensive -------------------------------------
Player 2 has a offensive role: 
    - chase the ball when the ball is in range and try to score
    - give up the ball to a team mate (player 1) only when in defense zone
    - strategically place itself in oppenent's danger zone when can't locate the ball

-------------------------- Collaborative ------------------------------------
Player 2 has a center support role: 
    - chase the ball when the ball is in range and try to score
    - give up the ball only when player 3 (offensive player) is already on the ball
    - strategically place itself at the center when can't locate the ball

    
    `heading`
        pi
-pi/2   .   pi/2
        0
* abs(heading) > 2 means player is facing opponents goal  
* abs(heading) < 0.7 means player is facing its own goal  
"""


class MyPlayer2(RSGPlayerRobot):
    strategy = {}            # strategy that team is playing
    data = 0                # data from supervisor
    team_data = 0           # data from team members
    heading = 0             # data from compass
    robot_pos = []          # position of robot
    sonar_values = {}       # data from sonars

# ------------------ Initialize essential data ----------------------------#
    def get_data_values(self):
        """ Initialize essential data such as heading, position, sonar """

        self.data = self.get_new_data()  # noqa: F841
        team_data = None

        # Get data from compass
        self.heading = self.get_compass_heading()  # noqa: F841

        # Get GPS coordinates of the robot
        self.robot_pos = self.get_gps_coordinates()  # noqa: F841

        # Get data from sonars
        self.sonar_values = self.get_sonar_values()  # noqa: F841

# ------------------------- 1- Defensive Strategy  -------------------------#
    def defensive_strat(self):
        team_data = None
        while self.is_new_team_data():
            team_data = self.get_new_team_data()  # noqa: F841
            # Do something with team data
        ball_data = None

        if self.is_new_ball_data():
            ball_data = self.get_new_ball_data()
        else:
            # robot does not see the ball
            # goes back to defense slowly
            if self.robot_pos[1] >= -0.59:
                if abs(self.heading) >= 2.4:
                    self.left_motor.setVelocity(-1)
                    self.right_motor.setVelocity(-1)

                elif abs(self.heading) <= 0.7:
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

        if ball_data:
            # Compute the speed for motors
            direction = utils.get_direction(ball_data["direction"])

            # If the robot has the ball right in front of it, go forward,
            # rotate otherwise
            if direction == 0:
                # advance slowly to avoid scoring against its own goal
                # when close
                if abs(self.heading) < 0.7 and self.robot_pos[1] > 0.59:
                    left_speed = 1
                    right_speed = 1

                # back up when a team mate is already on the ball in offense zone.
                if team_data and self.robot_pos[1] < 0:
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

# ------------------------ 2- Offensive Strategy  --------------------------#
    def offensive_strat(self):
        team_data = None
        while self.is_new_team_data():
            team_data = self.get_new_team_data()  # noqa: F841
            # Do something with team data
        ball_data = None
        if self.is_new_ball_data():
            ball_data = self.get_new_ball_data()
        else:
            # robot does not see the ball
            # robot try to position itself in opponents danger zone.
            if .59 >= self.robot_pos[1]:
                if abs(self.heading) >= 2.4:
                    self.left_motor.setVelocity(1)
                    self.right_motor.setVelocity(1)

                elif abs(self.heading) <= 0.7:
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

        if ball_data:
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

# ---------------------- 3- Collaborative Strategy  -------------------------#
    def collaborative_strat(self):
        while self.is_new_team_data():
            team_data = self.get_new_team_data()  # noqa: F841
            # Do something with team data
        ball_data = None

        if self.is_new_ball_data():
            ball_data = self.get_new_ball_data()
        else:
            # robot does not see the ball
            # robot tries to go position itself around the center of the field.
            if -.39 <= self.robot_pos[1] <= .39:
                if abs(self.heading) >= 2.4:
                    self.left_motor.setVelocity(1)
                    self.right_motor.setVelocity(1)

                elif abs(self.heading) <= 0.7:
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

        # Compute the speed for motors
        if ball_data:
            direction = utils.get_direction(ball_data["direction"])

            # If the robot has the ball right in front of it, go forward,
            # rotate otherwise
            if direction == 0:
                # advance slowly to avoid scoring against its own goal
                # when close
                if abs(self.heading) < 0.7 and self.robot_pos[1] > 0.59:
                    left_speed = 1
                    right_speed = 1

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

    def run(self):
        while self.robot.step(TIME_STEP) != -1:

            if self.is_new_data():
                # get strategy that the team is playing
                self.strategy = self.get_strategy_data()

                # Initialize data that robot needs (heading, position etc.. )
                self.get_data_values()

                if self.strategy["strategy_id"] == 1:       # defensive
                    self.defensive_strat()
                elif self.strategy["strategy_id"] == 2:     # offensive
                    self.offensive_strat()
                else:                                       # collab
                    self.collaborative_strat()
