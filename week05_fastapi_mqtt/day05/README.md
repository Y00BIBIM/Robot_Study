# Week05 Day05 — ROS 상태를 MQTT로 전송

## 학습 목표

ROS의 `/robot/state` Topic을 구독하고, 수신한 로봇 상태를 JSON 형식으로 변환해 MQTT의 `robot/state` Topic으로 발행하는 Bridge Node를 구현했다.

전체 데이터 흐름은 다음과 같다.

```text
virtual_robot_node
        ↓
ROS /robot/state
        ↓
ros_state_to_mqtt
        ↓
RobotState 메시지를 JSON으로 변환
        ↓
MQTT robot/state
        ↓
MQTT Subscriber
```

## 학습 내용

### ROS Subscriber 구현

`ros_state_to_mqtt.py`에서 ROS Node를 초기화하고 `/robot/state` Topic을 구독했다.

```python
rospy.init_node(
    "ros_state_to_mqtt",
    anonymous=False,
)

rospy.Subscriber(
    "/robot/state",
    RobotState,
    robot_state_callback,
    queue_size=10,
)
```

`/robot/state`에 새로운 메시지가 발행되면 `robot_state_callback()` 함수가 실행된다.

### MQTT Client 생성 및 연결

Paho MQTT 라이브러리를 사용해 MQTT Client를 생성하고 Mosquitto Broker에 연결했다.

```python
mqtt_client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id="ros_state_to_mqtt",
)

mqtt_client.connect(
    host=broker_host,
    port=broker_port,
    keepalive=60,
)

mqtt_client.loop_start()
```

`loop_start()`를 사용해 별도의 MQTT 네트워크 스레드에서 Broker 연결과 메시지 송수신을 처리하도록 구성했다.

### ROS 메시지를 JSON으로 변환

ROS에서 수신한 `RobotState` 메시지를 Python 딕셔너리로 변환했다.

```python
payload = {
    "robot_id": message.robot_id,
    "x": message.x,
    "y": message.y,
    "theta": message.theta,
    "speed": message.speed,
    "battery": message.battery,
    "status": message.status,
}
```

이후 `json.dumps()`를 사용해 MQTT로 전송할 수 있는 JSON 문자열로 변환했다.

```python
payload_text = json.dumps(
    payload,
    ensure_ascii=False,
    allow_nan=False,
)
```

### MQTT 상태 발행

변환한 JSON 문자열을 MQTT의 `robot/state` Topic으로 발행했다.

```python
mqtt_client.publish(
    topic="robot/state",
    payload=payload_text,
    qos=1,
    retain=True,
)
```

`qos=1`을 사용해 Broker가 메시지 수신을 확인하도록 설정했다.

`retain=True`를 적용해 Broker가 마지막 로봇 상태를 저장하도록 했다. 따라서 새로운 Subscriber가 접속해도 최신 상태를 즉시 받을 수 있다.

### 데이터 유효성 검사

로봇의 위치와 속도에 `NaN` 또는 무한대 값이 포함되는 것을 방지하기 위해 `math.isfinite()`를 사용했다.

```python
numeric_values = [
    message.x,
    message.y,
    message.theta,
    message.speed,
    message.battery,
]

if not all(math.isfinite(value) for value in numeric_values):
    return
```

비정상적인 수치가 발견되면 해당 상태를 MQTT로 발행하지 않도록 처리했다.

## 실행 및 테스트

Mosquitto Broker, ROS Master, 가상 로봇 Node를 실행한 후 Bridge 프로그램을 실행했다.

```bash
python ros_state_to_mqtt.py
```

MQTT Subscriber를 사용해 전달된 상태를 확인했다.

```bash
mosquitto_sub \
    -h localhost \
    -t robot/state \
    -q 1 \
    -v
```

출력 예시는 다음과 같다.

```text
robot/state {"robot_id":"virtual_robot_01","x":0.0,"y":0.0,"theta":0.0,"speed":0.0,"battery":100.0,"status":"idle"}
```

## 학습 결과

ROS의 `RobotState` 메시지를 MQTT JSON Payload로 변환하는 ROS → MQTT Bridge를 구현했다.

이번 학습을 통해 다음 내용을 이해했다.

* ROS Subscriber와 Callback 함수
* Paho MQTT Client 생성
* MQTT Broker 연결
* ROS 메시지를 Python 딕셔너리로 변환
* 딕셔너리를 JSON 문자열로 직렬화
* MQTT Topic 메시지 발행
* MQTT QoS 1
* Retained Message
* `NaN`과 무한대 값 검증
* ROS와 MQTT 사이의 Bridge 구조

