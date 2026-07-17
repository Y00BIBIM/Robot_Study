Week04 Day05 - ROS 상태 수신 및 Unity UI 표시
학습 목표

ROS에서 발행하는 /robot/state 토픽을 Unity에서 구독하고, 수신한 로봇 상태를 Unity UI에 표시한다.

RobotState 메시지 구조
string robot_id
float64 x
float64 y
float64 theta
float64 speed
float64 battery
string status

ROS의 float64 타입은 Unity C#에서 double 타입으로 생성된다.

학습 내용
Unity의 ROS-TCP-Connector를 사용하여 /robot/state 토픽 구독
RobotState.msg를 기반으로 RobotStateMsg.cs 생성
RobotStateSubscriber.cs 작성
ROS에서 수신한 값을 Unity 내부 변수에 저장
TextMeshPro UI를 이용해 위치, 방향, 상태 표시
Inspector에서 Subscriber와 UI Text 오브젝트 연결
ROS 좌표의 y 값을 Unity의 z 좌표로 사용
통신 구조
virtual_robot_node.py
        ↓
ROS /robot/state
        ↓
RobotStateSubscriber.cs
        ↓
RobotStateUI.cs
        ↓
Unity UI 갱신
주요 코드 역할

RobotStateSubscriber.cs는 ROS 메시지를 수신하고 다음 값을 저장한다.

RobotId
TargetX
TargetZ
TargetTheta
RobotSpeed
RobotBattery
RobotStatus

RobotStateUI.cs는 저장된 값을 읽어 화면에 표시한다.

Position: (x, z)
Theta: 현재 방향
Status: 현재 로봇 상태
Inspector 연결

RobotStateUI 컴포넌트의 다음 항목을 Hierarchy의 실제 오브젝트와 연결했다.

State Subscriber → RobotStateSubscriber가 붙은 ROSManager
Position Text    → PositionText
Direction Text   → DirectionText
Status Text      → StatusText
Connection Text  → ConnectionText

Inspector 연결이 누락되면 NullReferenceException이 발생할 수 있다.
