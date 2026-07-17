Week04 Day06 - Rigidbody 기반 로봇 이동
학습 목표

ROS에서 수신한 위치와 방향을 Unity의 Rigidbody에 적용하여 가상 로봇을 이동시킨다.

학습 내용
VirtualRobot 최상위 오브젝트에 Rigidbody 추가
로봇과 바닥에 Collider 설정
RobotPhysicsController.cs 작성
FixedUpdate()에서 물리 이동 처리
Rigidbody.MovePosition()을 사용한 위치 이동
Rigidbody.MoveRotation()을 사용한 방향 회전
ROS의 double 값을 Unity의 float로 형 변환
잘못된 NaN, Infinity 좌표 검사
기존 transform.Translate() 직접 이동 코드 제거
Rigidbody 설정
Use Gravity: On
Is Kinematic: Off
Interpolate: Interpolate
Collision Detection: Continuous

Constraints:
- Freeze Rotation X: On
- Freeze Rotation Y: Off
- Freeze Rotation Z: On

X축과 Z축 회전을 고정하여 로봇이 넘어지는 것을 방지하고, Y축 회전은 허용했다.

이동 구조
ROS /robot/state
        ↓
RobotStateSubscriber
        ↓
TargetX, TargetZ, TargetTheta
        ↓
RobotPhysicsController
        ↓
Rigidbody.MovePosition
Rigidbody.MoveRotation

ROS 메시지의 좌표를 Unity 좌표로 다음과 같이 사용했다.

ROS x → Unity x
ROS y → Unity z

ROS의 float64는 C#의 double이지만, Unity의 Vector3와 Quaternion은 float를 사용한다. 따라서 물리 이동에 적용할 때 명시적으로 형 변환했다.

Vector3 targetPosition = new Vector3(
    (float)stateSubscriber.TargetX,
    robotRigidbody.position.y,
    (float)stateSubscriber.TargetZ
);
theta 처리

ROS의 theta 값은 로봇의 회전 방향을 나타낸다.

ROS 노드에서 theta를 라디안으로 관리한다면 Unity의 회전 값에 적용하기 전에 도 단위로 변환해야 한다.

float thetaDegrees =
    (float)(stateSubscriber.TargetTheta * Mathf.Rad2Deg);
발생한 오류와 해결
1. ArgumentOutOfRangeException
Index and count must refer to a location within the buffer.
Non-negative number required.

원인은 ROS와 Unity가 서로 다른 RobotState 메시지 구조를 사용한 것이었다.

Unity가 기존에 다음과 같은 잘못된 구조를 사용하고 있었다.

x
y
direction
status

실제 ROS 메시지는 다음 7개 필드로 구성되어 있었다.

robot_id
x
y
theta
speed
battery
status

첫 번째 robot_id와 중간 필드가 누락되면서 메시지 바이트를 잘못 해석했고, 문자열 길이와 숫자 값이 비정상적으로 변환되었다.

해결 방법:

실제 RobotState.msg 구조 확인
ROS 패키지 재빌드
기존 Unity RobotStateMsg.cs 삭제
정확한 .msg 파일을 기준으로 Unity 메시지 재생성
모든 ROS 노드와 Unity 재시작
2. 비정상적인 좌표값 수신
x=3.49379741348268E+228
y=-3.26463690285594E-211

실제 좌표가 아니라 메시지 구조 불일치 때문에 바이트를 잘못 해석한 값이었다.

메시지 재생성 후 정상적인 좌표값을 수신할 수 있었다.

3. Rigidbody NaN 오류
Rigidbody.position assign attempt is not valid.
Input position is { NaN, ... }

TargetX 또는 TargetZ에 잘못된 값이 들어간 상태에서 MovePosition()을 호출하여 발생했다.

이동 전에 다음 값을 검사하도록 수정했다.

double.IsNaN(value)
double.IsInfinity(value)

유효하지 않은 좌표를 수신하면 해당 프레임의 이동을 실행하지 않도록 처리했다.

Day06 결과
ROS 상태값을 Unity에서 정상적으로 수신
ROS 위치를 Unity 좌표로 변환
Rigidbody를 이용해 로봇 이동
ROS 방향값을 이용해 로봇 회전
Collider를 이용한 물리 충돌 기반 마련
잘못된 메시지 및 좌표값에 대한 예외 처리 추가
