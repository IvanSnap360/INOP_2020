####импорт библиотеки
import cv2
import numpy as np
cap=cv2.VideoCapture(0)
cells_min = np.array((0,0,0), np.uint8)
cells_max = np.array((255, 255, 42), np.uint8)
#подготовка обазца знака
stop=cv2.imread("E:\\IVAN\\Ivan_desktop\\Kvantorium\\Competitions\\INOP_2020\\src\\CV\\help\\tr\\pic.jpg")# считываем изображение
stop=cv2.resize(stop,(64,64))#обрезаем его до размера 64х64
stop=cv2.inRange(stop,cells_min,cells_max)#бинаризуем
cv2.imshow("stop",stop)#выводим

while(True):
                ret,frame=cap.read()#читаем изображение с камеры
                frameCopy=frame.copy()#делаем копию изображения для контуров
                hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV_FULL)#переводим HSV
                hsv=cv2.blur(hsv,(5,5))#размыте
                mask=cv2.inRange(hsv,cells_min,cells_max)#бинаризация
                mask=cv2.erode(mask,None,iterations=2)#сглаживаем помехи
                mask=cv2.dilate(mask,None,iterations=4)#сглаживаем помехи
                contours=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)#находим контуры
                #берем опред. часть от контуров
                # сортировка не может работать с пустым массивом поэтому делаем услови 
                if contours:#
                                contours=sorted(contours[0],key=cv2.contourArea,reverse=True)#сортровка контуров, нахождение большего
                                cv2.drawContours(frame,contours,-1,(0,0,255),2)#рисуем контуры на изнач. изо.
                                (x,y,w,h)=cv2.boundingRect(contours[0])# 
                                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)#рисуем прямоугольный контур
                                roImg=frameCopy[y:y+h,x:x+w]# обрезаем изо. с камеры
                                roImg=cv2.resize(roImg,(64,64))#
                                roImg=cv2.inRange(roImg,cells_min,cells_max)# бинарезуем
                                cv2.imshow("Contours and frame",frame)#
                                cv2.imshow("rectangle",frame)#
                                cv2.imshow("shape",roImg)#
                                stop_val=0#
                                #по элементам массива сравниваем изображения
                                for i in range(64):
                                                for j in range(64):
                                                              if roImg[i][j]==stop[i][j]:
                                                                              stop_val+=1 #счётчик "похожести"
                                print(stop_val)#
                                if stop_val>3355:
                                                print("yes")
                                else:
                                                print("no")

                cv2.imshow("Original Frame",frame)
                cv2.imshow("Mask frame",mask)
                
                if cv2.waitKey(1)==ord("q"):
                                break
cap.release()
cv2.destroyAllWindows()
