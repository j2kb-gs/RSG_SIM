# - ROBOT PLAYER 1

import math  # noqa: F401
import utils
from rsg_player_robot import RSGPlayerRobot, TIME_STEP


class MyPlayer4(RSGPlayerRobot):
    def run(self):
        while self.robot.step(TIME_STEP) != 1:
            if self.is_new_data():
                data = self.get_new_data()

                while self.is_new_team_data():
                    team_data = self.get_new_team_data()
                    # use team data for something

                if self.is_new_ball_data():
                    ball_data = self.get_new_ball_data()
                else:
                    # if the robot can't see the ball, It stops
                    self.currentlyPlaying.stop()
                    continue

                # get data from compass
                heading = self.get_compass_heading()

                # get GPS coordinates of the robot
                robot_pos = self.get_gps_coordinates()

                # get data from sonars
                sonar_values = self.get_sonar_values()

                # compute the speed for motors
                direction = utils.get_direction(ball_data["direction"])

                # If the robot has the ball right in front of it, go forward,
                # rotate otherwise
                if direction == 0:      # move forward
                    self.startMotion(self.forwards)
                elif direction == 1:    # turn left
                    self.startMotion(self.turnLeft60)
                else:                   # turn right right
                    self.startMotion(self.turnRight60)

                # Send message to team robots
                self.send_data_to_team(self.player_id)
