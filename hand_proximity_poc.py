import cv2
import numpy as np
import time

CAM_ID = 0  # webcam id
FRAME_WIDTH = 640  # processing size (smaller = faster)
FRAME_HEIGHT = 360
SHOW_DEBUG_MASK = False  # set True to see segmentation mask


VRECT_NORM = (0.55, 0.25, 0.95, 0.75)  # right-side rectangle

LOW_HSV = np.array([0, 15, 60])
HIGH_HSV = np.array([25, 200, 255])

KERNEL_OPEN = (7, 7)
KERNEL_CLOSE = (11, 11)
WARNING_RATIO = 0.20  # if min_dist <= warning_threshold -> WARNING
DANGER_RATIO = 0.05   # if min_dist <= danger_threshold -> DANGER
# -----------------------------------

def norm_to_pixel(norm_rect, w, h):
    x1 = int(norm_rect[0] * w)
    y1 = int(norm_rect[1] * h)
    x2 = int(norm_rect[2] * w)
    y2 = int(norm_rect[3] * h)
    return (x1, y1, x2, y2)

def point_to_rect_distance(pt, rect):
    # rect = (x1,y1,x2,y2)
    x, y = pt
    x1, y1, x2, y2 = rect
    # if inside rect, distance to boundary is min distance to edges (can be 0)
    if x1 <= x <= x2 and y1 <= y <= y2:
        d = min(abs(x - x1), abs(x - x2), abs(y - y1), abs(y - y2))
        return d
    # if outside, compute distance to rectangle (Euclidean to closest point)
    cx = np.clip(x, x1, x2)
    cy = np.clip(y, y1, y2)
    return np.hypot(x - cx, y - cy)

def get_hand_mask(hsv):
    # skin color segmentation in HSV
    mask = cv2.inRange(hsv, LOW_HSV, HIGH_HSV)
    # morphological cleaning
    kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, KERNEL_OPEN)
    kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, KERNEL_CLOSE)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close)
    # optional blur to smooth edges
    mask = cv2.GaussianBlur(mask, (7,7), 0)
    _, mask = cv2.threshold(mask, 50, 255, cv2.THRESH_BINARY)
    return mask



def main():
    global SHOW_DEBUG_MASK
    cap = cv2.VideoCapture(CAM_ID)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not cap.isOpened():
        print("Cannot open camera")
        return

    fps_time = time.time()
    fps_count = 0
    fps = 0.0

    ret, frame = cap.read()
    if not ret:
        print("Can't read from camera")
        return
    h, w = FRAME_HEIGHT, FRAME_WIDTH
    diag = np.hypot(w, h)
    warning_thresh = WARNING_RATIO * diag
    danger_thresh = DANGER_RATIO * diag

    vrect = norm_to_pixel(VRECT_NORM, w, h)

    print("Press 'q' to quit. Press 'm' to toggle mask debug.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (w, h))
        frame_blur = cv2.GaussianBlur(frame, (5,5), 0)
        hsv = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2HSV)

        mask = get_hand_mask(hsv)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        state = "SAFE"
        min_dist = float('inf')
        hand_center = None
        hand_area = 0

        if contours:
            largest = max(contours, key=cv2.contourArea)
            hand_area = cv2.contourArea(largest)
            if hand_area > 500: 
                cv2.drawContours(frame, [largest], -1, (0,255,0), 2)
                # approximate center
                M = cv2.moments(largest)
                if M['m00'] != 0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    hand_center = (cx, cy)
                    cv2.circle(frame, hand_center, 5, (255,0,0), -1)

                pts = largest.reshape(-1, 2)
                for p in pts:
                    d = point_to_rect_distance((int(p[0]), int(p[1])), vrect)
                    if d < min_dist:
                        min_dist = d

        if min_dist == float('inf'):
            min_dist = max(w,h)

        if min_dist <= danger_thresh:
            state = "DANGER"
        elif min_dist <= warning_thresh:
            state = "WARNING"
        else:
            state = "SAFE"

        # Draw virtual rectangle
        x1,y1,x2,y2 = vrect
        if state == "SAFE":
            rect_color = (0,200,0)
        elif state == "WARNING":
            rect_color = (0,165,255)  # orange-ish
        else:
            rect_color = (0,0,255)    # red

        cv2.rectangle(frame, (x1,y1), (x2,y2), rect_color, 3)
        if hand_center is not None and hand_area>500:
            closest_pt = None
            closest_d = float('inf')
            for p in largest.reshape(-1,2):
                d = point_to_rect_distance((int(p[0]), int(p[1])), vrect)
                if d < closest_d:
                    closest_d = d
                    closest_pt = (int(p[0]), int(p[1]))
            if closest_pt is not None:
                cv2.circle(frame, closest_pt, 6, (0,255,255), -1)
                cx, cy = closest_pt
                nx = int(np.clip(cx, x1, x2))
                ny = int(np.clip(cy, y1, y2))
                cv2.line(frame, (cx,cy), (nx,ny), (200,200,200), 2, cv2.LINE_AA)

        text = f"State: {state}"
        cv2.putText(frame, text, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (255,255,255), 2, cv2.LINE_AA)
        dist_text = f"MinDist(px): {int(min_dist)}"
        cv2.putText(frame, dist_text, (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (220,220,220), 1, cv2.LINE_AA)

        # Danger overlay
        if state == "DANGER":
            # big warning
            cv2.putText(frame, "DANGER DANGER", (int(w*0.05), int(h*0.5)), cv2.FONT_HERSHEY_DUPLEX, 2.0, (0,0,255), 4, cv2.LINE_AA)
            # flashing semi-transparent overlay
            overlay = frame.copy()
            alpha = 0.4
            cv2.rectangle(overlay, (0,0), (w,h), (0,0,255), -1)
            cv2.addWeighted(overlay, alpha, frame, 1-alpha, 0, frame)

        # FPS calculation
        fps_count += 1
        if time.time() - fps_time >= 1.0:
            fps = fps_count / (time.time() - fps_time)
            fps_time = time.time()
            fps_count = 0
        cv2.putText(frame, f"FPS: {fps:.1f}", (w-140,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv2.LINE_AA)

        # Show debug mask optionally
        if SHOW_DEBUG_MASK:
            mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            combined = np.hstack((frame, cv2.resize(mask_bgr, (w, h))))
            cv2.imshow('Hand Proximity POC (frame | mask)', combined)
        else:
            cv2.imshow('Hand Proximity POC', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('m'):
            # toggle debug mask
            SHOW_DEBUG_MASK = not SHOW_DEBUG_MASK

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
