## Day02 - Unity C# 키보드 이동

### 학습 내용

- `RobotKeyboardController.cs` 작성
- `W`, `A`, `S`, `D` 키 입력 처리
- `transform.position`으로 전진/후진 이동
- `transform.Rotate()`로 좌회전/우회전 구현

### 입력 키

```text
W: forward
S: backward
A: turn left
D: turn right
```

### 발생한 오류
```
InvalidOperationException:
You are trying to read Input using the UnityEngine.Input class,
but you have switched active Input handling to Input System package in Player Settings.
```

### 해결 방법
-Unity 설정에서 Active Input Handling을 Both로 변경하였음
=> 사용하는 버전이 unity 6xxx 버전이기에, input 시스템이 새로 변경되었음. 이를 구버전 혼용 가능으로 설정 변경
```
Edit > Project Settings > Player
> Other Settings
> Active Input Handling
> Both
```
