
---

# Day07 README.md 요약본

아래 내용을 `Week03/Day07/README.md`에 붙여 넣으면 돼.

```md
# Week03 Day07 - CLI Based Virtual Robot Mini Project

## 학습 목표

Week03 Day07에서는 Week03 동안 구현한 ROS Python 노드를 정리하여 CLI 기반 가상 로봇 미니 프로젝트를 완성하였다.

가상 로봇은 `/robot/command` 토픽으로 명령을 받고, `/robot/state` 토픽으로 현재 상태를 publish한다. 사용자는 `robot_cli.py`를 통해 터미널에서 직접 명령을 입력할 수 있다.

---

## 전체 구조

```text
robot_cli.py
    ↓ publish
/robot/command
    ↓ subscribe
virtual_robot_node.py
    ↓ publish
/robot/state

```

### 배운점

Week03에서는 ROS Python 노드의 기본 구조부터 시작하여, 커스텀 메시지 설계, Publisher, Subscriber, Timer, Callback, 로그, 예외 처리까지 학습하였다.

이번 Day07 미니 프로젝트를 통해 로봇 시스템에서 명령 Topic과 상태 Topic을 분리하는 구조를 직접 구현할 수 있었다.

이 구조는 이후 Unity와 ROS를 연동할 때 그대로 확장할 수 있다. Unity는 /robot/command로 명령을 보내고, /robot/state를 구독하여 로봇 상태를 화면에 표시하는 방식으로 연결할 수 있다.
