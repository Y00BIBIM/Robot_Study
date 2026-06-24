def devide(a, b):
	try:
		result = a/b
		return result
	except ZeroDivisionError:
		print("Error: Cannot divide by zero.")
		return None

print(devide(10,2))
print(devide(10,0))

print("------------------------------------------")

valid_commands = ["forward", "backward", "left", "right", "stop"]

def validate_command(command):
    try:
        if command not in valid_commands:
            raise ValueError(f"Invalid command: {command}")
        print("Valid command:", command)
    except ValueError as e:
        print("Command Error:", e)


validate_command("forward")
validate_command("jump")

