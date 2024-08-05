import cv2
import math
from ultralytics import YOLO

model = YOLO('best.pt')

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, )

classes = model.names

while True:
    ret, frame = cap.read()

    if not ret:
        break

    #results = model(frame)[0]
    results = model(frame, stream=True)

    #caixas = results.render()[0]

    #print(classes)

    for r in results:
        boxes = r.boxes

        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

            confianca = math.ceil((box.conf[0]*100))/100
            print(f'Confiança: {confianca}')

            classe = int(box.cls[0])
            print(f'Classe: {classe}')

            org = [x1, y1-15]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = .75
            color = (0, 255, 0)
            thickness = 2

            cv2.putText(frame, f'{classes[classe]}, {confianca}', org, font, fontScale, color, thickness)

    cv2.imshow('YOLOv8', frame)

    # print(caixas.shape)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()