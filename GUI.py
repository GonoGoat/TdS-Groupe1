from tkinter import *
import cv2
import time
from firstFrame import FrameCapture

def videoAnalyse(point, sens, entree, video):
    cap = cv2.VideoCapture(video)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')

    out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280, 720))

    totalUp = 0
    totalDown = 0

    testX = None
    testY = None

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    (H, W) = frame1.shape[:2]

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
            if sens == "V":
                if testX is not None and point+2 > cX > point-2:
                    if cX < testX:
                        print(cX, ' < ', testX)
                        totalUp += 1
                        ChangeInput(totalUp, totalDown, entree)

                    elif cX > testX:
                        print(cX, ' > ', testX)
                        totalDown += 1
                        ChangeInput(totalUp, totalDown, entree)

            elif sens == "H":
                if testY is not None and point+2 > cY > point-2:
                    if cY < testY:
                        print(cY, ' < ', testY)
                        totalUp += 1
                        ChangeInput(totalUp, totalDown, entree)

                    elif cY > testY:
                        print(cY, ' > ', testY)
                        totalDown += 1
                        ChangeInput(totalUp, totalDown, entree)

            # point central du gars
            cv2.circle(frame1, (cX, cY), 2, (255, 255, 255), -1)

            testX = cX
            testY = cY
        if entree == "up" or entree == "right":
            cv2.putText(frame1, "Entrees: {}".format(totalUp), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            cv2.putText(frame1, "Sorties: {}".format(totalDown), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        elif entree == "down" or entree == "left":
            cv2.putText(frame1, "Entrees: {}".format(totalDown), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            cv2.putText(frame1, "Sorties: {}".format(totalUp), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
        if sens == "H":
            cv2.line(frame1, (0, point), (H,point), (0, 255, 255), 2)
        else:
            cv2.line(frame1, (point, 0), (point, W), (0, 255, 255), 2)
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


# Fenêtre principale
window = Tk()

# Personnalisation
window.title('Traitement de signal')
window.geometry("1080x720")
window.minsize(480, 360)
# window.iconbitmap('') import d'image
window.config(background='grey')

sens = "H"
entree = "up"
toSend = []
video = "Essai"
path = []


def nothing(x):
    pass


# Seconde fenêtre fonction

def open_url():
    path.append(FrameCapture())
    originalImage = cv2.imread('./image/frame_0.jpg')
    cv2.namedWindow("Frame")
    cv2.setMouseCallback("Frame", mouse_drawing)
    cv2.imshow("Frame", originalImage)


def newWindow():
    newWindow = Toplevel(window)
    newWindow.title('Vidéo')
    newWindow.geometry('720x480')
    newWindow.config(background="#4065A4")


def mouse_drawing(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        if (buttonSens['text'] == "Vertical"):
            sens = "V"
            if (buttonEntree['text'] == "Extérieur - Intérieur"):
                entree = "right"
            else:
                entree = "left"
        else:
            sens = "H"
            if (buttonEntree['text'] == "Intérieur\nExtérieur"):
                entree = "up"
            else:
                entree = "down"

        if sens == "H":
            toSend.append(y)

        else:
            toSend.append(x)
        toSend.append(sens)
        toSend.append(entree)
        cv2.destroyWindow('Frame')
        videoAnalyse(toSend[0], toSend[1], toSend[2], path[0])
        path.clear()
        toSend.clear()
    """
    if len(coords) == 1:
        xdiff = abs(coords[0][0] - coords[1][0])
        ydiff = abs(coords[0][1] - coords[1][1])

        if xdiff > ydiff:
            toSend.append(coords[0][1])
            toSend.append("H")
        else:
            toSend.append(coords[0][0])
            toSend.append("V")
        cv2.destroyWindow('Frame')
        videoAnalyse(toSend[0], toSend[1])
"""


def ChangeInput(totalUp, totalDown, entree):
    if entree == "up" or entree == "right":
        InPass.delete(0, END)
        InPass.insert(0, totalUp)
        OutPass.delete(0, END)
        OutPass.insert(0, totalDown)
    elif entree == "down" or entree == "left":
        InPass.delete(0, END)
        InPass.insert(0, totalDown)
        OutPass.delete(0, END)
        OutPass.insert(0, totalUp)


# Frame
frameOpen = Frame(window, bg='grey', bd=1)
frameCount = Frame(window, bg='grey', bd=1)

# Text
label_title = Label(window, text="Compteur de passage",
                    font=('Arial', 30), bg='grey', fg="white")
label_title.pack(side=TOP)

label_add = Label(frameOpen, text="Ajouter une vidéo",
                  font=('Arial', 15), bg='grey', fg="white")
label_add.pack(expand=YES)

label_finaleResult = Label(frameCount, text="Résultat final du comptage :", font=('Arial', 18), bg='grey', fg='white')
label_finaleResult.pack()

label_inPass = Label(frameCount, text="Nombre de personne(s) qui rentre(nt) : ",
                     font=('Arial', 15), bg='grey', fg="white")
label_inPass.pack(side=TOP)

# Button
button_add = Button(frameOpen, text="Choisir", font=("Arial", 15), bg="white", fg="grey", command=open_url)
button_add.pack(pady=25, fill=X)


def getTextButton():
    if (buttonSens['text'] == "Vertical"):
        buttonSens.config(text="Horizontal")
        buttonEntree.config(text="Intérieur\nExtérieur")
    else:
        buttonSens.config(text="Vertical")
        buttonEntree.config(text="Intérieur - Extérieur")


def setEntree():
    if (buttonEntree['text'] == "Intérieur\nExtérieur"):
        buttonEntree.config(text="Extérieur\nIntérieur")
    elif (buttonEntree['text'] == "Extérieur\nIntérieur"):
        buttonEntree.config(text="Intérieur\nExtérieur")
    elif (buttonEntree['text'] == "Extérieur - Intérieur"):
        buttonEntree.config(text="Intérieur - Extérieur")
    else:
        buttonEntree.config(text="Extérieur - Intérieur")


buttonSens = Button(frameOpen, text="Horizontal", font=("Arial", 15), bg="white", fg="grey", command=getTextButton)
buttonSens.pack(pady=40, fill=X)

buttonEntree = Button(frameOpen, text="Intérieur\nExtérieur", font=("Arial", 15), bg="white", fg="grey",
                      command=setEntree)
buttonEntree.pack(pady=60, fill=X)

# link = Entry(frameOpen, font=('Arial', 20), bg="#4065A4", fg='white')
# link.pack()

# Input

InPass = Entry(frameCount, font=('Arial', 20), bg="#4065A4", fg='white')
InPass.pack()

label_outPass = Label(frameCount, text="Nombre de personne(s) qui sorte(nt) : ",
                      font=('Arial', 15), bg='grey', fg="white")
label_outPass.pack(side=TOP)

OutPass = Entry(frameCount, font=('Arial', 20), bg="#4065A4", fg='white')
OutPass.pack()

# Ajout aux frames
frameOpen.pack(expand=YES)
frameCount.pack(expand=YES)

# Affichage de la fenêtre
window.mainloop()
