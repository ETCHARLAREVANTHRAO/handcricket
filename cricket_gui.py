import time
import random
import cv2
from tkinter import *
from PIL import Image, ImageTk
import cricket as ct
import os

root = Tk()
var = StringVar()
var.set( "Hand Cricket")
obj = ct.Cricket()

folder_path = "number_images"
my_list = os.listdir(folder_path)
pic_list = []

for i in my_list:
    image = cv2.imread(f'{folder_path}/{i}')
    dim = (200, 200)
    res = cv2.resize(image,dim, interpolation=cv2.INTER_AREA)
    pic_list.append(res)

text = Label(root, width=30,height=1, textvariable=var,font=("Aerial", 20), bg="orange")
text.grid(row=0, column=0, columnspan=2)
frame2 = Frame(root, width=600, height=480, bg="blue")
frame2.grid(row=1, column=0, padx=10, pady=2)
label1 = Label(frame2, width=30, height=1, text= "Game Starts in 4 sec", font=("Aerial", 20), bg="orange")
label1.grid(row=1, column=0)


imgFrame = Frame(root, width=600, height=500)
imgFrame.grid(row=1, column=1, padx=10, pady=2)


label = Label(imgFrame)
label.grid(row=1, column=0)
cap = cv2.VideoCapture(0)
score = 0

count = 0
def show_frame(score, count, pic_list):

    success, frame= cap.read()
    result = obj.score(frame)
    if result == None:
        result = 0
    cv2.putText(frame,  str(result), (25, 400), cv2.FONT_HERSHEY_PLAIN,
                5, (255, 0, 0), 5)
    cv2.putText(frame, str("Score: "+str(score)), (460, 50), cv2.FONT_HERSHEY_PLAIN,
                2, (255, 0, 0), 5)

    if count == 3000:
        if result != None:
            score += result
        else:
            score += 0
        var1 = IntVar()
        answer = random.randint(1, 1)
        var1.set(answer)
        label1 = Label(frame2, width=30, height=1, textvariable=var1, font=("Aerial", 20), bg="orange")
        label1.grid(row=1, column=0)
        img = ImageTk.PhotoImage(image= Image.fromarray(pic_list[answer]))
        label1 = Label(frame2,image=img)
        label1.image = img
        label1.grid(row=2, column=0)
        if answer == result:
            root.destroy()
            win = Tk()
            text = Label(win, width=30, height=10, text="Game over..Your Score is " + str(score), font=("Aerial", 20), bg="Green")
            text.grid(row=0, column=0, columnspan=2)

        time.sleep(2)
        count = 0

    else:
        cv2.putText(frame, str(int(count/700)), (100, 150), cv2.FONT_HERSHEY_PLAIN,
                    5, (255, 255, 0), 10)
        count += 100

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    label.imgtk = imgtk
    label.configure(image=imgtk)


    return label.after(50, lambda:show_frame(score, count, pic_list))

show_frame(score, count, pic_list)
root.mainloop()

