import cv2
import numpy as np

# Import de la vidéo
cap = cv2.VideoCapture('vtest.avi')

#
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')

out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280, 720))

total = 0

W = None
H = None

ret, frame1 = cap.read()
ret, frame2 = cap.read()

# Tant que la vidéo est en cours
while cap.isOpened():
    # Différence entre 2 'frames' successives (frame 1 - frame 2)
    # Différence absolue : Tout ce qui apparait et disparait
    diff = cv2.absdiff(frame1, frame2)
    # Convertion de cette différence en notions de gris
    # Passage de la différence en RGB en notion de gris
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    # retire le bruit grace au flou glaussien
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    cv2.imshow(blur,diff)
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
        # récupère les coordonnées du contour
        (x, y, w, h) = cv2.boundingRect(contour)
        # si la surface du contour est trop petite : pas de rectangle et passe au suivant
        if cv2.contourArea(contour) < 900:
            continue
        # sinon : dessine un rectangle à l'emplacement plus haut
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

        M = cv2.moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        if (H//2)+2 > cY > (H//2)-2:
            total += 1

        cv2.circle(frame1, (cX, cY), 2, (255, 255, 255), -1)

    cv2.putText(frame1, "Count: {}".format(total), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
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
