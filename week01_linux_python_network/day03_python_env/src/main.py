from datetime import datetime

from config import ROBOT_ID, INITIAL_X, INITIAL_Y, INITIAL_BATTERY, INITIAL_STATUS
from robot_state import RobotState


def create_robot_state():
    return RobotState(
        robot_id=ROBOT_ID,
        x=INITIAL_X,
        y=INITIAL_Y,
        battery=INITIAL_BATTERY,
        status=INITIAL_STATUS,
        timestamp=datetime.now().isoformat()
    )


def print_robot_state(robot):
    print("=== Robot State ===")
    print(f"Robot ID : {robot.robot_id}")
    print(f"Position : x={robot.x}, y={robot.y}")
    print(f"Battery  : {robot.battery}%")
    print(f"Status   : {robot.status}")
    print(f"Time     : {robot.timestamp}")
    print()


def main():
    robot = create_robot_state()

    print_robot_state(robot)

    robot.move_forward()
    print_robot_state(robot)

    robot.turn_left()
    print_robot_state(robot)

    robot.stop()
    print_robot_state(robot)

    print("Dictionary Format:")
    print(robot.to_dict())


if __name__ == "__main__":
    main()
