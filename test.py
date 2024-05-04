import RPi.GPIO as GPIO
import time
import threading
import serial

# Set up serial connection to Arduino
try:
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    time.sleep(2)  # Wait for connection to establish
except serial.SerialException:
    print("Failed to connect to Arduino on '/dev/ttyUSB0'")
    raise

# GPIO setup for linear stage
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define pin numbers
RED_PIN = 17
GREEN_PIN = 27
BLUE_PIN = 22
LMMAX_PIN = 6
LMMIN_PIN = 12
PULSE_PIN = 16
DIRECTION_PIN = 20
ENABLE_PIN = 21

# Set up GPIO pins
GPIO.setup([RED_PIN, GREEN_PIN, BLUE_PIN, PULSE_PIN, DIRECTION_PIN, ENABLE_PIN], GPIO.OUT)
GPIO.setup([LMMAX_PIN, LMMIN_PIN], GPIO.IN, pull_up_down=GPIO.PUD_UP)
def safe_serial_write(data):
    try:
        ser.write(data.encode())
        ser.flush()
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")

# Function to handle stepper motor movement for linear stage with Arduino communication
def wait_for_arduino():
    while True:
        if ser.in_waiting > 0:
            response = ser.readline().decode().strip()
            if response == "Done":
                return
            else:
                print("Arduino:", response)
def stepper_movement(direction, steps_per_second, stop_condition, command):
    GPIO.output(ENABLE_PIN, GPIO.LOW)
    GPIO.output(DIRECTION_PIN, direction)
    
    safe_serial_write(command)  # Improved command sending with error handling
    while not GPIO.input(stop_condition):
        GPIO.output(PULSE_PIN, GPIO.HIGH)
        time.sleep(1 / (2 * steps_per_second))
        GPIO.output(PULSE_PIN, GPIO.LOW)
        time.sleep(1 / (2 * steps_per_second))
    
    GPIO.output(PULSE_PIN, GPIO.LOW)
    GPIO.output(ENABLE_PIN, GPIO.HIGH)
    safe_serial_write('0')  # Send stop or status update command
    wait_for_arduino()  # Wait for Arduino to send "Done"

def round_movement(round):
    for i in round:
        # Move forward until stop condition
        time.sleep(1)
        stepper_movement(GPIO.LOW, 6400, LMMAX_PIN, '1')
        # Short delay before changing direction
        time.sleep(1)
        # Move backward until stop condition
        stepper_movement(GPIO.HIGH, 6400, LMMIN_PIN, '1')
        # Move forward until stop condition
    time.sleep(10)

# 


def routine_movement():
    while True:
        # Move forward until stop condition
        time.sleep(1)
        stepper_movement(GPIO.LOW, 6400, LMMAX_PIN, '1')
        # Short delay before changing direction
        time.sleep(1)
        # Move backward until stop condition
        stepper_movement(GPIO.HIGH, 6400, LMMIN_PIN, '1')
        # Move forward until stop condition
        
        time.sleep(10)

# Start routine movement in a separate thread
x = int(input('Insert the number of rounds you want: '))

if x == 1:
    movement_thread = threading.Thread(target=routine_movement)
else:
    movement_thread = threading.Thread(target=lambda: round_movement(range(x)))
movement_thread.start()

try:
    # Run an infinite loop to keep the script alive
    while True:
        time.sleep(1)
finally:
    GPIO.cleanup()  # Reset GPIO settings
    ser.close()  # Close serial connection
