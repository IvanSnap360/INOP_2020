#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2 
import numpy as np 
import rospy 
from std_msgs.msg import Int16
import os

color_0_0 = rospy.Publisher("robot/plan/0_0", Int16,queue_size=10)
color_1_0 = rospy.Publisher("robot/plan/1_0", Int16,queue_size=10)
color_2_0 = rospy.Publisher("robot/plan/2_0", Int16,queue_size=10)

color_0_1 = rospy.Publisher("robot/plan/0_1", Int16,queue_size=10)
color_1_1 = rospy.Publisher("robot/plan/1_1", Int16,queue_size=10)
color_2_1 = rospy.Publisher("robot/plan/2_1", Int16,queue_size=10)

color_0_2 = rospy.Publisher("robot/plan/0_2", Int16,queue_size=10)
color_1_2 = rospy.Publisher("robot/plan/1_2", Int16,queue_size=10)
color_2_2 = rospy.Publisher("robot/plan/2_2", Int16,queue_size=10)

rospy.init_node("plan", anonymous=True)


red_min = np.array((0, 216, 58), np.uint8)
red_max = np.array((255, 255, 188), np.uint8)

blue_min = np.array((114, 172, 69), np.uint8)
blue_max = np.array((130, 255, 166), np.uint8)

yellow_min = np.array((0, 127, 174), np.uint8)
yellow_max = np.array((255, 255, 255), np.uint8)

green_min = np.array((47, 104, 104), np.uint8)
green_max = np.array((81, 186, 255), np.uint8)

black_min = np.array((0, 0, 0), np.uint8)
black_max = np.array((255, 255, 28), np.uint8)

white_min = np.array((0, 0, 178), np.uint8)
white_max = np.array((88, 51, 229), np.uint8)

cells_min = np.array((0,0,0), np.uint8)
cells_max = np.array((255, 255, 42), np.uint8)

size_for_resize = (240, 240)

point_sdvig = 20

#blur_setting = (10,10)
blur_setting = (7,7)

circle_sdvir = 100
circle_radius = 20
circle_thin = 2
circle_color = (255,0,255)

find_rectangle_line_color = (255, 255,0)
find_rectangle_line_thin = 2

cap = cv2.VideoCapture(0)

plan = [[0,0,0],[0,0,0],[0,0,0]]


def find_color(cadr, color_min, color_max):
    x = 0
    y = 0
    w = 0
    h = 0
    
    cadr2 = cadr.copy()
    blur = cv2.blur(cadr2, blur_setting, 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv, color_min, color_max)
    _,  contos, heir = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE,)
    color = "" 
    if contos:
        contos = sorted(contos, key=cv2.contourArea, reverse=True)
        (x,y,w,h) = cv2.boundingRect(contos[0])
        cv2.rectangle(cadr2, (x + point_sdvig ,y + point_sdvig), (x+w-point_sdvig, y+h-point_sdvig), find_rectangle_line_color, find_rectangle_line_thin)
        #cv2.drawContours(cadr, conts,-1,(0,0,255),3)
      
    if ((color_min == red_min).any() and (color_max == red_max)).all():
       color = 5#"RED"
    elif (color_min == blue_min).all() and (color_max == blue_max).all():
        color = 2#"BLUE"
    elif (color_min == green_min).all() and (color_max == green_max).all():
        color = 3#"GREEN"
    elif (color_min == yellow_min).all() and (color_max == yellow_max).all():
        color = 4#"YELLOW"
    elif (color_min == black_min).all() and (color_max == black_max).all():
        color = 1#"BLACK"
    else:
        color = 0#"WHITE"
        
    return cadr2, x + point_sdvig, y + point_sdvig, x+w-point_sdvig, y+h-point_sdvig, color    




