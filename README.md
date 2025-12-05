# 🖐 Hand Proximity Detection using Classical Computer Vision

> **Real-time hand tracking + virtual boundary warning (SAFE → WARNING → DANGER)**

## 📌 Project Overview

This project implements a prototype that detects the user’s hand in real-time using webcam input and determines its proximity to a virtual boundary drawn on the screen. As the hand approaches the object, the system transitions through three states:

| State | Meaning |
| :--- | :--- |
| **SAFE** | Hand is far from the boundary |
| **WARNING** | Hand is approaching / near the boundary |
| **DANGER** | Hand is extremely close or touching the boundary |

When the hand reaches the danger zone, a big alert message **"DANGER DANGER"** is displayed visually on the screen.

This implementation uses only classical Computer Vision techniques (HSV skin masking + contour extraction + distance calculation).
❗ **No MediaPipe / OpenPose / cloud-based AI is used** — strictly meets assignment requirements.

---

## 🎯 Objective

To build a real-time hand-tracking prototype that:
* Tracks the hand/fingers using webcam feed.
* Uses color segmentation + contour detection (no ML models required).
* Draws a virtual boundary (rectangle) on screen.
* Detects proximity and classifies interaction dynamically.
* Shows real-time visual feedback including DANGER alert.
* Runs ≥ 8 FPS on CPU (achieved ~15-30 FPS depending on lighting).

---

## ⚙️ Features

* ✔ Real-time webcam-based hand tracking
* ✔ Skin-masking using HSV color segmentation
* ✔ Contour-based hand detection (largest contour chosen)
* ✔ Distance computation to virtual box boundary
* ✔ Dynamic state logic (SAFE / WARNING / DANGER)
* ✔ Warning highlight overlay + flashing alert
* ✔ FPS counter overlay
* ✔ Debug mode to view binary mask (press 'm')

---

## 🧠 Working Pipeline / Approach

1.  Capture frame from camera.
2.  Convert frame → HSV color space.
3.  Apply skin color thresholding to generate binary mask.
4.  Clean noise using morphological operations.
5.  Extract biggest contour → treat it as hand area.
6.  Compute contour-to-rectangle minimum distance.
7.  Compare with distance thresholds.
8.  Classify & display state:
    * **SAFE** → Green box
    * **WARNING** → Orange box
    * **DANGER** → Red + overlay "DANGER DANGER"
9.  Render visual feedback + FPS count.

---

## 📊 System Flow Diagram

```mermaid
flowchart TD

A[Start Webcam Stream] --> B[Capture Video Frame]
B --> C[Convert to HSV]
C --> D[Apply Skin Mask\n(inRange + Morphological Filter)]
D --> E[Find Contours]
E -->|largest contour| F[Calculate Hand Position & Distance to Virtual Box]
E -->|no contour| B

F --> G{Distance < Danger Threshold?}
G -->|Yes| H[DANGER<br>Show Red Overlay + "DANGER DANGER"]
G -->|No| I{Distance < Warning Threshold?}
I -->|Yes| J[WARNING<br>Orange Boundary]
I -->|No| K[SAFE<br>Green Boundary]

H --> L[Display Output]
J --> L
K --> L
L --> B[Next Frame Loop]


```

Here is the content converted into a clean, professional README.md format.Markdown# 🖐 Hand Proximity Detection using Classical Computer Vision

> **Real-time hand tracking + virtual boundary warning (SAFE → WARNING → DANGER)**

## 📌 Project Overview

This project implements a prototype that detects the user’s hand in real-time using webcam input and determines its proximity to a virtual boundary drawn on the screen. As the hand approaches the object, the system transitions through three states:

| State | Meaning |
| :--- | :--- |
| **SAFE** | Hand is far from the boundary |
| **WARNING** | Hand is approaching / near the boundary |
| **DANGER** | Hand is extremely close or touching the boundary |

When the hand reaches the danger zone, a big alert message **"DANGER DANGER"** is displayed visually on the screen.

This implementation uses only classical Computer Vision techniques (HSV skin masking + contour extraction + distance calculation).
❗ **No MediaPipe / OpenPose / cloud-based AI is used** — strictly meets assignment requirements.

---

## 🎯 Objective

