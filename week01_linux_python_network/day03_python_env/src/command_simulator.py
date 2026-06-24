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


def print_help():
    print("명령어를 입력하세요.")
    print("w: 전진")
    print("s: 후진")
    print("a: 좌회전")
    print("d: 우회전")
    print("space 또는 stop: 정지")
    print("q: 종료")
    print()


def print_state(robot):
    state = robot.to_dict()
    print(f"[STATE] x={state['x']}, y={state['y']}, battery={state['battery']}%, status={state['status']}")


def main():
    robot = create_robot_state()
    print_help()
    print_state(robot)

    while True:
        command = input("command> ")

        if command == "w":
            robot.move_forward()
        elif command == "s":
            robot.move_backward()
        elif command == "a":
            robot.turn_left()
        elif command == "d":
            robot.turn_right()
        elif command == " " or command == "stop":
            robot.stop()
        elif command == "q":
            print("프로그램을 종료합니다.")
            break
        else:
            print("알 수 없는 명령어입니다.")
            continue

        print_state(robot)


if __name__ == "__main__":
    main()
