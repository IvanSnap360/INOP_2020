import cv2
import numpy as np

red_min = np.array((0, 216, 58), np.uint8)
red_max = np.array((255, 255, 188), np.uint8)

blue_min = np.array((114, 172, 69), np.uint8)
blue_max = np.array((130, 255, 166), np.uint8)

yellow_min = np.array((0, 127, 174), np.uint8)
yellow_max = np.array((255, 255, 255), np.uint8)

green_min = np.array((47, 104, 104), np.uint8)
green_max = np.array((81, 186, 255), np.uint8)

black_min = np.array((0, 86, 0), np.uint8)
black_max = np.array((255, 90, 26), np.uint8)

white_min = np.array((0, 0, 175), np.uint8)
white_max = np.array((21, 255, 255), np.uint8)

cells_min = np.array((0,0,0), np.uint8)
cells_max = np.array((255, 255, 42), np.uint8)

size_for_resize = (320, 320)
blur_setting = (7, 7)

circle_sdvir = 100
circle_radius = 20
circle_thin = 2
circle_color = (255,0,255)

find_rectangle_line_color = (255, 255,0)
find_rectangle_line_thin = 2
cap = cv2.VideoCapture(0)

imshow_ar = []
global roImg
# def find_matrix(frame):
#     frameCopy = frame.copy()
#     blur = cv2.blur(frame, blur_setting, 0)
#     hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
#     thresh = cv2.inRange(hsv, cells_min, cells_max)
#     conts, heir = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     if conts:
#         conts = sorted(conts, key=cv2.contourArea, reverse=True)
#         (x,y,w,h) = cv2.boundingRect(conts[0])
#         cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 255), 3)
#         cv2.drawContours(frame, conts, -1, (0, 0, 255), 3)
#         M = cv2.moments(thresh)
        

        
        
#         roImg = frameCopy[y:y+h, x:x+w]
#         roImg = cv2.resize(roImg, size_for_resize)

#         cx = 32#int(M["m10"] / M["m00"])
#         cy = 32#int(M["m01"] / M["m00"])
      
#         cv2.circle(roImg, (cx,cy), circle_radius, circle_color, circle_thin)

#         cv2.circle(roImg, (cx, cy+circle_sdvir), circle_radius, circle_color, circle_thin)
#         cv2.circle(roImg, (cx, cy-circle_sdvir), circle_radius, circle_color, circle_thin)

#         cv2.circle(roImg, (cx+circle_sdvir, cy), circle_radius, circle_color, circle_thin)
#         cv2.circle(roImg, (cx-circle_sdvir, cy), circle_radius, circle_color, circle_thin)

#         cv2.circle(roImg, (cx+circle_sdvir, cy+circle_sdvir), circle_radius, circle_color, circle_thin)
#         cv2.circle(roImg, (cx-circle_sdvir, cy-circle_sdvir), circle_radius, circle_color, circle_thin)
#         cv2.circle(roImg, (cx+circle_sdvir, cy-circle_sdvir), circle_radius, circle_color, circle_thin)
#         cv2.circle(roImg, (cx-circle_sdvir, cy+circle_sdvir), circle_radius, circle_color, circle_thin)
#     #cv2.imshow("roImg", roImg)
#     cv2.imshow("frame", frame)


def find_color(cadr, color_min, color_max):
    cadr2 = cadr.copy()
    blur = cv2.blur(cadr2, blur_setting, 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv, color_min, color_max)
    conts, heir = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE,)
    
    if conts:
        conts = sorted(conts, key=cv2.contourArea, reverse=True)
        (x,y,w,h) = cv2.boundingRect(conts[0])
        cv2.rectangle(cadr2, (x,y), (x+w, y+h), find_rectangle_line_color, find_rectangle_line_thin)
        #cv2.drawContours(cadr, conts,-1,(0,0,255),3)
    return cadr2


ret, frame = cap.read()
imshow_ar = [find_color(frame, red_min, red_max),find_color(frame, blue_min, blue_max),find_color(frame, green_min, green_max), find_color(frame, yellow_min, yellow_max), find_color(frame, black_min, black_max)]
imshow_ar_names = ["RED","BLUE","GREEN","YELLOW","BLACK"]
i=0
while True:
    ret, frame = cap.read()
    frameCopy = frame.copy()
    blur = cv2.blur(frame, blur_setting, 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv, cells_min, cells_max)
    conts, heir = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if conts:
        conts = sorted(conts, key=cv2.contourArea, reverse=True)
        cv2.drawContours(frame, conts, 0, (0, 0, 255), 3)
        (x,y,w,h) = cv2.boundingRect(conts[0])
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 255), 3)
        
        M = cv2.moments(thresh)

        cx = int(size_for_resize[0] / 2) #int(M["m10"] / M["m00"])
        cy = int(size_for_resize[1] / 2) #int(M["m01"] / M["m00"])
        
        roImg = frameCopy[y:y+h, x:x+w]
        roImg = cv2.resize(roImg, size_for_resize)

        

        cv2.circle(roImg, (cx,cy), circle_radius, circle_color, circle_thin)

        cv2.circle(roImg, (cx, cy+circle_sdvir), circle_radius, circle_color, circle_thin)
        cv2.circle(roImg, (cx, cy-circle_sdvir), circle_radius, circle_color, circle_thin)

        cv2.circle(roImg, (cx+circle_sdvir, cy), circle_radius, circle_color, circle_thin)
        cv2.circle(roImg, (cx-circle_sdvir, cy), circle_radius, circle_color, circle_thin)

        cv2.circle(roImg, (cx+circle_sdvir, cy+circle_sdvir), circle_radius, circle_color, circle_thin)
        cv2.circle(roImg, (cx-circle_sdvir, cy-circle_sdvir), circle_radius, circle_color, circle_thin)
        cv2.circle(roImg, (cx+circle_sdvir, cy-circle_sdvir), circle_radius, circle_color, circle_thin)
        cv2.circle(roImg, (cx-circle_sdvir, cy+circle_sdvir), circle_radius, circle_color, circle_thin)

    cv2.imshow("roImg", roImg)
    cv2.imshow("frame", frame)

    cv2.imshow("RED",find_color(roImg, red_min, red_max))

    cv2.imshow("BLUE",find_color(roImg, blue_min, blue_max))

    cv2.imshow("GREEN",find_color(roImg, green_min, green_max))

    cv2.imshow("YELLOW", find_color(roImg, yellow_min, yellow_max))

    cv2.imshow("BLACK", find_color(roImg, black_min, black_max))

    cv2.imshow("WHITE", find_color(roImg, white_min, white_max))

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