To build a real-time hand-tracking prototype that:
* Tracks the hand/fingers using webcam feed.
* Uses color segmentation + contour detection (no ML models required).
* Draws a virtual boundary (rectangle) on screen.
* Detects proximity and classifies interaction dynamically.
* Shows real-time visual feedback including DANGER alert.
* Runs ≥ 8 FPS on CPU (achieved ~15-30 FPS depending on lighting).

---

## ⚙️ Features

* ✔ Real-time webcam-based hand tracking
* ✔ Skin-masking using HSV color segmentation
* ✔ Contour-based hand detection (largest contour chosen)
* ✔ Distance computation to virtual box boundary
* ✔ Dynamic state logic (SAFE / WARNING / DANGER)
* ✔ Warning highlight overlay + flashing alert
* ✔ FPS counter overlay
* ✔ Debug mode to view binary mask (press 'm')

---

## 🧠 Working Pipeline / Approach

1.  Capture frame from camera.
2.  Convert frame → HSV color space.
3.  Apply skin color thresholding to generate binary mask.
4.  Clean noise using morphological operations.
5.  Extract biggest contour → treat it as hand area.
6.  Compute contour-to-rectangle minimum distance.
7.  Compare with distance thresholds.
8.  Classify & display state:
    * **SAFE** → Green box
    * **WARNING** → Orange box
    * **DANGER** → Red + overlay "DANGER DANGER"
9.  Render visual feedback + FPS count.

---

## 📊 System Flow Diagram

```mermaid
flowchart TD

A[Start Webcam Stream] --> B[Capture Video Frame]
B --> C[Convert to HSV]
C --> D[Apply Skin Mask\n(inRange + Morphological Filter)]
D --> E[Find Contours]
E -->|largest contour| F[Calculate Hand Position & Distance to Virtual Box]
E -->|no contour| B

F --> G{Distance < Danger Threshold?}
G -->|Yes| H[DANGER<br>Show Red Overlay + "DANGER DANGER"]
G -->|No| I{Distance < Warning Threshold?}
I -->|Yes| J[WARNING<br>Orange Boundary]
I -->|No| K[SAFE<br>Green Boundary]

H --> L[Display Output]
J --> L
K --> L
L --> B[Next Frame Loop]
```
---

##  🏁 Output Example Behavior

| Hand position         | Boundary Color | Screen Text   | Warning Overlay     |
| --------------------- | -------------- | ------------- | ------------------- |
| Far away              | 🟩 Green       | SAFE          | ❌                   |
| Getting closer        | 🟧 Orange      | WARNING       | ❌                   |
| Very close / touching | 🟥 Red         | DANGER DANGER | 🔥 Flashing overlay |


## 🛠 How to Run
1. Install dependencies
```bash
pip install opencv-python numpy
```

2. Run the script
```bash
python hand_proximity_poc.py
```


### Keyboard controls
| Key | Action                    |
| --- | ------------------------- |
| `q` | Quit program              |
| `m` | Toggle mask debug display |


**Open the script and modify:**
```
WARNING_RATIO = 0.09   # Set higher to trigger WARNING earlier

DANGER_RATIO  = 0.02   # Set higher to trigger DANGER earlier
```

**Example sensitivity profiles:**

| Use case                | WARNING_RATIO | DANGER_RATIO |
| ----------------------- | ------------- | ------------ |
| Should warn early       | `0.15`        | `0.05`       |
| Normal sensitivity      | `0.09`        | `0.02`       |
| Require hand very close | `0.05`        | `0.01`       |

---

# 📈 Performance

Runs comfortably **15–30 FPS** on CPU depending on lighting and camera resolution.

Meets requirement of **≥ 8 FPS** real-time performance.




## 🚀 Possible Improvements (Future Scope)
* Add fingertip detection using convex hull & convexity defects.

* Use background subtraction for more robust mask.

* Add shape/BLOB filtering to reduce false positives.

* Use lightweight ML model to classify hand vs non-hand.

* Extend to gesture-based interactions.

# 🏆 Conclusion

This project successfully meets the problem statement requirements by implementing a real-time classical CV based hand-tracking system with proximity-based danger alert visualization.The system is efficient, lightweight, and demonstrates dynamic interaction with virtual objects — suitable for gesture-controlled UI, AR/VR safety zones, human-computer interaction and more.