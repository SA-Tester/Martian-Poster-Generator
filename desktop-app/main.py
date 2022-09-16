import datetime
import tkinter as tk
from PIL import Image, ImageTk
from EMTimeConverter import converEarthTimeToMartian

#create root window
window = tk.Tk()

def addSpirit():
    return

def addCuriosity():
    return

def addOpportunity():
    return

def earthClock():
    now = datetime.datetime.now()
    currentDate = str(now.day) + " - " + str(now.month) + " - " + str(now.year)
    earthDate = tk.Label(window, text=currentDate, font=('Arial 15'), bg="black", fg="white", width=25)
    earthDate.place(x=10, y=120)

    currentTime = str(now.hour) + " : " + str(now.minute) + " : " + str(now.second)
    earthTime = tk.Label(window, text=currentTime, font=('Arial 15'), bg="black", fg="white", width=25)
    earthTime.place(x=10, y=150)

    window.after(200, earthClock)

def marsClock():
    now = datetime.datetime.now()
    marsData = converEarthTimeToMartian(now.year, now.month, now.day, now.hour, now.minute, now.second)
    
    yearAndMonth = "    Year: " + str(marsData[0]) + "   |   Month: " + str(marsData[1])
    marsDate1 = tk.Label(window, text=yearAndMonth, font=('Arial 15'), bg="black", fg="white", width=25)
    marsDate1.place(x=985, y=120)

    LSAndSol = "Ls: " + str(marsData[2]) + "  |   Sol: " + str(marsData[3])
    marsDate2 = tk.Label(window, text=LSAndSol, font=('Arial 15'), bg="black", fg="white", width=25)
    marsDate2.place(x=985, y=150)

    window.after(200, marsClock)

def createWindow():
    #set app width, height and location on screen (x, y)
    app_width = 1280
    app_height = 960
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight() - 80
    x = (screen_width/2) - (app_width/2)
    y = (screen_height/2) - (app_height/2)

    #window title and center window set under the dimensions
    window.title("The Martian Lands")
    window.geometry('%dx%d+%d+%d' % (app_width, app_height, x, y))

    #add background image
    #mars image: Perseverance's Left Navcam Views Ingenuity During its Third Flight
    background_image = Image.open("images/mars.png")
    background_photoimage= ImageTk.PhotoImage(background_image)
    background_label = tk.Label(image=background_photoimage)
    background_label.image = background_photoimage
    background_label.place(x=0, y=0)

    title_text = tk.Label(window, text="The Martian Lands", font=("Arial 20"), width=100, height=2, fg="#fff", bg="#000")
    title_text.pack()

    # display earth date and time
    earthDateLabel = tk.Label(window, text="Date on Earth", font=('Arial 15'), bg="black", fg="white", width="25")
    earthDateLabel.place(x=10, y=90)
    earthClock()

    # display martian date and time
    marsDateLabel = tk.Label(window, text="Date on Mars", font=('Arial 15'), bg="black", fg="white", width="25")
    marsDateLabel.place(x=985, y=90)
    marsClock()

    #execute tkinter
    return window.mainloop()

createWindow()