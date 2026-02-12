import cv2
import numpy as np
import mediapipe as mp

# ---------------- INITIALIZE ----------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Set camera resolution (reduces stretching)
cap.set(3, 1280)
cap.set(4, 720)

canvas = None
prev_x, prev_y = None, None

draw_color = (255, 0, 0)
draw_thickness = 4
eraser_thickness = 50

# Extended colors (BGR)
colors = [
    (255, 0, 0),      # Blue
    (0, 255, 0),      # Green
    (0, 0, 255),      # Red
    (0, 255, 255),    # Yellow
    (255, 0, 255),    # Pink
    (255, 255, 255),  # White
    (42, 42, 165),    # Brown
    (0, 165, 255),    # Orange
    (128, 0, 128),    # Purple
    (0, 0, 0)         # Black
]

def count_fingers(hand_landmarks):
    fingers = []

    # Thumb
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    tips = [8, 12, 16, 20]
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

# Fullscreen window
cv2.namedWindow("Gesture Drawing", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Gesture Drawing",
                      cv2.WND_PROP_FULLSCREEN,
                      cv2.WINDOW_FULLSCREEN)

# ---------------- MAIN LOOP ----------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # Maintain aspect ratio (no stretch)
    screen_w = 1280
    screen_h = 720

    h, w = frame.shape[:2]
    scale = min(screen_w / w, screen_h / h)
    new_w = int(w * scale)
    new_h = int(h * scale)

    frame = cv2.resize(frame, (new_w, new_h))

    if canvas is None:
        canvas = np.zeros_like(frame)

    # Draw color palette
    box_width = new_w // len(colors)
    color_boxes = []

    for i, color in enumerate(colors):
        x1 = i * box_width
        y1 = 0
        x2 = x1 + box_width
        y2 = 80
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)
        color_boxes.append((x1, y1, x2, y2, color))

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    mode = "PAUSE"

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks,
                                   mp_hands.HAND_CONNECTIONS)

            finger_count = count_fingers(hand_landmarks)

            x = int(hand_landmarks.landmark[8].x * new_w)
            y = int(hand_landmarks.landmark[8].y * new_h)

            # -------- COLOR SELECT --------
            if finger_count == 2 and y < 80:
                mode = "SELECT COLOR"
                prev_x, prev_y = None, None

                for (x1, y1, x2, y2, color) in color_boxes:
                    if x1 < x < x2:
                        draw_color = color

            # -------- DRAW --------
            elif finger_count == 1:
                mode = "DRAW"

                if prev_x is None:
                    prev_x, prev_y = x, y

                cv2.line(canvas, (prev_x, prev_y),
                         (x, y), draw_color, draw_thickness)
                prev_x, prev_y = x, y

            # -------- PAUSE --------
            elif finger_count == 2:
                mode = "PAUSE"
                prev_x, prev_y = None, None

            # -------- ERASER --------
            elif finger_count == 5:
                mode = "ERASER"

                if prev_x is None:
                    prev_x, prev_y = x, y

                cv2.line(canvas, (prev_x, prev_y),
                         (x, y), (0, 0, 0), eraser_thickness)
                prev_x, prev_y = x, y

            # -------- CLEAR --------
            elif finger_count == 0:
                mode = "CLEAR"
                canvas = np.zeros_like(frame)
                prev_x, prev_y = None, None

            else:
                prev_x, prev_y = None, None

    else:
        prev_x, prev_y = None, None

    # Merge canvas and frame
    gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_canvas, 20, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
    canvas_fg = cv2.bitwise_and(canvas, canvas, mask=mask)

    final = cv2.add(frame_bg, canvas_fg)

    cv2.putText(final, f"Mode: {mode}", (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Gesture Drawing", final)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

 # python air_draw.py