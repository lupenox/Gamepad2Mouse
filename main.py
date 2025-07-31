import pygame
import ctypes
from ctypes import wintypes
import time
import math

# Setup native mouse movement using ctypes
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

def move_mouse_relative(dx, dy):
    current_pos = ctypes.wintypes.POINT()
    user32.GetCursorPos(ctypes.byref(current_pos))
    new_x = int(current_pos.x + dx)
    new_y = int(current_pos.y + dy)
    user32.SetCursorPos(new_x, new_y)

# Configurable settings
SENSITIVITY = 25.0       # How fast the cursor moves
ACCEL_CURVE = 1.3        # Higher = more control at low speeds, more speed at full tilt
DEADZONE = 0.15          # Joystick drift filter
UPDATE_RATE = 1 / 60     # 60 FPS

# Init Pygame controller
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("❌ No controller detected.")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"🎮 Controller connected: {joystick.get_name()}")

def apply_acceleration(value):
    if abs(value) < DEADZONE:
        return 0
    # Curve scaling for better control
    return math.copysign((abs(value) - DEADZONE) ** ACCEL_CURVE, value)

try:
    while True:
        pygame.event.pump()

        x = joystick.get_axis(0)  # Left stick X
        y = joystick.get_axis(1)  # Left stick Y

        dx = apply_acceleration(x) * SENSITIVITY
        dy = apply_acceleration(y) * SENSITIVITY

        if dx != 0 or dy != 0:
            move_mouse_relative(dx, dy)

        time.sleep(UPDATE_RATE)

except KeyboardInterrupt:
    print("\n🛑 Controller stopped.")
