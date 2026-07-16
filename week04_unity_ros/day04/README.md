# Week04 Day04 - Unity to ROS Message Publishing

## 학습 목표

Week04 Day04에서는 Unity에서 키보드 입력을 받아 ROS의 `/robot/command` 토픽으로 명령 메시지를 publish하는 기능을 구현하였다.

Day02에서는 Unity 내부에서만 `W`, `A`, `S`, `D` 키로 오브젝트를 움직였다.  
Day04에서는 이 입력을 ROS 명령 메시지로 변환하여 ROS Python 노드로 전달하는 구조를 만들었다.

---

## 전체 통신 구조

```text
Unity Keyboard Input
        ↓
RobotCommandPublisher.cs
        ↓ publish
/robot/command
        ↓ subscribe
virtual_robot_node.py
        ↓ publish
/robot/state
```

---

## 사용한 ROS 메시지

Week03에서 만든 커스텀 메시지를 Unity에서도 사용하였다.

### RobotCommand.msg

```text
string command
float64 target_speed
```

이 메시지는 Unity에서 ROS로 로봇 명령을 보낼 때 사용한다.

### RobotState.msg

```text
string robot_id
float64 x
float64 y
float64 theta
float64 speed
float64 battery
string status
```

이 메시지는 ROS에서 로봇의 현재 상태를 표현할 때 사용한다.

Day04에서는 주로 `RobotCommand.msg`를 사용하였다.

---

## Unity에서 ROS 메시지 생성

Unity에서 ROS 커스텀 메시지를 사용하려면 `.msg` 파일을 C# 메시지 클래스로 변환해야 한다.

Unity 상단 메뉴에서 다음 기능을 사용하였다.

```text
Robotics > Generate ROS Messages...
```

---

## ROS message path 설정

처음에는 다음 경로를 입력하였다.

```text
~/caktin_ws/src/virtual_robot/msg
```

하지만 이 경로에는 문제가 있었다.

### 문제점

```text
1. caktin_ws가 아니라 catkin_ws가 맞다.
2. Unity가 Windows에서 실행 중이면 Ubuntu의 ~/catkin_ws 경로를 직접 읽을 수 없다.
3. ROS message path에는 msg 폴더 자체보다 ROS 패키지 폴더 또는 메시지들이 들어 있는 상위 폴더를 지정하는 것이 좋다.
```

---

## 해결 방법

Unity 프로젝트 내부에 ROS 메시지 파일을 복사하여 사용하였다.

Unity 프로젝트 안에 다음 폴더 구조를 만들었다.

```text
Assets/
└── ROSMessages/
    └── virtual_robot/
        └── msg/
            ├── RobotCommand.msg
            └── RobotState.msg
```

그다음 `Generate ROS Messages...` 창에서 `ROS message path`를 다음 폴더로 지정하였다.

```text
Assets/ROSMessages
```

또는 실제 Windows 절대 경로로 지정할 수 있다.

```text
C:/Users/사용자이름/프로젝트경로/RobotUnityROS/Assets/ROSMessages
```

---

## 메시지 생성 결과

정상적으로 메시지가 생성되면 Unity 프로젝트 안에 다음과 같은 C# 파일이 생성된다.

```text
Assets/RosMessages/VirtualRobot/msg/RobotCommandMsg.cs
Assets/RosMessages/VirtualRobot/msg/RobotStateMsg.cs
```

이후 C# 스크립트에서 다음 namespace를 사용할 수 있다.

```csharp
using RosMessageTypes.VirtualRobot;
```

그리고 다음과 같이 메시지 객체를 생성할 수 있다.

```csharp
RobotCommandMsg msg = new RobotCommandMsg();
```

---

## RobotCommandPublisher.cs

Unity에서 키보드 입력을 받아 `/robot/command` 토픽으로 명령을 publish하는 스크립트를 작성하였다.

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.VirtualRobot;

public class RobotCommandPublisher : MonoBehaviour
{
    public string topicName = "/robot/command";
    public double targetSpeed = 1.0;

    private ROSConnection ros;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();
        ros.RegisterPublisher<RobotCommandMsg>(topicName);

