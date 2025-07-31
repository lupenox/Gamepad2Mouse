import pygame
import ctypes
from ctypes import wintypes
import time
import math
import pyautogui  # 🧠 Needed for mouse clicks

pyautogui.FAILSAFE = False

# Setup native mouse movement
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

def move_mouse_relative(dx, dy):
    current_pos = wintypes.POINT()
    user32.GetCursorPos(ctypes.byref(current_pos))
    new_x = int(current_pos.x + dx)
    new_y = int(current_pos.y + dy)
    user32.SetCursorPos(new_x, new_y)

# Configs
SENSITIVITY = 25.0
ACCEL_CURVE = 1.3
DEADZONE = 0.15
UPDATE_RATE = 1 / 60

# Init controller
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
    return math.copysign((abs(value) - DEADZONE) ** ACCEL_CURVE, value)

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    pyautogui.click(button='left')
                    print("🖱️ Left click (A button)")
                elif event.button == 1:
                    pyautogui.click(button='right')
                    print("🖱️ Right click (B button)")

        x = joystick.get_axis(0)
        y = joystick.get_axis(1)

        dx = apply_acceleration(x) * SENSITIVITY
        dy = apply_acceleration(y) * SENSITIVITY

        if dx != 0 or dy != 0:
            move_mouse_relative(dx, dy)

        time.sleep(UPDATE_RATE)

except KeyboardInterrupt:
    print("\n🛑 Controller stopped.")
