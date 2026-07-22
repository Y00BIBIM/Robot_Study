# Week05 Day01 — FastAPI 기본 서버 구축

## 학습 목표

FastAPI를 이용해 HTTP 요청을 처리하고, 가상 로봇 상태를 JSON 형식으로 반환하는 REST API 서버를 구현했다.

## 학습 내용

FastAPI 애플리케이션을 생성하고 다음 Endpoint를 구현했다.

* `GET /`

  * API 서버의 기본 정보 반환
* `GET /health`

  * 서버의 정상 작동 여부 확인
* `GET /robot/state`

  * 가상 로봇의 상태 정보 반환
* `GET /docs`

  * FastAPI가 자동으로 생성한 Swagger UI 확인

로봇 상태 응답 형식은 Pydantic의 `BaseModel`을 이용해 정의했다.

```python
class RobotStateResponse(BaseModel):
    robot_id: str
    x: float
    y: float
    theta: float
    speed: float
    battery: float
    status: str
```

Pydantic 모델을 사용하면 API가 반환하는 데이터의 필드와 자료형을 명확하게 지정할 수 있다. 또한 잘못된 형식의 데이터가 사용되는 것을 방지할 수 있다.

## FastAPI 서버 실행

FastAPI 애플리케이션은 Uvicorn을 이용해 실행했다.

```bash
python -m uvicorn app:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload
```

각 옵션의 의미는 다음과 같다.

* `app:app`

  * `app.py` 파일에 있는 `app` 객체 실행
* `--host 0.0.0.0`

  * 외부 컴퓨터에서도 서버에 접근할 수 있도록 설정
* `--port 8000`

  * 서버가 사용할 포트를 8000번으로 지정
* `--reload`

  * 코드가 수정되면 서버를 자동으로 재시작

서버 실행 후 다음 명령으로 API 응답을 확인했다.

```bash
curl http://localhost:8000/health
```

```bash
curl http://localhost:8000/robot/state
```

브라우저에서는 다음 주소로 접속해 Swagger UI를 확인했다.

```text
http://localhost:8000/docs
```

## 발생한 오류

Uvicorn 실행 중 다음 오류가 발생했다.

```text
pkg_resources.DistributionNotFound:
The 'uvloop>=0.14.0' distribution was not found
```

오류 메시지에서 다음 경로가 표시되었다.

```text
/usr/bin/uvicorn
```

이는 Python 가상환경에 설치된 Uvicorn이 아니라 Ubuntu 시스템에 전역으로 설치된 Uvicorn이 실행되고 있다는 의미였다.

## 오류 해결

먼저 Week05 가상환경을 활성화했다.

```bash
cd ~/robot_study/Week05/Day01
source ../venv/bin/activate
```

실행 경로를 확인했다.

```bash
which python
which pip
which uvicorn
```

이후 가상환경 안에 FastAPI와 Uvicorn을 설치했다.

```bash
python -m pip install "fastapi==0.115.0" \
    "uvicorn[standard]==0.30.6"
```

마지막으로 `uvicorn` 명령을 직접 실행하지 않고, 현재 Python 환경을 명시하는 방식으로 서버를 실행했다.

```bash
python -m uvicorn app:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload
```

이를 통해 시스템에 설치된 `/usr/bin/uvicorn`이 실행되는 문제를 해결했다.

## 학습 결과

FastAPI를 이용해 로봇 상태를 제공하는 기본 REST API 서버를 구현했다.

이번 학습을 통해 다음 내용을 이해했다.

* HTTP GET 요청
* REST API와 Endpoint
* JSON 응답
* FastAPI 애플리케이션 생성
* Uvicorn 서버 실행
* Pydantic 데이터 모델
* Swagger UI
* Python 가상환경
* `which` 명령을 이용한 프로그램 실행 경로 확인
* `python -m` 방식으로 현재 Python 환경의 패키지 실행

