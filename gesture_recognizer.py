import mediapipe as mp
import time
import math

class GestureRecognizer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # History for swipe detection
        self.centroid_history = []
        self.history_length = 10
        self.last_gesture_time = 0
        self.cooldown = 1.0  # Seconds between gestures

    def _get_centroid(self, landmarks):
        # Calculate roughly the center of the palm/hand
        x = [lm.x for lm in landmarks.landmark]
        y = [lm.y for lm in landmarks.landmark]
        return (sum(x) / len(x), sum(y) / len(y))

    def _is_fist(self, landmarks):
        # Check if fingers are curled.
        # Tips: 8 (Index), 12 (Middle), 16 (Ring), 20 (Pinky)
        # PIP joints: 6, 10, 14, 18
        # MCP joints: 5, 9, 13, 17
        
        # A simple check: if Tip is lower (higher y value) than PIP joint for all 4 fingers
        # Note: Thumb is different.
        
        tips = [8, 12, 16, 20]
        pips = [6, 10, 14, 18]
        
        curled_count = 0
        for tip, pip in zip(tips, pips):
            if landmarks.landmark[tip].y > landmarks.landmark[pip].y:
                curled_count += 1
                
        # Thumb: Tip 4, IP 3. If tip is to the right of IP (for right hand) or checking proximity
        # Simpler for fist: 4 fingers curled is usually enough or high tension check
        
        return curled_count >= 3

    def process(self, frame, draw=True):
        # Convert to RGB
        # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Assumed done by caller if needed or here
        # Actually caller usually passes BGR from opencv
        import cv2
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = self.hands.process(frame_rgb)
        
        gesture = None
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                # Cooldown check
                current_time = time.time()
                if current_time - self.last_gesture_time < self.cooldown:
                    continue

                # 1. Check for Fist (Pause)
                if self._is_fist(hand_landmarks):
                    gesture = "PAUSE_FIST"
                    self.last_gesture_time = current_time
                    self.centroid_history.clear()
                    return gesture
                
                # 2. Swipe Detection
                centroid = self._get_centroid(hand_landmarks)
                self.centroid_history.append((centroid, current_time))
                if len(self.centroid_history) > self.history_length:
                    self.centroid_history.pop(0)
                
                if len(self.centroid_history) >= 5:
                    # Check movement
                    start_pos, start_time = self.centroid_history[0]
                    end_pos, end_time = self.centroid_history[-1]
                    
                    dx = end_pos[0] - start_pos[0]
                    dy = end_pos[1] - start_pos[1]
                    dt = end_time - start_time
                    
                    if dt < 1.0 and dt > 0.1: # Reasonable swipe duration
                        # Thresholds for movement
                        SWIPE_THRESHOLD = 0.15 # 15% of screen width/height
                        
                        if abs(dx) > abs(dy): # Horizontal
                            if abs(dx) > SWIPE_THRESHOLD:
                                if dx > 0: # Left to Right (screen coordinates? No, x increases to right)
                                    # But mirror effect. Usually camera is mirrored.
                                    # If user moves hand Right (in reality), on screen it might move Right.
                                    # Let's assume standard.
                                    gesture = "SWIPE_RIGHT" # Next Song
                                else:
                                    gesture = "SWIPE_LEFT" # Prev Song
                        else: # Vertical
                            if abs(dy) > SWIPE_THRESHOLD:
                                if dy > 0: # Down (y increases downwards)
                                    gesture = "SWIPE_DOWN" # Vol Down
                                else:
                                    gesture = "SWIPE_UP" # Vol Up
                        
                        if gesture:
                            self.last_gesture_time = current_time
                            self.centroid_history.clear()
                            
        return gesture
