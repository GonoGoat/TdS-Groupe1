import cv2
import numpy as np

cap = cv2.VideoCapture('vtest.avi')
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')

out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280, 720))

W = None
H = None

ret, frame1 = cap.read()
ret, frame2 = cap.read()

diff = cv2.absdiff(frame1, frame2)
cv2.imshow('Test', diff)

while cap.isOpened():
    # Différence entre 2 'frames' successives
    diff = cv2.absdiff(frame1, frame2)
    print(diff)
    # Convertion de cette différence en notions de gris
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    # retire le bruit en grace au flou glaussien (filtre passe bande)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # (image à traiter, valeur du seuil, couleur des objets seuillés, type de seuil( ici binaire :
    # Seuil > objet : 0
    # Seuil < objet : couleur définie juste avant))
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    cv2.imshow('Test', thresh)
    # Dilatation de l'image
    dilated = cv2.dilate(thresh, None, iterations=3)
    # retrouver les contours.
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Parcourir tout les contours de l'image
    for contour in contours:
        # récupère les coordonnées du contour
        (x, y, w, h) = cv2.boundingRect(contour)
        # si la surface du contour est trop petite : pas de rectangle et passe au suivant
        if cv2.contourArea(contour) < 900:
            continue
        # sinon : dessine un rectangle à l'emplacement plus haut
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

    if W is None or H is None:
        (H, W) = frame1.shape[:2]

    cv2.line(frame1, (0, H // 2), (W, H // 2), (0, 255, 255), 2)

    image = cv2.resize(frame1, (1280, 720))
    out.write(image)
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()
out.release()
