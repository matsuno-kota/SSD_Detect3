import cv2
import sys

def capture():
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    if cap.isOpened() is False:
        print("can not open camera")
        sys.exit()

    cv2.namedWindow("webcam", cv2.WINDOW_AUTOSIZE)

    while True:
        ret, frame = cap.read()
        if ret is False:
            break

        cap.release()
        cv2.destroyAllWindows()
        im_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        return im_rgb
