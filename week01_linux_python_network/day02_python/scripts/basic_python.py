robot_name = "mobile_robot_01"
battery = 87.5
is_moving = False
position_x = 1.2
position_y = 3.4

print("Robot Name : ", robot_name)
print("Battery : ", battery)
print("Is Moving  : ", is_moving)
print("Position : ", position_x, position_y)

print(type(robot_name))
print(type(battery))
print(type(is_moving))
print(type(position_x))

print("--------------------------------------------")

sensor_values = [23.5, 24.1, 23.8, 24.0]
commands = ["forward", "left", "right", "stop"]

print("Sensor Values : ", sensor_values)
print("First Sensor : ", sensor_values[0])
print("Last Command : ", commands[-1])

sensor_values.append(25.2)
commands.append("backward")

print("Updated Sensor Vales : ", sensor_values)
print("Updated Commands : ", commands)

print("--------------------------------------------")

robot_state = {
	"name": robot_name,
	"battery": battery,
	"is_moving": False,
	"position": {
		"x": 1.2,
		"y": 3.4,
	}
}

print("Robot State: ", robot_state)
print("Robot Battery : ", robot_state["battery"])
print("Robot X Position : ", robot_state["position"]["x"])

robot_state["battery"] = 86.0
robot_state["is_moving"] = True

print("Updated Robot State : ", robot_state)

