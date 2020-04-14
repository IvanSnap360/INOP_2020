from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import time
import cv2
import numpy as np
import serial
import sys

# Testirovanie
showRects = (len(sys.argv) > 1) and (sys.argv[1] == "test")
# Razmer kubika shablona
tSize = 50
# Porog dlya shablona
tThreshold = 500
# Koordinaty kubikov v shablone
tCoords = [
    [475, 710],
    [540, 710],
    [600, 710],
    [665, 710],
    [725, 705],
    [785, 700]
]

# Razmer kubika na sklade
sSize = 100
# Porog dlya sklada
sThreshold = 1000
# Koordinaty kubikov na sklade
sCoords = [
    [230, 330],
    [360, 310],
    [520, 300],
    [700, 300],
    [840, 310],
    [970, 320],
]

# Nastoyka tsvetov
boundaries = [
    ([0, 0, 90],   [100, 100, 255], 1, "R"),
    ([0, 60, 0],    [110, 255, 110], 2, "G"),
    ([90, 0, 0],   [255, 110, 110], 3, "B"),
    ([130, 130, 130], [255, 255, 255], 4, "W"),
    ([0, 100, 100],  [100, 255, 255], 5, "Y"),
]




# Podkluchenie k arduino
if not showRects:
    print("Connecting to Arduino...")
    arduino = serial.Serial('/dev/ttyUSB0', 9600)

while True:
    # Tsveta shablona
    tColors = ["N", "N", "N", "N", "N", "N"]
    # Tsveta na sklade
    sColors = ["N", "N", "N", "N", "N", "N"]
    if not showRects:
        print("Waiting data from arduino...")
        sys.stdout.flush()
        msg = "";
        while(msg != b'GO!\r\n'):
            msg = arduino.readline()
            print ("Message from arduino: " + str(msg))
            sys.stdout.flush()
    for step in range(1): 
        print ("Detecting colors")
        # Podkluchaem kamery
        camera = PiCamera()
        camera.resolution = (1280, 1024)
        rawCapture = PiRGBArray(camera)
        time.sleep(1);
        # Delaem foto
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        camera.close()
        # Pokazyvaem kvadratiki
        #if showRects:
        for n in tCoords:
            cv2.rectangle(image, (n[0], n[1]), (n[0] + tSize, n[1] + tSize), (0,255,0), 3)
        for n in sCoords:
            cv2.rectangle(image, (n[0], n[1]), (n[0] + sSize, n[1] + sSize), (0,0,255), 3)
        if showRects:
          cv2.imshow("Image2", image)
        cv2.imwrite("/home/pi/Desktop/WRO2/img.png", image) 


        for (lower, upper, index, color) in boundaries:
            lower = np.array(lower, dtype = "uint8")
            upper = np.array(upper, dtype = "uint8")
            mask = cv2.inRange(image, lower, upper)
            
            idx = -1
            max = 0
            clr = 0
            for n in range(len(tCoords)):    
                ctr = mask[tCoords[n][1]:tCoords[n][1] + tSize, tCoords[n][0]:tCoords[n][0] + tSize]
                #cv2.imshow("Im-"+str(n), ctr)
                nzCount = cv2.countNonZero(ctr)
                print(["SMALL", n, color, nzCount])
                if (nzCount > tThreshold) and (nzCount > max) :
                    max = nzCount
                    idx = n
                    clr = color
            if idx >= 0:
                tColors[idx] = clr

            
            idx = -1
            max = 0
            clr = 0
            for n in range(len(sCoords)):
                ctr = mask[sCoords[n][1]:sCoords[n][1] + sSize, sCoords[n][0]:sCoords[n][0] + sSize]
                #cv2.imshow("Im-"+str(n), ctr)
                nzCount = cv2.countNonZero(ctr)
                print(["LARGE", n, color, nzCount])
                
                if (nzCount > sThreshold) and (nzCount > max) :
                    max = nzCount
                    idx = n
                    clr = color
            if idx >= 0:
                sColors[idx] = clr
        nc = 0
        for n in range(6):
            if (tColors[n] == 'N'):
                nc = nc + 1
            if (sColors[n] == 'N'):
                nc = nc + 1
        if nc == 2:
            break;
    print("Shablon")
    print(tColors)
    print("Sklad")
    print(sColors)
    sys.stdout.flush()
    if not showRects:
        msg = "";
        for n in tColors:
            msg = msg + n
        for n in sColors:
            msg = msg + n
        msg = msg + "\r\n"
        arduino.write(msg.encode())
    else:
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        break
