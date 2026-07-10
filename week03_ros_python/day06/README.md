# Week03 Day06 - Log and Exception Handling

## 학습 목표

Week03 Day06에서는 기존 `virtual_robot_node.py`에 로그와 예외 처리 기능을 추가하였다.

Day05까지는 로봇 명령을 받고 상태를 갱신하는 기본 구조를 구현하였다. Day06에서는 잘못된 명령, 비정상적인 속도 값, 배터리 부족 상황 등을 처리하고, 각 상황을 ROS 로그로 기록하도록 개선하였다.

---

## 학습 내용

### 1. ROS 로그 사용

ROS Python 노드에서 다음 로그 함수를 사용하였다.

```python
rospy.loginfo()
rospy.logwarn()
rospy.logerr()
```

### 2. 명령 검증

로봇이 처리할 수 있는 명령을 제한하였다.

```
forward
backward
turn_left
turn_right
stop
```

### 3. 속도 값 검증

'target_speed'값이 음수이거나 너무 큰 경우를 처리하였다.
음수 속도는 절대값을 이용해 양수로 변환했고, 너무 큰 속도는 최대 속도 값인 5.0으로 제한하였다.
이를 통해 잘못된 입력으로 로봇 상태가 비정상적으로 변화하는 것을 방지하였다.

### 4. 예외 처리

명령 처리 과정에서 오류가 발생하더라도 노드가 바로 종료되지 않도록 'try-except'를 사용하였다.

```
try:
    # command processing
except Exception as e:
    rospy.logerr("Error while processing command: %s", str(e))
```

