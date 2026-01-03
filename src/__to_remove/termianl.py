import sys

print("--- Script Start ---")

# Print all arguments received
print(f"All arguments received: {sys.argv}")

# Check if there are enough arguments to access specific ones
if len(sys.argv) > 1:
    print(f"First argument (after script name): {sys.argv[1]}")
else:
    print("No additional arguments provided.")

# Example of checking for a specific argument like -settings
settings_value = "default" # Initialize with a default value
for arg in sys.argv:
    if arg.startswith("-settings="):
        # Extract the value after "-settings="
        settings_value = arg.split("=")[1]
        print(f"Found -settings argument. Value: {settings_value}")
        break # Stop searching once found
    elif arg == "-help":
        print("Help requested. Usage: python my_script.py [-settings=<value>] [-help]")

print(f"Final settings value: {settings_value}")
print("--- Script End ---")