        Debug.Log("RobotCommandPublisher started. Publishing to " + topicName);
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.W))
        {
            PublishCommand("forward", targetSpeed);
        }
        else if (Input.GetKeyDown(KeyCode.S))
        {
            PublishCommand("backward", targetSpeed);
        }
        else if (Input.GetKeyDown(KeyCode.A))
        {
            PublishCommand("turn_left", 0.0);
        }
        else if (Input.GetKeyDown(KeyCode.D))
        {
            PublishCommand("turn_right", 0.0);
        }
        else if (Input.GetKeyDown(KeyCode.Space))
        {
            PublishCommand("stop", 0.0);
        }
    }

    void PublishCommand(string command, double speed)
    {
        RobotCommandMsg msg = new RobotCommandMsg();
        msg.command = command;
        msg.target_speed = speed;

        ros.Publish(topicName, msg);

        Debug.Log("Published command: " + command + ", target_speed: " + speed);
    }
}
```

---

## Unity 입력과 ROS 명령 매핑

```text
W     -> forward
S     -> backward
A     -> turn_left
D     -> turn_right
Space -> stop
```

---

## Unity 오브젝트 설정

`RobotCommandPublisher.cs` 스크립트를 `VirtualRobot` 오브젝트에 추가하였다.

```text
VirtualRobot
├── RobotKeyboardController
└── RobotCommandPublisher
```

Day04에서는 Unity 오브젝트를 직접 움직이는 것보다 ROS로 명령을 보내는 것이 핵심이므로, 테스트 중에는 `RobotKeyboardController`를 비활성화해도 된다.

---

## 실행 방법

### 1. ROS Master 실행

```bash
roscore
```

### 2. ROS-TCP-Endpoint 실행

```bash
cd ~/catkin_ws
source devel/setup.bash
roslaunch ros_tcp_endpoint endpoint.launch
```

### 3. 가상 로봇 노드 실행

```bash
cd ~/catkin_ws
source devel/setup.bash
rosrun virtual_robot virtual_robot_node.py
```

### 4. ROS 토픽 확인

```bash
rostopic echo /robot/command
```

또는 로봇 상태 확인:

```bash
rostopic echo /robot/state
```

### 5. Unity 실행

Unity에서 Play 버튼을 누른 뒤 키보드를 입력한다.

```text
W, A, S, D, Space
```

---

## 테스트 결과

Unity에서 `W` 키를 누르면 ROS의 `/robot/command` 토픽에 다음과 같은 메시지가 publish된다.

```text
command: "forward"
target_speed: 1.0
```

Unity에서 `Space` 키를 누르면 다음과 같은 정지 명령이 publish된다.

```text
command: "stop"
target_speed: 0.0
```

ROS의 `virtual_robot_node.py`는 `/robot/command` 토픽을 subscribe하고 있으므로, Unity에서 보낸 명령을 받아 로봇 상태를 변경한다.

---

## 발생한 문제

### 문제 1. Generate ROS Messages 창에서 Build 버튼이 보이지 않음

Unity 600.3.10f1 환경에서 `Generate ROS Messages...` 창에 `Build` 또는 `Generate` 버튼이 바로 보이지 않았다.

### 원인

입력한 ROS message path가 잘못되었거나, Unity에서 접근할 수 없는 Ubuntu 경로를 입력했기 때문일 가능성이 높았다.

잘못 입력한 경로:

```text
~/caktin_ws/src/virtual_robot/msg
```

### 해결 방법

Unity 프로젝트 내부에 `.msg` 파일을 복사하고, `ROS message path`를 Unity 프로젝트 내부의 `Assets/ROSMessages`로 지정하였다.

```text
Assets/ROSMessages
```

이후 `virtual_robot/msg` 폴더가 인식되면 `Build 2 msgs` 또는 비슷한 이름의 버튼을 통해 메시지를 생성할 수 있다.

---

## 발생한 문제 2. Unity Input 오류

Unity에서 기존 `Input.GetKeyDown()` 코드를 사용할 때 다음 오류가 발생할 수 있다.

```text
InvalidOperationException:
You are trying to read Input using the UnityEngine.Input class,
but you have switched active Input handling to Input System package in Player Settings.
```

### 해결 방법

Unity 설정에서 입력 방식을 `Both`로 변경하였다.

```text
Edit > Project Settings > Player
> Other Settings
> Active Input Handling
> Both
```

---

## 배운 점

Day04에서는 Unity에서 ROS로 메시지를 보내는 단방향 통신을 구현하였다.

Unity의 키보드 입력은 `RobotCommandPublisher.cs`에서 처리하고, 해당 입력은 `RobotCommandMsg`로 변환되어 ROS의 `/robot/command` 토픽으로 publish된다.

이 구조를 통해 Unity는 로봇 조작 인터페이스 역할을 하고, ROS는 실제 로봇 명령 처리와 상태 관리를 담당하게 된다.

다음 학습에서는 반대로 ROS의 `/robot/state` 토픽을 Unity에서 subscribe하여 Unity 화면에 로봇 상태를 표시하는 기능을 구현할 예정이다.
