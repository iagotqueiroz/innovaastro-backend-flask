import cv2 as cv
import threading

lock = threading.Lock()

def start_cam_view():
    global lock
    cap = cv.VideoCapture(0)
    if cap.isOpened():
        rval,frame = cap.read()
    else:
        rval = False

    while rval:
        with lock:
            rvl,frame = cap.read()
            if frame is None:
                continue

            (flag, encodedImage) = cv.imencode(".jpg", frame)
            if not flag:
                continue

        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
    
    cap.release()