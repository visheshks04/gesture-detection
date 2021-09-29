from Controller import Controller
import time
import cv2

controller = Controller()

while True:

    previous_time = time.time()
    img, hands = controller.detector.detect()
    img = controller.detector.draw(img, hands)
    if hands:
        for hand in hands:
            volume_distance = controller.detector.get_distance(hand, 4, 8)
            lock_distance = controller.detector.get_distance(hand, 12, 2)
            print(f"Volume Distance: {volume_distance}")
            print(f'Lock Distance: {lock_distance}')
            cv2.putText(img, f"Volume Distance: {volume_distance}", (10,60), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 2)
            cv2.putText(img, f'Lock Distance: {lock_distance}', (10,30), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 2)
            controller.set_volume(volume_distance)
            controller.volume_lock(lock_distance)

    current_time = time.time()
    fps = 1/(current_time-previous_time)
    cv2.putText(img, f'FPS: {fps}', (10,90), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 2)
    cv2.imshow('Video', img)
    cv2.waitKey(1)