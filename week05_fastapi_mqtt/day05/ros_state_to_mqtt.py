#!/usr/bin/env python3

import json
import math
import threading

import paho.mqtt.client as mqtt
import rospy

from virtual_robot.msg import RobotState

MQTT_STATE_TOPIC = "robot/state"

mqtt_client = None
mqtt_connected = threading.Event()

def on_connect(
	cleint,
	userdata,
	connect_flags,
	reason_code,
	properties,
):
	"""MQTT Broker 연결 결과 처리."""
	if reason_code == 0:
		mqtt_connected.set()
		rospy.loginfo("Connected to MQTT Broker")
	else:
		mqtt_connected.clear()
		rospy.logerr(
			f"MQTT connection failed: {reason_code}"
		)
		
def on_disconnect(
	client,
	userdata,
	disconnect_flags,
	reason_code,
	properties,
):
	"""MQTT 연결 끊어졌을 때 실행."""
	mqtt_connected.clear()
	
	if reason_code != 0:
		rospy.logwarn(
			f"Unexpected MQTT disconnection: {reason_code}"
		)

def robot_state_callback(message: RobotState) -> None:
    """
    ROS /robot/state 메시지를 JSON으로 변환해
    MQTT robot/state Topic으로 발행한다.
    """
    if not mqtt_connected.is_set():
        rospy.logwarn_throttle(
            5,
            "MQTT Broker가 연결되지 않아 상태를 발행할 수 없습니다.",
        )
        return

    numeric_values = [
        message.x,
        message.y,
        message.theta,
        message.speed,
        message.battery,
    ]

    # NaN 또는 Infinity가 MQTT JSON에 들어가는 것을 방지한다.
    if not all(math.isfinite(value) for value in numeric_values):
        rospy.logwarn(
            "Invalid RobotState detected: NaN or Infinity"
        )
        return

    payload = {
        "robot_id": message.robot_id,
        "x": message.x,
        "y": message.y,
        "theta": message.theta,
        "speed": message.speed,
        "battery": message.battery,
        "status": message.status,
    }

    try:
        payload_text = json.dumps(
            payload,
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError) as error:
        rospy.logerr(f"JSON serialization failed: {error}")
        return

    publish_result = mqtt_client.publish(
        topic=MQTT_STATE_TOPIC,
        payload=payload_text,
        qos=1,
        retain=True,
    )

    if publish_result.rc != mqtt.MQTT_ERR_SUCCESS:
        rospy.logwarn(
            f"MQTT publish failed: rc={publish_result.rc}"
        )
        return

    rospy.loginfo_throttle(
        1,
        f"ROS → MQTT state: {payload_text}",
    )


def shutdown() -> None:
    """ROS Node 종료 시 MQTT 연결을 정리한다."""
    if mqtt_client is not None:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()


def main() -> None:
    global mqtt_client

    rospy.init_node(
        "ros_state_to_mqtt",
        anonymous=False,
    )

    broker_host = rospy.get_param(
        "~broker_host",
        "localhost",
    )
    broker_port = rospy.get_param(
        "~broker_port",
        1883,
    )

    mqtt_client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="ros_state_to_mqtt",
    )

    mqtt_client.on_connect = on_connect
    mqtt_client.on_disconnect = on_disconnect

    try:
        mqtt_client.connect(
            host=broker_host,
            port=broker_port,
            keepalive=60,
        )
    except OSError as error:
        rospy.logfatal(
            f"MQTT Broker connection failed: {error}"
        )
        return

    mqtt_client.loop_start()

    rospy.Subscriber(
        "/robot/state",
        RobotState,
        robot_state_callback,
        queue_size=10,
    )

    rospy.on_shutdown(shutdown)

    rospy.loginfo(
        "ROS /robot/state → MQTT robot/state bridge started"
    )

    rospy.spin()


if __name__ == "__main__":
    main()
