import requests


BASE_URL = "http://127.0.0.1:8000"


def get_health():
    response = requests.get(f"{BASE_URL}/health")
    print("GET /health")
    print(response.json())
    print()


def get_robot_state():
    response = requests.get(f"{BASE_URL}/robot/state")
    print("GET /robot/state")
    print(response.json())
    print()


def send_robot_command(command):
    response = requests.post(
        f"{BASE_URL}/robot/command",
        json={
            "command": command
        },
    )

    print(f"POST /robot/command command={command}")
    print(response.json())
    print()


def main():
    get_health()
    get_robot_state()

    send_robot_command("forward")
    send_robot_command("left")
    send_robot_command("stop")

    get_robot_state()


if __name__ == "__main__":
    main()
