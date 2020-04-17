import cv2
import numpy as np
import sys 



cap = cv2.VideoCapture(0)

cells_min = np.array((0,0,165), np.uint8)
cells_max = np.array((255, 88, 188), np.uint8)
size_for_resize = (64,64)


plan=cv2.imread("E:\\IVAN\\Ivan_desktop\\Kvantorium\\Competitions\\INOP_2020\\src\\CV\\CV_4\\pic.jpg")
plan=cv2.resize(plan,size_for_resize)
plan = cv2.blur(plan, (2,2), 0)
plan=cv2.cvtColor(plan, cv2.COLOR_BGR2HSV)
plan = cv2.inRange(plan, cells_min, cells_max)
cv2.imshow("plan", plan)




while True:
    ret, frame = cap.read()
    frame2 = frame.copy()
    frame = cv2.convertScaleAbs(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow("frame2", frame)
    frame = cv2.blur(frame, (2, 2), 0)
    frame = cv2.inRange(frame, cells_min, cells_max)
    cv2.imshow("frame", frame)
    frame = cv2.erode(frame, None, iterations= 2)
    frame = cv2.dilate(frame, None, iterations= 4)
    contrours, heir = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contrours:
        contrours = sorted(contrours, key=cv2.contourArea, reverse=True)
        (x,y,w,h) = cv2.boundingRect(contrours[0])
        #cv2.drawContours(frame2,contrours,-1,(0,0,255),3) 

        cv2.rectangle(frame2, (x,y), (x+w, y+h), (0,255,0), 3)
        #cv2.circle(roImg, ((x+w)%2, (y+h)%2), 20, (0,0,200))
        roImg = frame2[y:y+h,x:x+w]
        roImg = cv2.resize(frame, size_for_resize)
        
        counter = 0
        for i in range(64):
            for j in range(64):
                if roImg[i][j] == plan[i][j]:
                    counter+=1
        
        if counter>2970:
           print("yes")
        else:
            print("no")
        print(counter)
        
    
    cv2.imshow("roImg", roImg)
    cv2.imshow("frame", frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release
cv2.destroyAllWindows
