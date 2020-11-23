import cv2
import numpy as np

cap = cv2.VideoCapture('vtest.avi')
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')

out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280, 720))

totalUp = 0
totalDown = 0

testX = None
testY = None

W = None
H = None

ret, frame1 = cap.read()
ret, frame2 = cap.read()


while cap.isOpened():
    # Différence entre 2 'frames' successives
    diff = cv2.absdiff(frame1, frame2)
    # Convertion de cette différence en notions de gris
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    # retire le bruit grace au flou glaussien
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # (image à traiter, valeur du seuil, couleur des objets seuillés, type de seuil( ici binaire :
    # Seuil > objet : 0
    # Seuil < objet : couleur définie juste avant))
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    # Dilatation de l'image
    dilated = cv2.dilate(thresh, None, iterations=3)
    # retrouver les contours.
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Parcourir tout les contours de l'image

    if W is None or H is None:
        (H, W) = frame1.shape[:2]

    for contour in contours:
        # créé un rectangle sur le contour
        (x, y, w, h) = cv2.boundingRect(contour)
        # si la surface du contour est trop petite : pas de rectangle et passe au suivant
        if cv2.contourArea(contour) < 900:
            continue
        # sinon : dessine un rectangle à l'emplacement plus haut
        # params : (image, start_point (x,y), end_point (x, y), color (Blue,Green,Red), thickness(épaisseur))
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # centre d'une personne
        M = cv2.moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        if testY is not None:
            if cY == (H // 2) and (H // 2) < testY:
                totalUp += 1

            if cY == (H // 2) and (H // 2) > testY:
                totalDown += 1

        # point central du gars
        cv2.circle(frame1, (cX, cY), 2, (255, 255, 255), -1)

        testX = cX
        testY = cY

    cv2.putText(frame1, "A: {}".format(totalUp), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    cv2.putText(frame1, "B: {}".format(totalDown), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

    cv2.line(frame1, (0, H // 2), (W, H // 2), (0, 255, 255), 2)

    image = cv2.resize(frame1, (1280, 720))
    out.write(image)
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if frame2 is None:
        break

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()
out.release()
