import json

import paho.mqtt.client as mqtt


BROKER_HOST = "localhost"
BROKER_PORT = 1883


def on_connect(
    client,
    userdata,
    flags,
    reason_code,
    properties,
):
    print(f"Broker connected: {reason_code}")

    client.subscribe(
        "robot/#",
        qos=1,
    )


def on_message(
    client,
    userdata,
    message,
):
    payload_text = message.payload.decode("utf-8")

    print(f"Topic: {message.topic}")
    print(f"Payload: {payload_text}")

    try:
        payload_json = json.loads(payload_text)
        print(f"JSON: {payload_json}")
    except json.JSONDecodeError:
        print("Payload is not valid JSON")


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="week05_day04_client",
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(
    BROKER_HOST,
    BROKER_PORT,
    keepalive=60,
)

client.loop_start()

state_payload = {
    "robot_id": "virtual_robot_01",
    "x": 1.5,
    "y": 2.0,
    "theta": 0.75,
    "speed": 0.5,
    "battery": 95.0,
    "status": "running",
}

publish_result = client.publish(
    topic="robot/state",
    payload=json.dumps(state_payload),
    qos=1,
    retain=False,
)

publish_result.wait_for_publish()

print("MQTT message published")
print("Press Enter to stop")

input()

client.loop_stop()
client.disconnect()
