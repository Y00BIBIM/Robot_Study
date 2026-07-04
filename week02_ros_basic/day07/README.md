# Week02 Day07 - ROS 1 종합 복습

## 오늘 학습한 내용

- catkin workspace 구조 복습
- ROS package 생성 복습
- Python Publisher 작성
- Python Subscriber 작성
- turtlesim 제어
- rqt_graph로 ROS 통신 구조 확인

## 핵심 개념

Publisher는 Topic에 메시지를 발행한다.  
Subscriber는 Topic에서 메시지를 구독한다.  
Message Type이 맞아야 통신할 수 있다.

## 실습 결과

- `/turtle1/cmd_vel` 토픽으로 `geometry_msgs/Twist` 메시지를 발행하여 거북이를 움직였다.
- `/turtle1/pose` 토픽을 구독하여 거북이의 위치를 출력했다.
