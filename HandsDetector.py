import cv2
import mediapipe as mp
import time
import numpy as np

class HandsDetector:

    def __init__(self, max_num_hands=1, min_detection_confidence=0.75, device_index=0, cam_width=1280, cam_height=800):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=max_num_hands, min_detection_confidence=min_detection_confidence)
        self.mp_draw = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(device_index)
        # Try fixing the cam width and cam height
        self.cap.set(3, cam_width)
        self.cap.set(4, cam_height)

    def detect(self):
        success, img = self.cap.read()
        self.shape = img.shape
        assert success, 'Could not capture the image correctly'
        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = self.hands.process(img_RGB)

        return img, results.multi_hand_landmarks

    def draw(self, img, hands, connections=True):

        if hands:
            for hand in hands: 
                if connections:
                    self.mp_draw.draw_landmarks(img, hand, self.mp_hands.HAND_CONNECTIONS)
                else:
                    self.mp_draw.draw_landmarks(img, hand)

        return img

    def get_distance(self, hand, l1_index, l2_index):
        h, w, _ = self.shape

        l1 = hand.landmark[l1_index]
        l2 = hand.landmark[l2_index]

        l1x = l1.x * w
        l2x = l2.x * w

        l1y = l1.y * h
        l2y = l2.y * h

        distance = abs(l1x - l2x), abs(l1y - l2y)

        euclidean = np.sqrt(distance[0]**2 + distance[1]**2)
        return euclidean




if __name__ == '__main__':

    detector = HandsDetector()
    

    while True:

        previous_time = time.time()
        img, hands = detector.detect()
        img = detector.draw(img, hands)
        if hands:
            for hand in hands:
                distance = detector.get_distance(hand, 4, 20)
                print(f"Distance: {distance}")
                cv2.putText(img, f'Distance: {distance}', (10,60), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 2)

        current_time = time.time()
        fps = 1/(current_time-previous_time)
        cv2.putText(img, f'FPS: {fps}', (10,90), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 2)
        cv2.imshow('Video', img)
        cv2.waitKey(1)
