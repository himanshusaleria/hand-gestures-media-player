import cv2
from gesture_recognizer import GestureRecognizer
from controller import SystemController
import time

def main():
    print("Initializing Gesture Controlled Player...")
    
    # Initialize components
    recognizer = GestureRecognizer()
    controller = SystemController()
    
    # Initialize Camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("Camera started. Press 'q' to quit.")
    print("Gestures:")
    print(" - Swipe Left: Prev Song")
    print(" - Swipe Right: Next Song")
    print(" - Swipe Up: Vol Up")
    print(" - Swipe Down: Vol Down")
    print(" - Fist/Clench: Play/Pause")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Flip the frame horizontally for a later selfie-view display
        # This makes it easier for the user to coordinate swiping "left" or "right" on screen
        frame = cv2.flip(frame, 1)

        # Process frame for gestures
        # Drawing is done on the frame in-place
        detected_gesture = recognizer.process(frame)

        if detected_gesture:
            print(f"Detected: {detected_gesture}")
            
            # Visual feedback text
            cv2.putText(frame, f"ACTION: {detected_gesture}", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Execute Command
            if detected_gesture == "SWIPE_LEFT":
                controller.prev_track()
            elif detected_gesture == "SWIPE_RIGHT":
                controller.next_track()
            elif detected_gesture == "SWIPE_UP":
                controller.volume_up()
            elif detected_gesture == "SWIPE_DOWN":
                controller.volume_down()
            elif detected_gesture == "PAUSE_FIST":
                controller.play_pause()
        
        # Display the resulting frame
        cv2.imshow('Gesture Player', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
