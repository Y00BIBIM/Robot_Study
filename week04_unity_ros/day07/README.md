## Week04 Day07 - Unity·ROS 통합 및 최종 동작 검증

### 학습 목표

Week04에서 구현한 Unity와 ROS 기능을 하나로 통합하고, 명령 전송부터 상태 수신, UI 갱신, 물리 이동까지 전체 흐름을 검증한다.

### 전체 통신 구조

```text
Unity 키보드 입력
        ↓
RobotCommandPublisher
        ↓
ROS /robot/command
        ↓
virtual_robot_node.py
        ↓
로봇 위치·방향·상태 계산
        ↓
ROS /robot/state
        ↓
RobotStateSubscriber
        ├── RobotStateUI
        └── RobotPhysicsController
```

### 사용한 RobotState 메시지 구조

```text
string robot_id
float64 x
float64 y
float64 theta
float64 speed
float64 battery
string status
```

ROS의 `float64`는 Unity C#에서 `double`로 처리하고, `Vector3`와 `Quaternion`에 적용할 때 `float`로 형 변환한다.

---

### 학습 내용

#### 1. Unity Scene 및 Hierarchy 정리

Unity Scene의 오브젝트를 역할에 따라 정리했다.

```text
Week04_Day07
├── Main Camera
├── Directional Light
├── Ground
├── Obstacles
├── VirtualRobot
│   ├── RobotBody
│   ├── RobotHead
│   └── DirectionMarker
├── ROSManager
└── Canvas
    └── RobotStatePanel
```

각 오브젝트의 역할은 다음과 같다.

* `ROSManager`: ROS Topic 발행 및 구독
* `VirtualRobot`: Rigidbody 기반 가상 로봇
* `Canvas`: ROS에서 받은 상태 표시
* `Obstacles`: Collider 충돌 테스트

---

#### 2. Inspector 연결 최종 확인

`RobotPhysicsController`와 `RobotStateUI`가 `RobotStateSubscriber`의 데이터를 사용할 수 있도록 Inspector에서 오브젝트 참조를 연결했다.

```text
RobotPhysicsController
└── State Subscriber → ROSManager

RobotStateUI
├── State Subscriber → ROSManager
├── Connection Text → ConnectionText
├── Position Text → PositionText
├── Direction Text → DirectionText
└── Status Text → StatusText
```

Inspector 연결이 누락되면 `NullReferenceException`이 발생하거나 UI와 로봇 이동이 동작하지 않을 수 있다.

---

#### 3. ROS 상태 수신 시간 저장

`RobotStateSubscriber.cs`에 마지막 메시지 수신 시간을 저장하는 기능을 추가했다.

```csharp
public bool HasReceivedState { get; private set; }
public float LastReceivedTime { get; private set; }
```

메시지를 수신할 때 다음 값을 갱신한다.

```csharp
HasReceivedState = true;
LastReceivedTime = Time.time;
```

이를 통해 TCP 연결 자체가 유지되더라도 `/robot/state` 메시지가 일정 시간 동안 들어오지 않는 상태를 감지할 수 있다.

---

#### 4. ROS 상태 연결 Timeout 처리

Unity가 마지막 상태를 계속 `Connected`로 표시하지 않도록 Timeout 기능을 구현했다.

```text
상태 메시지 수신 중
→ Connection: Connected

일정 시간 동안 메시지 없음
→ Connection: State Timeout

아직 메시지를 한 번도 받지 않음
→ Connection: Waiting for ROS...
```

기본 Timeout 시간은 약 2초로 설정했다.

```csharp
bool isTimedOut =
    Time.time - stateSubscriber.LastReceivedTime
    > timeoutSeconds;
```

---

#### 5. Rigidbody 이동 안전 처리

`RobotPhysicsController.cs`에서 ROS 상태가 유효할 때만 로봇을 이동하도록 처리했다.

이동 전 다음 조건을 확인한다.

```text
- Subscriber가 연결되어 있는가?
- 상태 메시지를 한 번 이상 받았는가?
- 상태 수신 Timeout이 발생하지 않았는가?
- 위치 값이 NaN 또는 Infinity가 아닌가?
```

유효하지 않은 좌표는 Rigidbody에 적용하지 않는다.

```csharp
private bool IsValidNumber(double value)
{
    return !double.IsNaN(value) &&
           !double.IsInfinity(value);
}
```

이를 통해 다음과 같은 Unity 물리 오류를 방지했다.

```text
Rigidbody.position assign attempt is not valid.
Input position is { NaN, ... }
```

---

#### 6. ROS 좌표를 Unity 좌표로 적용

ROS의 2차원 좌표를 Unity의 3차원 좌표에 다음과 같이 적용했다.

