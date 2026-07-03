1. catkin_ws는 왜 필요한가?
=> catkin is "ROS build system", and catkin_ws is catkin's workspace
----------------------------------------------------------------------------
2. src 폴더에는 무엇이 들어가는가?
=> build data(ROS package data)
-----------------------------------------------------------------------------
3. ROS package는 왜 만드는가?
=> through package, user can add specific ROS system chunk easliy 
-----------------------------------------------------------------------------
4. package.xml은 어떤 역할을 하는가?
=> write dependecy of this package
-----------------------------------------------------------------------------
5. catkin_make 후 source devel/setup.bash를 왜 해야 하는가?
=> announce the location of "catkin package" to current terminal

Today study progress

1. catkin_ws 확인
2. week2_turtle_practice 패키지 생성
3. catkin_make 빌드
4. scripts 폴더 생성
5. turtle_move_pub.py 작성
6. turtlesim을 코드로 움직이기
7. turtle_pose_sub.py 작성
8. pose 정보 출력하기
9. rqt_graph로 통신 구조 확인
10. Day05_Day06.md에 정리
11. GitHub에 commit


Today summary
-ROS의 워크스페이스는 catkin & catkin_ws
-Publisher는 ROS에게 데이터를 주고
-Subscriber는 ROS에게 있는 데이터를 받는다
