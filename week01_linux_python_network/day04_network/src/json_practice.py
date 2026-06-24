import json
from datetime import datetime
from pathlib import Path

from config import (
	ROBOT_ID,
	INITIAL_X,
	INITIAL_Y,
	INITIAL_BATTERY,
	INITIAL_STATUS,
)
from robot_state import RobotState

DATA_DIR = Path("data")
JSON_FILE_PATH = DATA_DIR / "robot_state.json"

def create_robot_state():
	return RobotState(
		robot_id=ROBOT_ID,
		x=INITIAL_X,
		y=INITIAL_Y,
		battery=INITIAL_BATTERY,
		status=INITIAL_STATUS,
		timestamp=datetime.now().isoformat(),
	)

def save_robot_state_to_json(robot):
	DATA_DIR.mkdir(exist_ok=True)

	with open(JSON_FILE_PATH, "w", encoding="utf-8") as file:
		json.dump(robot.to_dict(), file, ensure_ascii=False, indent=4)

	print(f"Chnage robot status into .json file : {JSON_FILE_PATH}")

def load_robot_state_from_json():
	with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
		data = json.load(file)

	print("Read the robot status in .json file.")
	return data
def main():
	robot = create_robot_state()

	robot.move_forward()
	robot.turn_left()

	save_robot_state_to_json(robot)

	loaded_data = load_robot_state_from_json()

	print("=== Loaded Robot State ===")
	print(f"Robot ID : {loaded_data['robot_id']}")
	print(f"Position : x={loaded_data['x']}, y={loaded_data['y']}")
	print(f"Battery : {loaded_data['battery']}%")
	print(f"status : {loaded_data['status']}")
	print(f"Time : {loaded_data['timestamp']}")

if __name__ == "__main__":
	main()
