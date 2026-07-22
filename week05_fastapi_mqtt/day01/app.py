from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="Virtual Robot API",
    description="ROS 가상 로봇 상태를 제공하는 API",
    version="1.0.0",
)


class RobotStateResponse(BaseModel):
    robot_id: str
    x: float
    y: float
    theta: float
    speed: float
    battery: float
    status: str


@app.get("/")
def read_root():
    return {
        "message": "Virtual Robot API",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "virtual-robot-api",
    }


@app.get("/robot/state", response_model=RobotStateResponse)
def get_robot_state():
    return RobotStateResponse(
        robot_id="virtual_robot_01",
        x=1.5,
        y=2.0,
        theta=0.75,
        speed=0.5,
        battery=95.0,
        status="running",
    )
