from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

from config import (
    ROBOT_ID,
    INITIAL_X,
    INITIAL_Y,
    INITIAL_BATTERY,
    INITIAL_STATUS,
)
from robot_state import RobotState


app = FastAPI()

robot = RobotState(
    robot_id=ROBOT_ID,
    x=INITIAL_X,
    y=INITIAL_Y,
    battery=INITIAL_BATTERY,
    status=INITIAL_STATUS,
    timestamp=datetime.now().isoformat(),
)


class CommandRequest(BaseModel):
    command: str


@app.get("/")
def root():
    return {
        "message": "Robot API Server is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.get("/robot/state")
def get_robot_state():
    return robot.to_dict()


@app.post("/robot/command")
def send_robot_command(request: CommandRequest):
    command = request.command

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
        return {
            "success": False,
            "message": f"Unknown command: {command}",
            "robot_state": robot.to_dict(),
        }

    return {
        "success": True,
        "command": command,
        "robot_state": robot.to_dict(),
    }
