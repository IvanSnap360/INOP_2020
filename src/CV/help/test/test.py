import cv2

cap = cv2.VideoCapture(0)

# while True:
#     #ret, frame = cap.read()
#     frame = cv2.imread("E:\\IVAN\\Ivan_desktop\\Kvantorium\\Competitions\\INOP_2020\\src\\CV\\help\\test\\pic.jpg")
#     cv2.imshow("Frame", frame)

#     if cv2.waitKey(1) == ord('q'):
#         break

cap.release()
cv2.destroyAllWindows