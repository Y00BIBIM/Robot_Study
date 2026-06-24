class Robot:
    def __init__(self, name):
        self.name = name
        self.battery = 100.0
        self.x = 0.0
        self.y = 0.0
        self.status = "idle"

    def move_forward(self):
        self.y += 1.0
        self.battery -= 1.0
        self.status = "moving"

    def move_backward(self):
        self.y -= 1.0
        self.battery -= 1.0
        self.status = "moving"

    def turn_left(self):
        self.x -= 0.5
        self.battery -= 0.5
        self.status = "turning_left"

    def turn_right(self):
        self.x += 0.5
        self.battery -= 0.5
        self.status = "turning_right"

    def stop(self):
        self.status = "idle"

    def get_state(self):
        return {
            "name": self.name,
            "battery": self.battery,
            "position": {
                "x": self.x,
                "y": self.y
            },
            "status": self.status
        }


def handle_command(robot, command):
    if command == "forward":
        robot.move_forward()
    elif command == "backward":
        robot.move_backward()
    elif command == "left":
        robot.turn_left()
    elif command == "right":
        robot.turn_right()
    elif command == "stop":
        robot.stop()
    else:
        print("Unknown command:", command)


def main():
    robot = Robot("mobile_robot_01")
    commands = ["forward", "forward", "right", "stop"]

    for command in commands:
        handle_command(robot, command)
        print(robot.get_state())


if __name__ == "__main__":
    main()
