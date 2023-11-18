import cv2
import numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="path to the image file")
args = vars(ap.parse_args())


if args["image"]:
    img = cv2.imread(args["image"])
else:
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()


while True:
    if not args["image"]:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
    else:
        frame = img.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 20)


    left = [0, 0]
    right = [0, 0]
    up = [0, 0]
    down = [0, 0]

    if lines is not None:  
        for obj in lines:
            theta = obj[0][1]
            rho = obj[0][0]

         
            if 1.0 <= np.round(theta, 2) <= 1.1 or 2.0 <= np.round(theta, 2) <= 2.1:
                if 20 <= rho <= 30:
                    left[0] += 1
                elif 60 <= rho <= 65:
                    left[1] += 1
                elif -73 <= rho <= -57:
                    right[0] += 1
                elif 148 <= rho <= 176:
                    right[1] += 1

          
            elif 0.4 <= np.round(theta, 2) <= 0.6 or 2.6 <= np.round(theta, 2) <= 2.7:
                if -63 <= rho <= -15:
                    up[0] += 1
                elif 67 <= rho <= 74:
                    down[1] += 1
                    up[1] += 1
                elif 160 <= rho <= 171:
                    down[0] += 1


    if left[0] >= 1 and left[1] >= 1:
        direction = "left"
    elif right[0] >= 1 and right[1] >= 1:
        direction = "right"
    elif up[0] >= 1 and up[1] >= 1:
        direction = "up"
    elif down[0] >= 1 and down[1] >= 1:
        direction = "down"
    else:
        direction = "no arrow detected"


    print(direction)
    print("Up:", up, "Down:", down, "Left:", left, "Right:", right)


    cv2.imshow("Arrow Detection", frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


if not args["image"]:
    cap.release()
else:
    cv2.destroyAllWindows()

