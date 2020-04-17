import cv2
import numpy as np



if __name__ == '__main__':
    def nothing(*arg):
        pass

cap = cv2.VideoCapture(0)

cv2.namedWindow( "settings" ) 


cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings', 255, 255, nothing)
cv2.createTrackbar('s2', 'settings', 255, 255, nothing)
cv2.createTrackbar('v2', 'settings', 255, 255, nothing)

while(1):

    _, frame = cap.read()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h1 = cv2.getTrackbarPos('h1', 'settings')
    s1 = cv2.getTrackbarPos('s1', 'settings')
    v1 = cv2.getTrackbarPos('v1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    s2 = cv2.getTrackbarPos('s2', 'settings')
    v2 = cv2.getTrackbarPos('v2', 'settings')
    
    lower_color = np.array([h1,s1,v1], np.uint8)
    upper_color = np.array([h2, s2, v2], np.uint8)

    mask = cv2.blur(hsv, (7, 7))    
    mask = cv2.inRange(mask, lower_color, upper_color)

    res = cv2.bitwise_and(frame, frame, mask = mask)

    #cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
   

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()