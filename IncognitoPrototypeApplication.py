#Rob Thurman, Blake McNeil, Logan Cashwell, Kale Samber
#Sledge Distillery Prototype Application
#Date: 4/25/2020
#Purpose: This application shows customers if the alcohol they wish to purchase will put them over the allowable limit or not. If it does, the application will tell them when they can purchase more.

#This section imports the needed modules
import pyodbc
import tkinter as tk # Import tkinter
from tkinter import * 
import tkinter.font 
from PIL import Image
from tkinter import ttk

#This section connects our code to the Access database
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\User\Desktop\sledge.accdb;') #IMPORTANT:change user to your username on your computer's desktop to connect to the database
cursor = conn.cursor()

#This section gives the options for the drop down menus
purchaseCombo = ['One small bottle (750)','Two small bottles (1500)','One large bottle (1500)']
States = ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']




class mainPage:                     
    
    def __init__(self):                     
        window = Tk() #the main application window
        window['bg'] = 'white' #background color
        window.title("Sledge Distillery Check Amount")
        window.geometry("300x400") #the size of the application window
        #----sledge Company Logo-----
        photo = Image.open("C:\\Users\\User\\Desktop\\sledge_logo.png") 
        photo = photo.resize((290,144), Image.ANTIALIAS)
        photo.save("sledge_logo.png","png")
        GW_logo = PhotoImage(file="sledge_logo.png")
        Label(window, image=GW_logo).grid(row = 1,sticky = W)
        Label(window, text = "Purchase Limit Check", font = 'Helvetica 20 bold', bg='white').grid(row= 3, sticky = W)
        Label(window, text="Enter DL#:",bg='orange',font=('Helvetica',10)).grid(row=7) #Label for DL input field

        

    #Entry Variable where users will enter ID number
        global dlEntry
        dlEntry = Entry(window)
        dlEntry.grid(row=8)

        global combo1 #first drop down menu
        combo1 = ttk.Combobox(window, value=purchaseCombo, width = 25, state = 'readonly')
        combo1.grid(row=14)

        global combo2 #second drop down menu
        combo2 = ttk.Combobox(window, value=States,width=25, state = 'readonly')
        combo2.grid(row=11)

        #After making proper selections, this button activtates the checkAmount function
        checkButton = Button(window, text="Check amount", font=("Helvetica",15,"bold"), command = checkAmount).grid(row = 15,sticky = W)
        
        window.grid_columnconfigure(10,minsize=100)
        window.grid_rowconfigure(15,minsize=100)   
        window.mainloop()

        
    

def checkAmount(): #This is the function doing the checking work and communication with the database. 
   #this section takes the DL input/choices from above and assigns them to variables. It then uses .split to pull the relevant information
    dlNumber = int(dlEntry.get())
    dlState = combo2.get() 
    selectedAmount = combo1.get() 
    amount1 = selectedAmount.split('(')
    amount2 = amount1[1].split(')')
    totalAmount = int(amount2[0])
    global nextDate2

    
    cursor.execute('SELECT * FROM "SledgeCustomers" WHERE CusID=? and State=?',dlNumber,dlState) #matches dlNumer and dlState inputs to database entries
    rows = cursor.fetchall()
    cursor.execute('SELECT * FROM "SledgeCustomers" WHERE CusID=? and State=?',dlNumber,dlState)
    
    
    for row in cursor.fetchall():
      if row[1]+totalAmount <= 1500: #adds previous amount purchased to the attempting to be purchased today. It then compares that number to 1500 to see if it is allowed or not
         cartWindow = Tk()
         Label(cartWindow, text = "Purchase Limit Check", font = 'Helvetica 20 bold')
         cartLabel = Label(cartWindow,text='You can make this purchase',bg='green', font=(None,20)) #yes, the customer can make the purchase.
         cartButton = Button(cartWindow,text = 'Ok',command = cartWindow.destroy,bg='gray')
         cartLabel.pack()
         cartButton.pack()
         cartWindow.mainloop()
      else:
         cartWindow = Tk()
         Label(cartWindow, text = "Purchase Limit Check", font = 'Helvetica 20 bold')
         cursor.execute('SELECT nextPurchase FROM "SledgeCustomers" WHERE CusID=? and State=?',dlNumber,dlState)
         for row in cursor.fetchall():
            pass
         nextDate =str(row[0]).split(' ') #these lines search the database for previous purchase date and then adds 30 days
         nextDate2=nextDate[0] #assigns next date to variable
         cartLabel = Label(cartWindow,text='Cannot purchase until'+" " +nextDate2,bg='red', font=(None,20)) #no, cannot purchase. Gives date of next allowed purchase
         cartButton = Button(cartWindow,text = 'Ok',command = cartWindow.destroy,bg='gray')

         cartLabel.pack()
         cartButton.pack()
         cartWindow.mainloop()

  

mainPage()