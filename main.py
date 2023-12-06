import pygame
from pigpio
import time

# Initialize Pygame and Joystick
pygame.init()
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    raise IOError("No joystick detected")
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Pin setup
ESC_GPIO_PIN_ROLLER = 24  # Change to a hardware PWM pin
ESC_GPIO_PIN_LEFT = 19    # Change to a hardware PWM pin
ESC_GPIO_PIN_RIGHT = 5   # Change to a hardware PWM pin
VIRTUAL_GND_PIN = 13       # Pin for virtual GND

# Function to set the duty cycle for the ESC
def set_esc_speed(gpio_pin, pulse_width_us):
    pi.set_servo_pulsewidth(gpio_pin, pulse_width_us)

def update_motors(left_speed, right_speed):
    set_esc_speed(ESC_GPIO_PIN_LEFT, left_speed)
    set_esc_speed(ESC_GPIO_PIN_RIGHT, right_speed)
    time.sleep(0.02)

# Initialize pigpio
pi = pigpio.pi(port=8880)

# Set the virtual ground pin to LOW
pi.set_mode(VIRTUAL_GND_PIN, pigpio.OUTPUT)
pi.write(VIRTUAL_GND_PIN, 0)
center = 1485
diff = 50

# Set the PWM - arming
set_esc_speed(ESC_GPIO_PIN_ROLLER, 1000)  # 1.0ms pulse
set_esc_speed(ESC_GPIO_PIN_LEFT, 1500)    # 1.5ms pulse
set_esc_speed(ESC_GPIO_PIN_RIGHT, 1500)   # 1.5ms pulse
print("Arming!")
time.sleep(2)

try:
    running = True
    while running:
        pygame.event.pump()  # Process event queue

        # Assuming axis 0 for forward/backward, axis 1 for left/right
        forward_backward = -joystick.get_axis(0)  # Invert if needed
        left_right = joystick.get_axis(1)

        left_speed = forward_backward + left_right
        right_speed = forward_backward - left_right

        # Limit speed values to range -1 to 1
        left_speed = center + max(-1, min(1, left_speed))*diff
        right_speed = center + max(-1, min(1, right_speed))*diff

        update_motors(left_speed, right_speed)

        # Add your roller motor control here (e.g., based on a joystick button)

        time.sleep(0.1)  # Adjust as needed

except KeyboardInterrupt:
    pass

finally:
    # Ensure the motors are stopped when the script exits
    # Stop the PWM for each pin
    set_esc_speed(ESC_GPIO_PIN_ROLLER, 0)
    set_esc_speed(ESC_GPIO_PIN_LEFT, 0)
    set_esc_speed(ESC_GPIO_PIN_RIGHT, 0)
    pi.stop()
    pygame.quit()
