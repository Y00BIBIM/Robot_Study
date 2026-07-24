# Week05 Day07 — Unity·ROS·FastAPI·MQTT 전체 통합

## 학습 목표

Week05에서 구현한 FastAPI와 MQTT Bridge를 기존 Unity·ROS 시스템에 연결하고, 여러 외부 통신 방식으로 로봇을 제어하고 상태를 확인하는 전체 통합 테스트를 진행했다.

최종 시스템 구조는 다음과 같다.

```text
                         FastAPI
                    GET /robot/state
                           ↑
                           │
Unity ←────────── ROS /robot/state ─────────→ ROS → MQTT Bridge
   │                       ↑                         │
   │                       │                         ▼
   │              virtual_robot_node          MQTT robot/state
   │                       ↑
   │                       │
   ├────────────→ ROS /robot/command
   │                       ↑
   │                       ├─ FastAPI POST /robot/command
   │                       │
   │                       └─ MQTT → ROS Bridge
   │                                  ↑
   └───────────────────────── MQTT robot/command
```

## 통합 구성 요소

전체 테스트에서는 다음 프로그램과 서비스를 함께 실행했다.

* Mosquitto MQTT Broker
* ROS Master
* `virtual_robot_node`
* ROS TCP Endpoint
* Unity 가상 로봇 프로젝트
* FastAPI 서버
* `ros_state_to_mqtt.py`
* `mqtt_command_to_ros.py`
* MQTT Subscriber

## MQTT 명령 통합 테스트

MQTT의 `robot/command` Topic으로 이동 명령을 발행했다.

```bash
mosquitto_pub \
    -h localhost \
    -t robot/command \
    -q 1 \
    -m '{"command":"forward","target_speed":0.5}'
```

명령은 다음 순서로 전달됐다.

```text
MQTT robot/command
        ↓
mqtt_command_to_ros
        ↓
ROS /robot/command
        ↓
virtual_robot_node
        ↓
ROS /robot/state
```

변경된 로봇 상태는 다시 다음 경로로 전달됐다.

```text
ROS /robot/state
        ├─ FastAPI GET /robot/state
        ├─ MQTT robot/state
        └─ Unity 로봇 위치 및 UI
```

이를 통해 MQTT 명령으로 로봇을 제어하고, 변경된 상태를 ROS·HTTP·MQTT·Unity에서 동시에 확인했다.

## HTTP 명령 통합 테스트

FastAPI의 `POST /robot/command` Endpoint를 이용해 로봇 명령을 전달했다.

```bash
curl -X POST \
    http://localhost:8000/robot/command \
    -H "Content-Type: application/json" \
    -d '{
        "command": "forward",
        "target_speed": 0.5
    }'
```

HTTP 요청은 다음 순서로 처리됐다.

```text
HTTP POST /robot/command
        ↓
FastAPI ROS Publisher
        ↓
ROS /robot/command
        ↓
virtual_robot_node
        ↓
ROS /robot/state
```

현재 상태는 다음 명령으로 확인했다.

```bash
curl http://localhost:8000/robot/state
```

FastAPI를 이용해 외부 웹 클라이언트에서도 로봇 명령을 전송하고 상태를 조회할 수 있음을 확인했다.

## Unity 통합 테스트

Unity에서 키보드 입력으로 명령을 발행하고 변경된 로봇 상태를 확인했다.

```text
Unity 키보드 입력
        ↓
ROS /robot/command
        ↓
virtual_robot_node
        ↓
ROS /robot/state
        ├─ Unity Rigidbody 위치 변경
        ├─ Unity 상태 UI 변경
        ├─ FastAPI 상태 변경
        └─ MQTT 상태 발행
```

Unity, FastAPI, MQTT 중 어떤 방식으로 명령을 보내더라도 동일한 `/robot/command` Topic으로 전달되고, 최종 상태는 `/robot/state` Topic을 기준으로 모든 시스템에 공유되는 구조를 확인했다.

## ROS 연결 구조 확인

다음 명령으로 실행 중인 ROS Node를 확인했다.

```bash
rosnode list
```

주요 Node는 다음과 같다.

```text
/virtual_robot_node
/virtual_robot_command_api
/ros_state_to_mqtt
/mqtt_command_to_ros
/unity_endpoint
```

Topic의 Publisher와 Subscriber 관계도 확인했다.

```bash
rostopic info /robot/state
rostopic info /robot/command
```

`rqt_graph`를 이용해 ROS 내부 통신 구조를 시각적으로 확인했다.

```bash
rqt_graph
```

MQTT Topic은 ROS Topic이 아니므로 `rqt_graph`에는 나타나지 않고, MQTT Bridge Node와 ROS Topic의 연결만 표시된다.


## 최종 통신 흐름

### MQTT를 이용한 제어

```text
MQTT 명령
→ MQTT → ROS Bridge
→ ROS 명령
→ 가상 로봇 상태 변경
→ MQTT·FastAPI·Unity에 상태 전달
```

### FastAPI를 이용한 제어

```text
HTTP POST 명령
→ FastAPI ROS Publisher
→ ROS 명령
→ 가상 로봇 상태 변경
→ MQTT·FastAPI·Unity에 상태 전달
```

### Unity를 이용한 제어

```text
Unity 키보드 명령
→ ROS 명령
→ 가상 로봇 상태 변경
→ Unity·FastAPI·MQTT에 상태 전달
```

## 학습 결과

Unity, ROS, FastAPI, MQTT를 연결한 가상 로봇 통합 시스템을 구현했다.

이번 학습을 통해 다음 내용을 이해했다.

* ROS Topic을 중심으로 한 통합 시스템 구성
* Unity와 ROS 간 양방향 통신
* FastAPI를 통한 로봇 상태 조회 및 명령 전달
* MQTT를 통한 로봇 상태 발행 및 명령 수신
* ROS ↔ MQTT Bridge 구조
* 여러 Publisher가 동일한 ROS Custom Message를 사용하는 방법
* `rosnode`, `rostopic`, `rqt_graph`를 이용한 연결 확인
* Shell Script를 이용한 여러 서비스 실행 및 종료 관리
* 하나의 로봇 상태를 여러 외부 시스템에 공유하는 구조

