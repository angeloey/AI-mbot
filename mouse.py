import time
import win32api, win32con
import math

class MouseThread:
    def __init__(self):
    #sens_mod = 8182 #180deg = this many pixels
        self.dpi = 800
        self.sense = 32
        self.fov_x = 95
        self.fov_y = 64

        self.min_speed_multiplier = 1
        self.max_speed_multiplier = 15
        self.max_distance = 320

    def leftClick(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        time.sleep(.8)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        print('Left Click')

    def rightClick(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
        time.sleep(.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
        print('Right Click')
        
    def moveMouse(self, x, y):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)
        
    def calculateOffset(self, target_x, target_y):
        if target_x <= 160:
            offset_x = -(160 - target_x)
        else:
            offset_x = (target_x - 160)
            
        if target_y <= 160:
            offset_y = -(160 - target_y)
        else:
            offset_y = (target_y - 160)
            
        distance = math.sqrt(offset_x**2 + offset_y**2)   
        speed_multiplier = self.calculate_speed_multiplier(distance)
            
        degrees_per_pixel_x = self.fov_x / 1920
        degrees_per_pixel_y = self.fov_y / 1080
        
        mouse_move_x = offset_x * degrees_per_pixel_x
        move_x = (mouse_move_x / 360) * (self.dpi * (1 / self.sense)) * speed_multiplier

        mouse_move_y = offset_y * degrees_per_pixel_y
        move_y = (mouse_move_y / 360) * (self.dpi * (1 / self.sense)) * speed_multiplier
        
        self.moveMouse(int(offset_x), int(offset_y))
        #if abs(offset_x) < 10 and abs(offset_y) < 10:
        #    self.leftClick()

    def calculate_speed_multiplier(self, distance):
            normalized_distance = min(distance / self.max_distance, 1)
            speed_multiplier = self.min_speed_multiplier + (self.max_speed_multiplier - self.min_speed_multiplier) * (1 - normalized_distance)
            
            return speed_multiplier
        
mouse = MouseThread()
