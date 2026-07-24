# Week05 Day06 — MQTT 명령을 ROS로 전달

## 학습 목표

MQTT의 `robot/command` Topic을 구독하고, 수신한 JSON 명령을 ROS의 `RobotCommand` 메시지로 변환해 `/robot/command` Topic으로 발행하는 Bridge Node를 구현했다.

전체 데이터 흐름은 다음과 같다.

```text
MQTT Publisher
        ↓
MQTT robot/command
        ↓
mqtt_command_to_ros
        ↓
JSON 명령 검증
        ↓
ROS RobotCommand 메시지 생성
        ↓
ROS /robot/command
        ↓
virtual_robot_node
```

## 학습 내용

### ROS Publisher 구현

MQTT에서 받은 명령을 ROS로 전달하기 위해 `/robot/command` Publisher를 생성했다.

```python
ros_command_publisher = rospy.Publisher(
    "/robot/command",
    RobotCommand,
    queue_size=10,
)
```

메시지 타입은 다음 커스텀 메시지를 사용했다.

```text
virtual_robot/RobotCommand
```

`RobotCommand.msg`의 구조는 다음과 같다.

```text
string command
float64 target_speed
```

기존에 사용했던 `std_msgs/String`과 혼용하면 Topic 메시지 타입 불일치가 발생하므로 모든 Publisher와 Subscriber에서 `RobotCommand` 타입을 사용했다.

### MQTT Topic 구독

Paho MQTT Client를 생성한 뒤 Broker 연결에 성공하면 `robot/command` Topic을 구독하도록 구현했다.

```python
def on_connect(
    client,
    userdata,
    connect_flags,
    reason_code,
    properties,
):
    if reason_code == 0:
        client.subscribe(
            "robot/command",
            qos=1,
        )
```

구독 처리를 `on_connect()` 안에 작성하면 Broker 연결이 끊겼다가 다시 연결돼도 Topic을 재구독할 수 있다.

### MQTT Payload 디코딩

MQTT 메시지의 Payload는 `bytes` 형식이므로 UTF-8 문자열로 변환했다.

```python
payload_text = message.payload.decode("utf-8")
```

변환한 JSON 문자열을 `json.loads()`로 Python 딕셔너리로 변환했다.

```python
payload = json.loads(payload_text)
```

수신하는 JSON 구조는 다음과 같다.

```json
{
  "command": "forward",
  "target_speed": 0.5
}
```

### 명령 유효성 검사

지원하는 명령을 집합으로 정의했다.

```python
ALLOWED_COMMANDS = {
    "forward",
    "backward",
    "left",
    "right",
    "stop",
}
```

수신한 `command`가 허용된 명령인지 검사했다.

```python
if command not in ALLOWED_COMMANDS:
    return
```

또한 `target_speed`가 숫자인지 확인하고, 허용 범위 안에 있는지 검사했다.

```python
if (
    isinstance(target_speed, bool)
    or not isinstance(target_speed, (int, float))
):
    return

target_speed = float(target_speed)

if not 0.0 <= target_speed <= 2.0:
    return
```

`NaN`이나 무한대 값이 전달되는 것도 차단했다.

```python
if not math.isfinite(target_speed):
    return
```

### 정지 명령 처리

`stop` 명령에서는 입력값과 관계없이 목표 속도를 `0.0`으로 설정했다.

```python
if command == "stop":
    target_speed = 0.0
```

이를 통해 다음과 같은 잘못된 입력이 전달되더라도 안전하게 정지 명령을 발행할 수 있다.

```json
{
  "command": "stop",
  "target_speed": 1.0
}
```

### ROS 메시지 생성 및 발행

모든 검증을 통과하면 `RobotCommand` 메시지를 생성했다.

```python
ros_message = RobotCommand()
ros_message.command = command
ros_message.target_speed = target_speed
```

완성된 메시지를 ROS의 `/robot/command` Topic으로 발행했다.

```python
ros_command_publisher.publish(ros_message)
```

## Retained Command 처리

로봇 이동 명령에는 Retained Message를 사용하지 않았다.

`robot/command`에 Retained Message가 저장되면 새로운 Subscriber가 연결됐을 때 과거 명령이 다시 전달될 수 있기 때문이다.

기존에 저장된 Retained Command가 있다면 다음 명령으로 제거했다.

```bash
mosquitto_pub \
    -h localhost \
    -t robot/command \
    -r \
    -n
```

## 실행 및 테스트

Bridge 프로그램을 실행했다.

```bash
python mqtt_command_to_ros.py
```

다른 터미널에서 ROS 명령을 확인했다.

```bash
rostopic echo /robot/command
```

MQTT로 전진 명령을 발행했다.

```bash
mosquitto_pub \
    -h localhost \
    -t robot/command \
    -q 1 \
    -m '{"command":"forward","target_speed":0.5}'
```

ROS Topic에서는 다음 메시지를 확인할 수 있었다.

```text
command: "forward"
target_speed: 0.5
```

잘못된 명령, 비정상적인 JSON, 속도 범위를 초과한 명령은 ROS로 전달되지 않는 것도 확인했다.

## 학습 결과

MQTT JSON 명령을 검증하고 ROS의 `RobotCommand` 메시지로 변환하는 MQTT → ROS Bridge를 구현했다.

이번 학습을 통해 다음 내용을 이해했다.

* MQTT Topic 구독
* MQTT `bytes` Payload 디코딩
* JSON 문자열 파싱
* 명령 및 자료형 검증
* 속도 범위 검사
* ROS Custom Message 생성
* ROS Publisher를 이용한 명령 발행
* MQTT 명령에서 Retained Message를 사용하면 안 되는 이유
* MQTT와 ROS 사이의 안전한 명령 전달 구조

