#!/usr/bin/env python3

import json
import math

import paho.mqtt.client as mqtt
import rospy

from virtual_robot.msg import RobotCommand


MQTT_COMMAND_TOPIC = "robot/command"

ALLOWED_COMMANDS = {
    "forward",
    "backward",
    "left",
    "right",
    "stop",
}

MIN_SPEED = 0.0
MAX_SPEED = 2.0

mqtt_client = None
ros_command_publisher = None


def on_connect(
    client,
    userdata,
    connect_flags,
    reason_code,
    properties,
):
    """Broker 연결 후 robot/command Topic을 구독한다."""
    if reason_code != 0:
        rospy.logerr(
            f"MQTT connection failed: {reason_code}"
        )
        return

    rospy.loginfo("Connected to MQTT Broker")

    result, message_id = client.subscribe(
        MQTT_COMMAND_TOPIC,
        qos=1,
    )

    if result == mqtt.MQTT_ERR_SUCCESS:
        rospy.loginfo(
            f"Subscribed to MQTT Topic: {MQTT_COMMAND_TOPIC}"
        )
    else:
        rospy.logerr(
            f"MQTT subscription failed: rc={result}"
        )


def on_message(
    client,
    userdata,
    message,
):
    """
    MQTT JSON 명령을 검증한 후
    ROS RobotCommand 메시지로 발행한다.
    """
    try:
        payload_text = message.payload.decode("utf-8")
    except UnicodeDecodeError as error:
        rospy.logwarn(f"Invalid UTF-8 payload: {error}")
        return

    try:
        payload = json.loads(payload_text)
    except json.JSONDecodeError as error:
        rospy.logwarn(f"Invalid JSON payload: {error}")
        return

    if not isinstance(payload, dict):
        rospy.logwarn("MQTT command must be a JSON object")
        return

    command = payload.get("command")
    target_speed = payload.get("target_speed")

    if command not in ALLOWED_COMMANDS:
        rospy.logwarn(
            f"Unsupported robot command: {command}"
        )
        return

    # bool도 Python에서는 int의 하위 타입이므로 별도로 제외한다.
    if (
        isinstance(target_speed, bool)
        or not isinstance(target_speed, (int, float))
    ):
        rospy.logwarn(
            "target_speed must be a numeric value"
        )
        return

    target_speed = float(target_speed)

    if not math.isfinite(target_speed):
        rospy.logwarn(
            "target_speed cannot be NaN or Infinity"
        )
        return

    if not MIN_SPEED <= target_speed <= MAX_SPEED:
        rospy.logwarn(
            f"target_speed must be between "
            f"{MIN_SPEED} and {MAX_SPEED}"
        )
        return

    if command == "stop":
        target_speed = 0.0

    ros_message = RobotCommand()
    ros_message.command = command
    ros_message.target_speed = target_speed

    ros_command_publisher.publish(ros_message)

    rospy.loginfo(
        "MQTT → ROS command: "
        f"command={command}, "
        f"target_speed={target_speed:.2f}"
    )


def on_disconnect(
    client,
    userdata,
    disconnect_flags,
    reason_code,
    properties,
):
    if reason_code != 0:
        rospy.logwarn(
            f"Unexpected MQTT disconnection: {reason_code}"
        )


def shutdown() -> None:
    if mqtt_client is not None:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()


def main() -> None:
    global mqtt_client
    global ros_command_publisher

    rospy.init_node(
        "mqtt_command_to_ros",
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

    ros_command_publisher = rospy.Publisher(
        "/robot/command",
        RobotCommand,
        queue_size=10,
    )

    mqtt_client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="mqtt_command_to_ros",
    )

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
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

    rospy.on_shutdown(shutdown)

    rospy.loginfo(
        "MQTT robot/command → ROS /robot/command bridge started"
    )

    rospy.spin()


if __name__ == "__main__":
    main()
