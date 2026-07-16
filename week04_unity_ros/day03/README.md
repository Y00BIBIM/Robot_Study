# Week04 Day03 - ROS-TCP-Connector & ROS-TCP-Endpoint Setup

## 학습 목표

Week04 Day03에서는 Unity와 ROS가 통신할 수 있도록 연결 환경을 구성하였다.

Unity 쪽에는 `ROS-TCP-Connector`를 설치하고, ROS 쪽에는 `ROS-TCP-Endpoint`를 설치하여 Unity와 ROS 사이에서 메시지를 주고받을 수 있는 TCP 통신 구조를 준비하였다.

---

## 전체 구조

```text
Unity
  └── ROS-TCP-Connector
          ↓ TCP 통신
ROS
  └── ROS-TCP-Endpoint
          ↓
ROS Topic
```

---

## Unity 쪽 설정

Unity에서 ROS와 통신하기 위해 `ROS-TCP-Connector` 패키지를 설치하였다.

### 설치 방법

Unity 상단 메뉴에서 다음 경로로 이동하였다.

```text
Window > Package Manager
```

그다음 `+` 버튼을 누르고 다음 항목을 선택하였다.

```text
Add package from git URL...
```

입력한 Git URL:

```text
https://github.com/Unity-Technologies/ROS-TCP-Connector.git?path=/com.unity.robotics.ros-tcp-connector
```

설치가 완료되면 Unity 상단 메뉴에 다음 항목이 생성된다.

```text
Robotics
```

---

## ROS 쪽 설정

ROS 쪽에서는 `ROS-TCP-Endpoint` 패키지를 catkin workspace에 설치하였다.

### 설치 명령어

```bash
cd ~/catkin_ws/src
git clone https://github.com/Unity-Technologies/ROS-TCP-Endpoint.git
```

설치 후 catkin workspace를 빌드하였다.

```bash
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

---

## ROS-TCP-Endpoint 실행

Unity와 ROS를 연결하기 위해 ROS 쪽에서 endpoint를 실행하였다.

```bash
cd ~/catkin_ws
source devel/setup.bash
roslaunch ros_tcp_endpoint endpoint.launch
```

실행 시 다음과 같은 설정이 확인되었다.

```text
/unity_endpoint/tcp_ip: 0.0.0.0
/unity_endpoint/tcp_port: 10000
```

즉, ROS-TCP-Endpoint는 기본적으로 `0.0.0.0:10000`에서 Unity의 연결을 기다린다.

---

## Unity ROS Settings 설정

Unity에서 다음 메뉴로 이동하였다.

```text
Robotics > ROS Settings
```

설정해야 하는 값은 다음과 같다.

```text
ROS IP Address: Ubuntu IP 주소
ROS Port: 10000
```

Ubuntu의 IP 주소는 다음 명령어로 확인할 수 있다.

```bash
hostname -I
```

Windows에서 Unity를 실행하고 Ubuntu VM 또는 WSL에서 ROS를 실행하는 경우, `127.0.0.1`이 아니라 Ubuntu 쪽 IP 주소를 입력해야 한다.

---

## 발생한 오류

### 오류 내용

ROS-TCP-Endpoint 실행 중 다음 오류가 발생하였다.

```text
/usr/bin/env: ‘python’: No such file or directory
```

전체 상황은 `roslaunch ros_tcp_endpoint endpoint.launch` 실행 중 `default_server_endpoint.py`가 실행되지 못하고 종료되는 문제였다.

---

## 오류 원인

`ROS-TCP-Endpoint`의 Python 실행 파일이 다음과 같은 형태로 실행되려고 했다.

```python
#!/usr/bin/env python
```

하지만 현재 Ubuntu 환경에는 `python` 명령어가 없고 `python3`만 존재해서 발생한 오류였다.

---

## 해결 방법

Ubuntu에서 `python` 명령어가 `python3`를 가리키도록 다음 패키지를 설치하였다.

```bash
sudo apt update
sudo apt install python-is-python3
```

설치 후 확인:

```bash
python --version
```

정상적으로 Python 3 버전이 출력되면 다시 endpoint를 실행한다.

```bash
cd ~/catkin_ws
source devel/setup.bash
roslaunch ros_tcp_endpoint endpoint.launch
```

---

## 확인한 점

- Unity에 `ROS-TCP-Connector`를 설치하였다.
- ROS에 `ROS-TCP-Endpoint`를 설치하였다.
- `catkin_make`로 ROS workspace를 빌드하였다.
- `roslaunch ros_tcp_endpoint endpoint.launch`를 실행하였다.
- Python 실행 오류를 해결하였다.
- Unity와 ROS가 통신할 준비를 완료하였다.

---

## 배운 점

Unity와 ROS가 직접 같은 프로세스에서 실행되는 것이 아니라, Unity 쪽의 `ROS-TCP-Connector`와 ROS 쪽의 `ROS-TCP-Endpoint`가 TCP 통신으로 연결된다.

Unity는 사용자 입력과 시각화를 담당하고, ROS는 로봇 명령 처리와 상태 관리를 담당한다.

Day03에서는 실제 메시지를 주고받기 전, Unity와 ROS가 통신할 수 있는 기본 연결 환경을 구성하였다.
