# Robot Intern Study

로봇 프로그래밍 인턴 준비를 위한 학습 프로젝트입니다.

## 목표

Unity + ROS + FastAPI + DB 기반 가상 로봇 관제 미니 시스템을 구현하는 것이 목표입니다.

## 학습 기간

2026년 6월 19일 ~ 2026년 7월 31일

## 현재까지 학습 내용

### 6월 19일

- Linux 기본 명령어 학습
- 터미널에서 폴더 생성, 이동, 파일 확인 연습

### 6월 20일

- Python 기본 문법 복습
- 함수, 클래스, 딕셔너리, 예외 처리 복습

### 6월 21일

- Python 가상환경 venv 생성
- pip 패키지 설치
- requirements.txt 생성
- .gitignore 작성
- RobotState 클래스 작성
- CLI 기반 로봇 명령 시뮬레이터 작성

### 6월 22일

- IP, Port, HTTP, JSON 개념 학습
- JSON 파일 저장/읽기 실습
- FastAPI 서버 작성
- Python requests로 API 요청 실습

### 6월 23일

- Git/GitHub 기본 개념 학습
- 로컬 Git 저장소 생성
- commit 작성
- GitHub 원격 저장소 연결
- push 실습

## 프로젝트 구조

```text
robot-intern-study/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── robot_state.json
└── src/
    ├── config.py
    ├── robot_state.py
    ├── main.py
    ├── command_simulator.py
    ├── json_practice.py
    ├── simple_api_server.py
    └── http_client.py
