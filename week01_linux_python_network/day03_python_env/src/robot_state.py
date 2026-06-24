from dataclasses import dataclass
from datetime import datetime


@dataclass
class RobotState:
    robot_id: str
    x: float
    y: float
    battery: float
    status: str
    timestamp: str

    def move_forward(self):
        self.x += 1.0
        self.status = "moving_forward"
        self.battery -= 0.5
        self.update_time()

    def move_backward(self):
        self.x -= 1.0
        self.status = "moving_backward"
        self.battery -= 0.5
        self.update_time()

    def turn_left(self):
        self.y += 1.0
        self.status = "turning_left"
        self.battery -= 0.3
        self.update_time()

    def turn_right(self):
        self.y -= 1.0
        self.status = "turning_right"
        self.battery -= 0.3
        self.update_time()

    def stop(self):
        self.status = "stopped"
        self.update_time()

    def update_time(self):
        self.timestamp = datetime.now().isoformat()

    def to_dict(self):
        return {
            "robot_id": self.robot_id,
            "x": self.x,
            "y": self.y,
            "battery": round(self.battery, 2),
            "status": self.status,
            "timestamp": self.timestamp
        }
