# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import cv2 
import numpy as np

cap = cv2.VideoCapture(0)

print(cv2.__version__)

while True:
    ret, frame = cap.read()

    frame_hsv = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2HSV)

    frame = cv2.convertScaleAbs(frame)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.convertScaleAbs(frame_gray)

    
    frame_hsv_blur = cv2.GaussianBlur(frame_hsv, (3,3), 0)
    frame_hsv_range = cv2.inRange(frame_hsv_blur, (28, 0, 0) , (255, 255, 255))
    frame_hsv_range = cv2.erode(frame_hsv_range, None, iterations= 2)
    frame_hsv_range = cv2.dilate(frame_hsv_range, None, iterations= 4)

    contours, hierarchy = cv2.findContours( frame_hsv_range.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if contours:
        contours = sorted(contours, key=cv2.contourArea, reverse= True)
        cv2.drawContours( frame, contours[0], -1, (255,0,0), 3)
        (x, y, w, h) = cv2.boundingRect(contours[0])
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,255),3)

    frame_gray_blur = cv2.GaussianBlur(frame_gray, (5, 5), 0)
    frame_gray_edged = cv2.Canny(frame_gray_blur, 10, 250)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    frame_gray_closed = cv2.morphologyEx(frame_gray_edged, cv2.MORPH_CLOSE, kernel)
    cnts, heir = cv2.findContours(frame_gray_closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    total = 0

    for c in cnts:
        frame_gray_peri = cv2.arcLength(c, True)
        frame_gray_approx = cv2.approxPolyDP(c, 0.08 * frame_gray_peri, True)
        if len(frame_gray_approx) == 4:
            cv2.drawContours(frame, [frame_gray_approx], -1, (0, 255, 0), 4)
            total += 1


    cv2.imshow("FRAME", frame)
    cv2.imshow("FRAME_GRAY", frame_gray)
    cv2.imshow("FRAME_BLUR", frame_gray_blur)
    cv2.imshow("FRAME_gray_EDGED", frame_gray_edged)
    cv2.imshow("FRAME_gray_CLOSED", frame_gray_closed)
    cv2.imshow('contours', frame) 
    print(total)





    if  cv2.waitKey(1) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()