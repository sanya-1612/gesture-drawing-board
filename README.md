# 🖐️ AI Virtual Drawing Board using Hand Gestures

A real-time computer vision based virtual drawing system that allows users to draw, erase, and change colors using only hand gestures via webcam.

No mouse. No stylus. No touchscreen.  
Just gesture-based interaction powered by AI.

---

## 🚀 Demo Overview

This system uses MediaPipe hand tracking to detect 21 hand landmarks in real time and converts finger patterns into drawing commands on a virtual canvas.

The interaction is smooth, responsive, and completely touch-free.

---

## ✨ Gesture Controls

| Gesture | Action |
|----------|--------|
| ☝️ 1 Finger | Draw |
| ✌️ 2 Fingers | Pause / Select Color |
| 🖐️ Open Palm (5) | Erase |
| ✊ Closed Fist (0) | Clear Screen |

---

## 🎨 Features

- Real-time hand landmark detection
- Multi-color selection panel
- Smooth line rendering
- Proper stroke break handling (no unwanted reconnections)
- Dynamic eraser mode
- Full-screen canvas with maintained aspect ratio
- Low-latency processing
- Clean overlay blending on live video feed

---

## 🛠 Tech Stack

- Python
- OpenCV
- MediaPipe
- NumPy

---

## 🧠 Key Concepts Implemented

- Real-time gesture classification
- State management (Draw / Pause / Erase / Clear)
- Hand landmark processing
- Aspect ratio handling in fullscreen mode
- Canvas blending using bitwise masking
- Smooth drawing logic with previous-point tracking

---

## 📦 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/gesture-drawing-board.git
cd gesture-drawing-board
2️⃣ Install Dependencies
pip install opencv-python mediapipe numpy
▶️ Run the Project
python gesture_draw.py
Press q to exit.

🎯 Why This Project Matters
This project demonstrates practical implementation of:

Human-Computer Interaction (HCI)

Vision-based UI systems

Real-time input automation

Touchless interface design

It showcases how computer vision can replace traditional input devices in interactive systems.

🔮 Future Improvements
Thickness selector gesture

Save drawing functionality

Gesture-based undo/redo

AI-based shape smoothing

Multi-hand support

Smart classroom integration

📌 Use Cases
Smart classrooms

Interactive presentations

Touchless public systems

Accessibility tools

Creative AI interfaces

👩‍💻 Author
Sanya Singh Rathore
B.Tech CSE (AI & ML)

Exploring Computer Vision, AI Interaction Systems, and Intelligent Interfaces.

⭐ If you like this project, consider giving it a star!
