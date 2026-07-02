# Week02 Day03-04: ROS Topic, Message, Service, Parameter

## 1. Topic 실습

### 확인한 Topic 목록
- /turtle1/cmd_vel
- /turtle1/pose

### /turtle1/cmd_vel
- Type: geometry_msgs/Twist
- Publisher: /teleop_turtle
- Subscriber: /turtlesim
- 역할: 거북이 이동 명령 전달

### /turtle1/pose
- Type: turtlesim/Pose
- Publisher : /teleop_turtle
- Subscriber: /turtlesim
- 역할: 거북이의 현재 위치와 방향 정보 전달

## 2. Message 구조

geometry_msgs/Twist는 linear와 angular로 구성된다.

- linear.x: 전진 속도
- angular.z: 회전 속도

## 3. Service 실습

사용한 Service:
- /spawn
- /kill
- /clear

/spawn은 새 거북이를 생성하는 Service이다.

## 4. Parameter 실습

확인한 Parameter:
- /background_r
- /background_g
- /background_b

rosparam set 명령어로 배경색을 변경했다.

## 5. 느낀 점

Topic은 계속 흐르는 데이터 통신이고,
Service는 요청과 응답 방식의 통신이라는 차이를 이해했다.
