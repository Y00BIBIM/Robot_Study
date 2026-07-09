# Week03 Day04 & Day05 - Robot Message Design and Timer Node

## 학습 목표

Week03 Day04와 Day05에서는 ROS Python 노드에서 사용할 로봇 상태 메시지와 명령 메시지를 직접 설계하고, 이를 이용해 가상 로봇 노드를 구현하였다.

기존에는 `std_msgs/String` 타입으로 단순 문자열 명령을 주고받았지만, 이번 학습에서는 커스텀 메시지를 정의하여 로봇의 상태와 명령 데이터를 더 명확하게 관리하도록 개선하였다.

---

## Day04 - 메시지 구조 설계

Day04에서는 가상 로봇이 주고받을 메시지 구조를 직접 정의하였다.

### 생성한 메시지 파일

```text
virtual_robot/msg/RobotState.msg
virtual_robot/msg/RobotCommand.msg
