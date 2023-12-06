import RPi.GPIO as GPIO
import time

# Pin setup
ESC_GPIO_PIN = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(ESC_GPIO_PIN, GPIO.OUT)

# Initialize PWM
# The PWM frequency is typically 50Hz for ESCs.
pwm = GPIO.PWM(ESC_GPIO_PIN, 50)
pwm.start(0)

# Function to set the duty cycle for the ESC
def set_esc_speed(pulse_width_ms):
    duty_cycle = (pulse_width_ms / 20) * 100
    pwm.ChangeDutyCycle(duty_cycle)

# Set the PWM
set_esc_speed(1.25)
time.sleep(10)

# Stop the PWM
pwm.stop()

# Cleanup GPIO
GPIO.cleanup()
