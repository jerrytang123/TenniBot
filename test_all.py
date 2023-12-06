import pigpio
import time

# Pin setup
ESC_GPIO_PIN_ROLLER = 24  # Change to a hardware PWM pin
ESC_GPIO_PIN_LEFT = 19    # Change to a hardware PWM pin
ESC_GPIO_PIN_RIGHT = 5   # Change to a hardware PWM pin
VIRTUAL_GND_PIN = 13       # Pin for virtual GND

# Initialize pigpio
pi = pigpio.pi(port=8880)

# Function to set the duty cycle for the ESC
def set_esc_speed(gpio_pin, pulse_width_us):
    pi.set_servo_pulsewidth(gpio_pin, pulse_width_us)

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
time.sleep(5)

# Uncomment to send command
set_esc_speed(ESC_GPIO_PIN_ROLLER, 1400)  # 1.25ms pulse
set_esc_speed(ESC_GPIO_PIN_LEFT, center - diff)    # 1.4ms pulse
set_esc_speed(ESC_GPIO_PIN_RIGHT, center + diff)   # 1.4ms pulse
print("Commanding!")
time.sleep(5)

# Stop the PWM for each pin
set_esc_speed(ESC_GPIO_PIN_ROLLER, 0)
set_esc_speed(ESC_GPIO_PIN_LEFT, 0)
set_esc_speed(ESC_GPIO_PIN_RIGHT, 0)

# Cleanup
pi.stop()
