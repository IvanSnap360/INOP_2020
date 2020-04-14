# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import cv2 
import numpy as np

cap = cv2.VideoCapture(0)
pic = cv2.imread("E:\\IVAN\\Ivan_desktop\\Kvantorium\\Competitions\\INOP_2020\\src\\CV\\CV_3\\pic.jpg")

print(cv2.__version__)

picture = cv2.convertScaleAbs(pic)
picture_gray = cv2.cvtColor(picture, cv2.COLOR_RGB2GRAY)
picture_gray = cv2.convertScaleAbs(picture_gray)

picture_gray_blur = cv2.GaussianBlur(picture_gray, (3, 3), 0)
picture_gray_edged = cv2.Canny(picture_gray_blur, 10, 250)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
picture_gray_closed = cv2.morphologyEx(picture_gray_edged, cv2.MORPH_CLOSE, kernel)
p_cnts, p_heir = cv2.findContours(picture_gray_closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
total = 0

(px,py,pw,ph)=cv2.boundingRect(p_cnts[0])# 
p_roImg=picture[py:py+ph,px:px+pw]
p_roImg=cv2.resize(p_roImg,(64,64))

for a in p_cnts:
    p_cnts = sorted(p_cnts, key=cv2.contourArea, reverse= True)
    picture_gray_peri = cv2.arcLength(a, True)
    picture_gray_approx = cv2.approxPolyDP(a, 0.08 * picture_gray_peri, True)
    if len(picture_gray_approx) == 4:
        cv2.drawContours(picture, [picture_gray_approx], -1, (0, 255, 0), 4)
        total += 1

cv2.imshow("MATRIX", p_roImg)

while True:
    ret, frame = cap.read()
    frameCopy=frame.copy()
    frame = cv2.convertScaleAbs(frame)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.convertScaleAbs(frame_gray)

    frame_gray_blur = cv2.GaussianBlur(frame_gray, (3, 3), 0)
    frame_gray_edged = cv2.Canny(frame_gray_blur, 10, 250)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    frame_gray_closed = cv2.morphologyEx(frame_gray_edged, cv2.MORPH_CLOSE, kernel)
    cnts, heir = cv2.findContours(frame_gray_closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    total = 0

    for c in cnts:
        cnts = sorted(cnts, key=cv2.contourArea, reverse= True)
        frame_gray_peri = cv2.arcLength(c, True)
        frame_gray_approx = cv2.approxPolyDP(c, 0.08 * frame_gray_peri, True)
        if len(frame_gray_approx) == 4:
            cv2.drawContours(frame, [frame_gray_approx], -1, (0, 255, 0), 4)
            total += 1
            
    (x,y,w,h)=cv2.boundingRect(cnts[0])# 
    roImg=frameCopy[y:y+h,x:x+w]
    roImg=cv2.resize(roImg,(64,64))

    cv2.imshow("FRAME", frame)
    #cv2.imshow("FRAME_GRAY", frame_gray)
    #cv2.imshow("FRAME_BLUR", frame_blur)
    cv2.imshow("FRAME_gray_EDGED", frame_gray_edged)
    #cv2.imshow("FRAME_gray_CLOSED", frame_gray_closed)
    cv2.imshow('contours', frame) 
    cv2.imshow("shape",roImg)#
    #print(total)
    for i in range(64):
        for j in range(64):
            if frame_gray_approx[i][j] == picture_gray_approx[i][j]:
                matrix_val+=1 #счётчик "похожести"
    print(matrix_val)#
    if matrix_val>2600:
            print("stop")




    if  cv2.waitKey(1) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()