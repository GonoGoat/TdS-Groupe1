from tkinter import *
from firstFrame import FrameCapture

# Fenêtre principale
window = Tk()

#Personnalisation
window.title('Traitement de signal')
window.geometry("1080x720")
window.minsize(480, 360)
#window.iconbitmap('') import d'image
window.config(background='grey')

#Seconde fenêtre fonction
def open_url() :
	newWindow = Toplevel(window)
	newWindow.title('Vidéo')
	newWindow.geometry('720x480')
	newWindow.config(background="#4065A4")
	FrameCapture()
	

	
#Frame
frameOpen = Frame(window, bg='grey', bd=1)
frameCount = Frame(window, bg='grey', bd=1)

#Text
label_title = Label(window, text="Compteur de passage", 
font=('Arial', 30), bg='grey', fg="white")
label_title.pack(side=TOP)

label_add = Label(frameOpen, text="Ajouter une vidéo", 
font=('Arial', 15), bg='grey', fg="white")
label_add.pack(expand=YES)

label_inPass = Label(frameCount, text="Nombre de personne(s) qui rentre(nt) : ", 
font=('Arial', 15), bg='grey', fg="white")
label_inPass.pack(side=TOP)



#Button
button_add = Button(frameOpen, text="Choisir", font=("Arial",15), bg="white", fg="grey", command=open_url)
button_add.pack(pady=25, fill=X)

#link = Entry(frameOpen, font=('Arial', 20), bg="#4065A4", fg='white')
#link.pack()

#Input

InPass = Entry(frameCount, font=('Arial', 20), bg="#4065A4", fg='white')
InPass.pack()

label_outPass = Label(frameCount, text="Nombre de personne(s) qui sorte(nt) : ", 
font=('Arial', 15), bg='grey', fg="white")
label_outPass.pack(side=TOP)

OutPass = Entry(frameCount, font=('Arial', 20), bg="#4065A4", fg='white')
OutPass.pack()

#Ajout aux frames
frameOpen.pack(expand=YES)
frameCount.pack(expand=YES)


#Affichage de la fenêtre
window.mainloop()