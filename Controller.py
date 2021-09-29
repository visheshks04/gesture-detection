from HandsDetector import HandsDetector
import sys
import os
import time
import cv2

class Controller:

    def __init__(self):
        self.detector = HandsDetector()
        self.volume_lock_switch = False

    def set_volume(self, distance, distance_at_min_volume=25, distance_at_max_volume=270):
        
        volume_status = distance/(distance_at_max_volume - distance_at_min_volume) * 100 # Calculated Volume distance
        if volume_status>100: # make sure the volume percentage never exceeds 100 and goes below 0
            volume_status = 100
        if volume_status<0:
            volume_status = 0
        
        if self.volume_lock_switch:
            if sys.platform == 'linux2' or sys.platform == 'linux':
                os.system(f"amixer -D pulse sset Master {volume_status}%")
            elif sys.platform == 'win32':
                os.system(f'nircmd.exe setsysvolume {volume_status/100 * 65535}')

    def volume_lock(self, distance, threshold=40):
        if distance<threshold:
            self.volume_lock_switch = not self.volume_lock_switch # NEEDS FIXING

if __name__ == '__main__':

    controller = Controller()
    
    while True:

        previous_time = time.time()
        img, hands = controller.detector.detect()
        img = controller.detector.draw(img, hands)
        if hands:
            for hand in hands:
                distance = controller.detector.get_distance(hand, 4, 8)
                print(f"Distance: {distance}")
                cv2.putText(img, f'Distance: {distance}', (10,60), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 2)
                controller.set_volume(distance)

        current_time = time.time()
        fps = 1/(current_time-previous_time)
        cv2.putText(img, f'FPS: {fps}', (10,90), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 2)
        cv2.imshow('Video', img)
        cv2.waitKey(1)