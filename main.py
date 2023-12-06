from gpiozero import Motor, PWMOutputDevice
from pynput.keyboard import Key, Listener
import time

# Motor setup
left_motor = PWMOutputDevice(pin=19, frequency=50)   # ESC_GPIO_PIN_LEFT
right_motor = PWMOutputDevice(pin=5, frequency=50)   # ESC_GPIO_PIN_RIGHT
roller_motor = PWMOutputDevice(pin=24, frequency=50) # ESC_GPIO_PIN_ROLLER

center_pulse = 1485 / 1000  # Convert to milliseconds
pulse_diff = 50 / 1000      # Convert to milliseconds
max_pulse = 2               # Maximum pulse duration in milliseconds
min_pulse = 1               # Minimum pulse duration in milliseconds

def set_motor_speed(motor, speed):
    # Convert speed (-1 to 1) to pulse duration
    pulse_duration = center_pulse + (speed * pulse_diff)
    # Ensure pulse is within the valid range
    pulse_duration = max(min_pulse, min(max_pulse, pulse_duration))
    # Set motor speed
    motor.value = pulse_duration / 20  # Convert to duty cycle (20ms period)

def stop_motors():
    left_motor.value = 0.05 / 20 #center_pulse / 20
    right_motor.value = 0.05 / 20 #center_pulse / 20

def on_press(key):
    if key == Key.up:
        set_motor_speed(left_motor, 1)
        set_motor_speed(right_motor, 1)
        print('Up')
    elif key == Key.down:
        set_motor_speed(left_motor, -1)
        set_motor_speed(right_motor, -1)
        print('down')
    elif key == Key.left:
        set_motor_speed(left_motor, -1)
        set_motor_speed(right_motor, 1)
        print('left')
    elif key == Key.right:
        set_motor_speed(left_motor, 1)
        set_motor_speed(right_motor, -1)
        print('right')
    elif key == Key.space:  # Use space key to start/stop the roller motor
        roller_motor.value = center_pulse / 20# Forward        

def on_release(key):
    if key in [Key.up, Key.down, Key.left, Key.right]:
        stop_motors()
    elif key == Key.space:
        roller_motor.value =  0.05 / 20  # Stop roller motor
    if key == Key.esc:
        stop_motors()
        return False

# Listen for keyboard events
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()



