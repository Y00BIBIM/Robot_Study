import threading
from contextlib import asynccontextmanager
from typing import Optional

import rospy
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from virtual_robot.msg import RobotState


class RobotStateResponse(BaseModel):
    robot_id: str
    x: float
    y: float
    theta: float
    speed: float
    battery: float
    status: str


latest_state: Optional[RobotStateResponse] = None
state_lock = threading.Lock()
ros_subscriber = None

def robot_state_callback(message: RobotState) -> None:
    """
    /robot/state Topic에서 새로운 메시지를 받을 때 실행된다.
    받은 ROS 메시지를 FastAPI에서 사용할 수 있는 형태로 저장한다.
    """
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

    rospy.loginfo(
        "API server received state: "
        f"id={message.robot_id}, "
        f"x={message.x:.2f}, "
        f"y={message.y:.2f}, "
        f"status={message.status}"
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI 서버가 시작될 때 ROS Node와 Subscriber를 생성하고,
    서버가 종료될 때 ROS 연결을 정리한다.
    """
    global ros_subscriber

    if not rospy.core.is_initialized():
        rospy.init_node(
            "virtual_robot_api_server",
            anonymous=False,
            disable_signals=True,
        )

    ros_subscriber = rospy.Subscriber(
        "/robot/state",
        RobotState,
        robot_state_callback,
        queue_size=10,
    )

    rospy.loginfo("Virtual Robot FastAPI server connected to ROS")

    yield

    if ros_subscriber is not None:
        ros_subscriber.unregister()

    if not rospy.is_shutdown():
        rospy.signal_shutdown("FastAPI server stopped")


app = FastAPI(
    title="ROS Virtual Robot API",
    description="ROS /robot/state Topic을 REST API로 제공한다.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "virtual-robot-api",
        "ros_initialized": rospy.core.is_initialized(),
        "ros_shutdown": rospy.is_shutdown(),
    }


@app.get("/robot/state", response_model=RobotStateResponse)
def get_robot_state():
    with state_lock:
        state = latest_state

    if state is None:
        raise HTTPException(
            status_code=503,
            detail="ROS /robot/state 메시지를 아직 수신하지 못했습니다.",
        )

    return state
