-Today Study Progress Tree-

Robot_Study/
└── Week04/
    ├── Day01_Day04/
    │   ├── README.md
    │   ├── Scripts/
    │   │   ├── RobotKeyboardController.cs
    │   │   └── RobotCommandPublisher.cs
    │   └── Notes/
    │       └── unity_ros_setup.md
    
# Week04 Day01~Day04 - Unity + ROS Integration

## 학습 목표

Week04에서는 Unity와 ROS를 연동하는 기초 과정을 학습하였다.

Day01에서는 Unity 프로젝트를 생성하고 간단한 가상 로봇 오브젝트를 만들었다.  
Day02에서는 Unity C# 스크립트로 키보드 입력을 받아 로봇을 이동시켰다.  
Day03에서는 ROS-TCP-Connector와 ROS-TCP-Endpoint를 설치하여 Unity와 ROS가 통신할 수 있는 환경을 구성하였다.  
Day04에서는 Unity 키보드 입력을 ROS의 `/robot/command` 토픽으로 publish하였다.

---

## Day01 - Unity 프로젝트 생성

### 학습 내용

- Unity 3D 프로젝트 생성
- `Assets/Scenes`, `Assets/Scripts`, `Assets/Materials`, `Assets/Prefabs` 폴더 구성
- `VirtualRobot` 오브젝트 생성
- `Body`, `Head`, `DirectionMarker`를 이용한 간단한 로봇 형태 제작
- `Ground` Plane 생성
- Camera 위치 조정

### 결과

Unity Scene 안에 간단한 가상 로봇 오브젝트를 만들었다.

---




