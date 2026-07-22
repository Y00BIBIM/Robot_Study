# Week05 Day02 — FastAPI와 ROS Topic 연결

## 학습 목표

ROS의 `/robot/state` Topic을 FastAPI 서버에서 구독하고, 가장 최근에 수신한 로봇 상태를 REST API를 통해 반환하도록 구현했다.

전체 데이터 흐름은 다음과 같다.

```text
virtual_robot_node
        │
        │ RobotState 발행
        ▼
  /robot/state
        │
        │ RobotState 구독
        ▼
FastAPI ros_api_server
        │
        │ HTTP GET 요청
        ▼
웹 브라우저 또는 외부 클라이언트
```

## ROS Node 초기화

FastAPI 서버가 시작될 때 ROS Node를 초기화했다.

```python
rospy.init_node(
    "virtual_robot_api_server",
    anonymous=False,
    disable_signals=True,
)
```

Uvicorn이 프로그램의 실행과 종료 신호를 관리하기 때문에 ROS의 기본 신호 처리를 비활성화하기 위해 `disable_signals=True`를 사용했다.

## ROS Subscriber 생성

FastAPI 서버에서 `/robot/state` Topic을 구독하는 Subscriber를 생성했다.

```python
ros_subscriber = rospy.Subscriber(
    "/robot/state",
    RobotState,
    robot_state_callback,
    queue_size=10,
)
```

`/robot/state`에 새로운 메시지가 발행되면 `robot_state_callback()` 함수가 실행된다.

## 최신 로봇 상태 저장

ROS Callback에서 수신한 메시지를 FastAPI가 반환할 수 있는 Pydantic 모델로 변환했다.

```python
def robot_state_callback(message: RobotState) -> None:
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
```

ROS Topic은 지속적으로 메시지를 전달하지만 HTTP API는 클라이언트의 요청이 있을 때만 응답한다.

따라서 가장 최근에 수신한 ROS 메시지를 `latest_state` 변수에 저장하고, API 요청이 들어왔을 때 이 값을 반환하도록 구성했다.

## Thread Lock 사용

ROS Callback과 FastAPI 요청 처리 함수가 서로 다른 실행 흐름에서 동시에 `latest_state`에 접근할 수 있다.

동시 접근으로 인한 데이터 문제를 방지하기 위해 `threading.Lock`을 사용했다.

```python
with state_lock:
    latest_state = new_state
```

API에서 상태를 읽을 때도 같은 Lock을 사용했다.

```python
with state_lock:
    state = latest_state
```

## REST API 응답 구현

`GET /robot/state` 요청이 들어오면 가장 최근에 받은 ROS 상태를 반환하도록 구현했다.

```python
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
```

ROS 메시지를 아직 받지 못한 경우에는 임의의 값을 반환하지 않고 `503 Service Unavailable` 오류를 반환하도록 처리했다.

## 실행 순서

첫 번째 터미널에서 ROS Master를 실행했다.

```bash
source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash

roscore
```

두 번째 터미널에서 가상 로봇 노드를 실행했다.

```bash
source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash

rosrun virtual_robot virtual_robot_node.py
```

세 번째 터미널에서 ROS 환경과 Python 가상환경을 적용한 후 FastAPI 서버를 실행했다.

```bash
source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash

cd ~/robot_study/Week05/Day02
source ../venv/bin/activate

python -m uvicorn ros_api_server:app \
    --host 0.0.0.0 \
    --port 8000
```

ROS Node가 중복 초기화되는 문제를 방지하기 위해 Day02에서는 Uvicorn의 `--reload` 옵션을 사용하지 않았다.

## API 연결 테스트

다음 명령을 이용해 FastAPI 서버 상태를 확인했다.

```bash
curl http://localhost:8000/health
```

다음 명령으로 ROS에서 받은 로봇 상태를 확인했다.

```bash
curl http://localhost:8000/robot/state
```

ROS의 `/robot/state` 데이터가 변경되면 FastAPI의 `/robot/state` 응답 값도 함께 변경되는 것을 확인했다.

## ROS 메시지 타입 불일치 오류

`/robot/command` Topic에 명령을 보내는 과정에서 다음 경고가 발생했다.

```text
topic types do not match:
[virtual_robot/RobotCommand] vs. [std_msgs/String]
```

원인은 같은 `/robot/command` Topic을 사용하는 Publisher와 Subscriber가 서로 다른 메시지 타입을 사용했기 때문이다.

실제 `/robot/command` Topic은 다음 커스텀 메시지를 사용한다.

```text
virtual_robot/RobotCommand
```

`RobotCommand.msg`의 구조는 다음과 같다.

```text
string command
float64 target_speed
```

기존에는 다음과 같이 `std_msgs/String` 타입으로 명령을 전송했다.

```bash
rostopic pub -1 /robot/command \
    std_msgs/String \
    "data: 'forward'"
```

하지만 `/robot/command`가 사용하는 실제 타입은 `virtual_robot/RobotCommand`이므로 다음과 같이 수정했다.

```bash
rostopic pub -1 /robot/command \
    virtual_robot/RobotCommand \
    "{command: 'forward', target_speed: 0.5}"
```

정지 명령은 다음과 같이 전송할 수 있다.

```bash
rostopic pub -1 /robot/command \
    virtual_robot/RobotCommand \
    "{command: 'stop', target_speed: 0.0}"
```

이번 오류를 통해 동일한 ROS Topic에 연결되는 모든 Publisher와 Subscriber는 반드시 같은 메시지 타입을 사용해야 한다는 것을 확인했다.

## 학습 결과

ROS의 `/robot/state` Topic과 FastAPI를 연결해 실제 로봇 상태를 HTTP API로 제공하는 기능을 구현했다.

이번 학습을 통해 다음 내용을 이해했다.

* FastAPI와 ROS Node 통합
* `rospy.init_node()`를 이용한 ROS Node 초기화
* `rospy.Subscriber()`를 이용한 Topic 구독
* ROS Callback 함수
* 최신 ROS 메시지 저장
* ROS 메시지를 Pydantic 모델로 변환
* Thread Lock을 이용한 동시 접근 제어
* HTTP `503 Service Unavailable` 처리
* ROS Custom Message 사용
* ROS Topic의 Publisher와 Subscriber 메시지 타입 통일

