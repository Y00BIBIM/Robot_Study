import threading
from contextlib import asynccontextmanager
from typing import Literal, Optional

import rospy
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from virtual_robot.msg import RobotCommand, RobotState


class RobotStateResponse(BaseModel):
    robot_id: str
    x: float
    y: float
    theta: float
    speed: float
    battery: float
    status: str


class RobotCommandRequest(BaseModel):
    command: Literal[
        "forward",
        "backward",
        "left",
        "right",
        "stop",
    ]

    target_speed: float = Field(
        ge=0.0,
        le=2.0,
        description="목표 이동 속도",
    )


class RobotCommandResponse(BaseModel):
    accepted: bool
    command: str
    target_speed: float
    topic: str


latest_state: Optional[RobotStateResponse] = None

state_lock = threading.Lock()

ros_state_subscriber = None
ros_command_publisher = None


def robot_state_callback(message: RobotState) -> None:
    """ROS /robot/state 메시지를 최신 상태로 저장한다."""
    global latest_state

    new_state = RobotStateResponse(
        robot_id=message.robot_id,
        x=message.x,
        y=message.y,
        theta=message.theta,
        speed=message.speed,
        battery=message.battery,
        status=message.status,
    )

    with state_lock:
        latest_state = new_state


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI 시작과 종료 시 ROS 자원을 관리한다."""
    global ros_state_subscriber
    global ros_command_publisher

    if not rospy.core.is_initialized():
        rospy.init_node(
            "virtual_robot_command_api",
            anonymous=False,
            disable_signals=True,
        )

    ros_state_subscriber = rospy.Subscriber(
        "/robot/state",
        RobotState,
        robot_state_callback,
        queue_size=10,
    )

    ros_command_publisher = rospy.Publisher(
        "/robot/command",
        RobotCommand,
        queue_size=10,
    )

    rospy.loginfo(
        "FastAPI ROS state subscriber and command publisher started"
    )

    yield

    if ros_state_subscriber is not None:
        ros_state_subscriber.unregister()

    if ros_command_publisher is not None:
        ros_command_publisher.unregister()

    if not rospy.is_shutdown():
        rospy.signal_shutdown("FastAPI server stopped")


app = FastAPI(
    title="Virtual Robot Control API",
    description="ROS 로봇 상태를 조회하고 이동 명령을 전송한다.",
    version="1.1.0",
    lifespan=lifespan,
)


@app.get("/health")
def health_check():
    with state_lock:
        state_received = latest_state is not None

    return {
        "status": "ok",
        "service": "virtual-robot-command-api",
        "ros_initialized": rospy.core.is_initialized(),
        "state_received": state_received,
    }


@app.get(
    "/robot/state",
    response_model=RobotStateResponse,
)
def get_robot_state():
    with state_lock:
        state = latest_state

    if state is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ROS /robot/state 메시지를 아직 수신하지 못했습니다.",
        )

    return state


@app.post(
    "/robot/command",
    response_model=RobotCommandResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def send_robot_command(
    request: RobotCommandRequest,
):
    if ros_command_publisher is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ROS Publisher가 준비되지 않았습니다.",
        )

    target_speed = request.target_speed

    # stop 명령은 항상 속도를 0으로 처리한다.
    if request.command == "stop":
        target_speed = 0.0

    ros_message = RobotCommand()
    ros_message.command = request.command
    ros_message.target_speed = target_speed

    ros_command_publisher.publish(ros_message)

    rospy.loginfo(
        "Command published: "
        f"command={request.command}, "
        f"target_speed={target_speed:.2f}"
    )

    return RobotCommandResponse(
        accepted=True,
        command=request.command,
        target_speed=target_speed,
        topic="/robot/command",
    )
