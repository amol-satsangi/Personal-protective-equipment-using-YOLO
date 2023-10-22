from ultralytics import YOLO
import cv2
import cvzone
import math
# cap = cv2.VideoCapture(0) #for webcame
# cap.set(3, 1280)
# cap.set(4, 720)
cap = cv2.VideoCapture("Videos/ppe-1.mp4")

model = YOLO("ppe.pt")
classNames = ['Excavator', 'Gloves', 'Hardhat', 'Ladder', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest', 'Person', 'SUV', 'Safety Cone', 'Safety Vest', 'bus', 'dump truck', 'fire hydrant', 'machinery', 'mini-van', 'sedan', 'semi', 'trailer', 'truck and trailer', 'truck', 'van', 'vehicle', 'wheel loader']
myColor = (0, 0, 255)
while True:
    success, img = cap.read()
    results = model(img, stream = True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            #for cv2
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # print(x1, y1, x2, y2)
            # cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            #for cv zone
            w, h = x2-x1, y2-y1
            bbox = int(x1), int(y1), int(w), int(h)
            # cvzone.cornerRect(img, bbox)
            cv2.rectangle(img, (x1, y1), (x2, y2), myColor, thickness=3)
            conf = math.ceil((box.conf[0]*100))/100
            # print(conf)

            cls = int(box.cls[0])
            currentClass = classNames[cls]
            print(currentClass)
            if conf>0.5:
                if currentClass == "Excavator" or currentClass == "Safety Vest" or currentClass == "Mask":
                    myColor = (0, 255, 0)
                elif currentClass == "NO-Hardhat" or currentClass == "NO-Safety Vest" or currentClass == "NO-Mask":
                    myColor = (0, 0, 255)
                else:
                    myColor = (255, 0, 0)

            cvzone.putTextRect(img, f'{conf} {classNames[int(cls)]}', (max(0, x1), max(0, y1-20)), scale=0.5, thickness=1, colorB=myColor, colorT=(255, 255, 255), colorR=myColor, offset=5)
            cv2.rectangle(img, (x1, y1), (x2, y2), myColor, thickness=3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
