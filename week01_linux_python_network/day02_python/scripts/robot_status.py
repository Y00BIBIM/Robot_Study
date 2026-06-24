battery = 35
status = "idle"

if battery >= 80:
    print("Battery status: High")
elif battery >= 40:
    print("Battery status: Medium")
else:
    print("Battery status: Low")

if status == "moving":
    print("Robot is moving.")
elif status == "idle":
    print("Robot is waiting.")
elif status == "error":
    print("Robot has an error.")
else:
    print("Unknown status.")

print("---------------------------------------------------")

commands = ["forward", "backward", "left", "stop"]

for command in commands:
    print("Execute command:", command)

sensor_values = [23.5, 24.1, 25.0, 24.8]

total = 0
for value in sensor_values:
    total += value

average = total / len(sensor_values)
print("Average sensor value:", average)

count = 3
while count > 0:
    print("Countdown:", count)
    count -= 1

print("Robot start!")

print("----------------------------------------------")

def get_battery_level(battery):
	if battery >= 80:
		return "High"
	elif battery >= 40:
		return "Medium"
	else:
		return "Low"

def create_robot_state(name, battery, x, y, status):
	return {
		"name": name,
		"battery": battery,
		"position": {
			"x": x,
			"y": y
		},
		"status": status
	}

level = get_battery_level(76)
print("Battery Level:", level)

state = create_robot_state("mobile_robot_01", 76, 1.0, 2.0, "idle")
print("Created State:", state)