def detect():
    for attemps in range(300):
        ret, frame = cap.read()
        frameCopy = frame.copy()
        blur = cv2.blur(frame, blur_setting, 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(hsv, cells_min, cells_max)
        _, conts, heir = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if conts:
            conts = sorted(conts, key=cv2.contourArea, reverse=True)
            cv2.drawContours(frame, conts, 0, (0, 0, 255), 3)
            (fx,fy,fw,fh) = cv2.boundingRect(conts[0])
            cv2.rectangle(frame, (fx,fy), (fx+fw, fy+fh), (255, 0, 255), 3)
            
            M = cv2.moments(thresh)

            cx = int(size_for_resize[0] / 2) #int(M["m10"] / M["m00"])
            cy = int(size_for_resize[1] / 2) #int(M["m01"] / M["m00"])
            
            roImg = frameCopy[fy:fy+fh, fx:fx+fw]
            roImg = cv2.resize(roImg, size_for_resize)

            cv2.circle(roImg, (cx,cy), circle_radius, circle_color, circle_thin)
            for cxi in range(0,320,80):
                for cyj in range(0,320,80):
                    cv2.circle(roImg, (cxi,cyj), circle_radius, circle_color, circle_thin)
                    

        red_frame, red_x1, red_y1, red_x2, red_y2, red_color = find_color(roImg, red_min, red_max)
        blue_frame, blue_x1, blue_y1, blue_x2, blue_y2, blue_color = find_color(roImg, blue_min, blue_max)
        green_frame, green_x1, green_y1, green_x2, green_y2, green_color = find_color(roImg, green_min, green_max)
        yellow_frame, yellow_x1, yellow_y1, yellow_x2, yellow_y2, yellow_color = find_color(roImg, yellow_min, yellow_max)
        black_frame, black_x1, black_y1, black_x2, black_y2, black_color = find_color(roImg, black_min, black_max)
        white_frame, white_x1, white_y1, white_x2, white_y2, white_color = find_color(roImg, white_min, white_max)

        x1_point = [red_x1, blue_x1, green_x1, yellow_x1, black_x1, white_x1]
        y1_point = [red_y1, blue_y1, green_y1, yellow_y1, black_y1, white_y1] 
        x2_point = [red_x2, blue_x2, green_x2, yellow_x2, black_x2, white_x2] 
        y2_point = [red_y2, blue_y2, green_y2, yellow_y2, black_y2, white_y2] 
        color = [red_color, blue_color, green_color, yellow_color, black_color, white_color]

        for i in range(0,240,80):
            for j in range(0,240,80):
                cv2.rectangle(roImg, (i,j), (i+80, j+80), circle_color, circle_thin)
                for a in range(6):
                    if (x1_point[a] > i) and (x2_point[a] < (i+80)) and (y1_point[a] > j) and (y2_point[a]  < (j+80)):
                        aj=int(i/80)
                        ai=int(j/80)
                        plan[ai][aj] = color[a]


        # for io in range (0,3,1):
        #     for jo in range(0,3,1):
        #         print
        print(plan)

    #    cv2.imshow("RED",red_frame)
    #    cv2.imshow("BLUE",blue_frame)
    #    cv2.imshow("GREEN",green_frame)
    #    cv2.imshow("YELLOW",yellow_frame)
    #   cv2.imshow("BLACK",black_frame)
    #    cv2.imshow("WHITE",white_frame)

    #    cv2.imshow("roImg", roImg)
        cv2.imshow("FRAME", frame)

        # if cv2.waitKey(1) == ord('q'):
        #     break
    color_0_0.publish(plan[0][0])
    color_1_0.publish(plan[1][0])
    color_2_0.publish(plan[2][0])

    color_0_1.publish(plan[0][1])
    color_1_1.publish(plan[1][1])
    color_2_1.publish(plan[2][1])

    color_0_2.publish(plan[0][2])
    color_1_2.publish(plan[1][2])
    color_2_2.publish(plan[2][2])
    
    
    
detect()



rospy.spin()

cap.release()
cv2.destroyAllWindows()    