```text
ROS x → Unity x
ROS y → Unity z
```

Unity의 높이 좌표인 `y`는 현재 Rigidbody 위치를 유지한다.

```csharp
Vector3 targetPosition = new Vector3(
    (float)stateSubscriber.TargetX,
    robotRigidbody.position.y,
    (float)stateSubscriber.TargetZ
);
```

`Vector3`는 `float` 기반이므로 ROS `float64` 값을 명시적으로 변환했다.

---

#### 7. theta를 Unity 회전에 적용

ROS의 `theta` 값을 Unity 로봇의 Y축 회전에 적용했다.

ROS에서 `theta`를 라디안으로 관리하는 경우 Unity에서 도 단위로 변환해야 한다.

```csharp
float angle =
    (float)stateSubscriber.TargetTheta
    * Mathf.Rad2Deg;
```

그다음 `Quaternion`과 `Rigidbody.MoveRotation()`을 이용해 부드럽게 회전시켰다.

```csharp
Quaternion targetRotation =
    Quaternion.Euler(0f, angle, 0f);
```

---

#### 8. 기존 직접 이동 코드 제거

Unity 키보드 입력 스크립트에서 다음과 같은 직접 이동 코드를 제거하거나 비활성화했다.

```csharp
transform.Translate(...);
transform.Rotate(...);
transform.position += ...;
```

키보드 입력은 이제 Unity 오브젝트를 직접 움직이지 않고 ROS 명령만 발행한다.

```text
키보드 입력
→ /robot/command 발행
→ ROS 상태 변경
→ /robot/state 수신
→ Rigidbody 이동
```

이 구조를 통해 ROS가 로봇 상태의 기준이 되도록 구성했다.

---

### 통합 테스트

#### 상태 수신 테스트

Unity 실행 후 `/robot/state`의 다음 값이 정상적으로 표시되는지 확인했다.

```text
robot_id
x
y
theta
speed
battery
status
```

비정상적으로 큰 지수 값이나 `NaN`이 표시되지 않는지 함께 확인했다.

#### 전진 테스트

```text
W 입력
→ /robot/command에 전진 명령 발행
→ ROS 위치 변경
→ Unity UI 위치 변경
→ VirtualRobot 이동
```

#### 회전 테스트

```text
A 또는 D 입력
→ ROS theta 변경
→ Unity 방향 UI 변경
→ VirtualRobot Y축 회전
```

#### 정지 테스트

```text
정지 명령
→ speed 값 0
→ status 값 stopped
→ 로봇 위치 변경 중단
```

#### 장애물 충돌 테스트

Cube 형태의 장애물을 배치하고 다음 내용을 확인했다.

* 로봇이 장애물을 통과하지 않는지 확인
* Rigidbody가 충돌 과정에서 넘어지지 않는지 확인
* Unity Console에 물리 오류가 반복되지 않는지 확인

#### 상태 노드 종료 테스트

`virtual_robot_node.py`를 종료한 뒤 일정 시간이 지나면 Unity UI에 다음 상태가 표시되도록 했다.

```text
Connection: State Timeout
```

Timeout 상태에서는 마지막 ROS 좌표를 계속 적용하지 않도록 로봇 이동도 중단했다.

#### 상태 노드 재실행 테스트

ROS 노드를 다시 실행하고 상태 메시지가 수신되면 다음 상태로 복구되는지 확인했다.

```text
Connection: Connected
```

---

### 주요 학습 포인트

* Unity와 ROS 간 양방향 통신 구조
* Unity Publisher와 Subscriber 역할 분리
* ROS 상태를 기준으로 Unity Rigidbody 이동
* ROS `float64`와 Unity `float` 간 형 변환
* ROS 라디안과 Unity 도 단위 변환
* `Update()`와 `FixedUpdate()`의 역할 차이
* Inspector를 통한 컴포넌트 참조 연결
* 상태 메시지 Timeout 감지
* `NaN`과 `Infinity` 값에 대한 방어 코드 작성
* Collider를 이용한 장애물 충돌 처리

---

### Week04 최종 결과

Week04를 통해 다음 통합 구조를 구현했다.

```text
Unity
├── 키보드 입력
├── ROS 명령 발행
├── ROS 상태 구독
├── 상태 UI 표시
└── Rigidbody 기반 로봇 이동

ROS 1
├── Unity 명령 수신
├── 가상 로봇 상태 계산
└── RobotState 메시지 발행
```

최종적으로 Unity에서 입력한 명령이 ROS를 거쳐 처리되고, 변경된 로봇 상태가 다시 Unity로 전달되어 UI와 가상 로봇 움직임에 반영되는 양방향 통신 흐름을 학습했다.
