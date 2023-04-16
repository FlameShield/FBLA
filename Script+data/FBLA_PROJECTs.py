#importing tkinter to use it's gui and abilities
import random as rnd
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from tkcalendar import Calendar
from tktooltip import ToolTip
from PIL import Image, ImageTk
import pandas as pd
import csv
import os

#creates the relative path
absolute_path = os.path.dirname(__file__)

#makes a vsriable for the csv file paths
file_prefix = absolute_path+'\csv_files'

#restarts the program from the beginning
def restart():
    window.destroy()
    login_screen()
    
#closes the currently open admin window
def admin_close(current_window):
    current_window.destroy()
    admin_home_function()
    
#closes the whole program when a toplevel window is closed
def on_toplevel_close():
    window.destroy()
    
#Goes through and makes sure every csv file exists and creates them if not
if not os.path.exists(file_prefix+r'\user_account_details.csv'):
    with open(file_prefix+r'\user_account_details.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['username', 'password', 'email', 'grade','points'])
        file.close()
if not os.path.exists(file_prefix+r'\admin_account_details.csv'):
    with open(file_prefix+r'\admin_account_details.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['username', 'password'])
        file.close()
if not os.path.exists(file_prefix+r'\user_submissions.csv'):
    with open(file_prefix+r'\user_submissions.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['username', 'password', 'event', 'date','file'])
        file.close()
if not os.path.exists(file_prefix+r'\student_prizes.csv'):
    with open(file_prefix+r'\student_prizes.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['prize', 'points', 'file'])
        file.close()
        
#Creates an image for the submissions
def image(master_view,submissions_list,i):
    
    #grabs the photo folder's path
    path = absolute_path + r'\Phuutuuzs\\'
    
    #creates the photos full path
    list_image = path + submissions_list[i][4]
    # Load the image
    img = Image.open(list_image)
  
    # Resize the image
    img = img.resize((150, 100), resample=Image.BICUBIC)

    # Convert the resized image to a Tkinter-compatible format
    tk_img = ImageTk.PhotoImage(img)

    # Create a Tkinter label with the image
    label = Label(master_view, image=tk_img)

    # Keep a reference to the image to prevent garbage collection
    label.image = tk_img
    
    #Return the label for use
    return label

#Function for the submissions
def submission_approval(master_view):
    global button_pressed
    
    #Toplevel closes program
    master_view.protocol("WM_DELETE_WINDOW", on_toplevel_close)
    
    #creates a submissions list
    submissions_list = []
    #opens the submissions file
    with open(file_prefix+r'\user_submissions.csv', 'r') as f:
        
        #reads it
        mycsv = csv.reader(f)
        mycsv = list(mycsv)
        
        #for loop for the amount of rows
        for i in range(len(pd.read_csv(file_prefix+r'\user_submissions.csv'))):
            #creates another folder for reach row
            submission_row = []
            
            #goes through the row and sets each column to the submission_row list
            for x in range(5):
                row_number = i+1
                column_number = x
                text = mycsv[row_number][column_number]
                submission_row.append(text)
            
            #adds the row list to the overall list
            submissions_list.append(submission_row)
        f.close()
        
    #Function to get rid of a user's submission
    def delete_submission(user):
        
        # open the CSV file in read mode
        with open(file_prefix+r'\user_submissions.csv', mode='r', newline='') as csv_file:
            
            # create a CSV reader object
            csv_reader = csv.reader(csv_file)
            
            # read the contents of the file into a list
            rows = list(csv_reader)
            csv_file.close()

        # filter the rows to remove the ones that match the target user
        rows = [row for row in rows if row[0] != user]

        # open the same CSV file in write mode
        with open(file_prefix+r'\user_submissions.csv', mode='w', newline='') as csv_file:
            
            # create a CSV writer object
            csv_writer = csv.writer(csv_file)
            
            # write the modified rows back to the file
            csv_writer.writerows(rows)
            
            csv_file.close()
            
    #Function to give a user their points
    def point_adder(user):
        
        # open the CSV file in read mode
        with open(file_prefix+r'\user_account_details.csv', mode='r', newline='') as csv_file:
            
            # create a CSV reader object
            csv_reader = csv.reader(csv_file)
            
            # create a list to store the modified rows
            rows = []
            
            # loop through each row
            for row in csv_reader:
                
                # check if the first column's data matches the user value
                if row[0] == user:
                    
                    # Give the user's points an added 5
                    row[4] = int(row[4])+5
                    
                # append the modified row to the list
                rows.append(row)
                
            csv_file.close()

        # open the CSV file in write mode
        with open(file_prefix+r'\user_account_details.csv', mode='w', newline='') as csv_file:
            
            # create a CSV writer object
            csv_writer = csv.writer(csv_file)
            
            # write the modified rows
            csv_writer.writerows(rows)
            
            csv_file.close()
        
        #run the delete function
        delete_submission(user)
        
    #creates and sets the variable to check for button clicks
    button_pressed = tk.BooleanVar()
    button_pressed.set(False)

    #creates a function to handle the actions of an approved submission
    def approve(i):
        global yesnt
        global button_pressed
        
        #sets the button true to have the loop run again
        button_pressed.set(True)
        
        #sets yesnt to 1 to display that points were added
        yesnt = 1
        point_adder(submissions_list[i][0])
        submission_frame.destroy()
    def deny():
        global yesnt
        global button_pressed
        button_pressed.set(True)
        yesnt = 0
        delete_submission(submissions_list[i][0])
        submission_frame.destroy()


    for i in range(len(submissions_list)):
        def approve_button():
            approve(i)
        def go_back():
            admin_close(master_view)
        button_pressed.set(False)
        
        submission_frame = tk.Frame(master_view)
        submission_frame.grid(row=0,column=0)
        
        image(submission_frame,submissions_list,i).grid(row=0,column=0,columnspan=4,sticky=NSEW)
        
        submission_label = tk.Label(master=submission_frame,borderwidth=1,relief="solid",text=f"User: {submissions_list[i][0]} | Event: {submissions_list[i][2]} | Date: {submissions_list[i][3]} | File: {submissions_list[i][4]}")
        submission_label.grid(row=1,column=0,columnspan=4)
        
        approve_button = tk.Button(master=submission_frame,text="Approve",command=approve_button)
        approve_button.grid(row=2,column=1,sticky=NSEW)
        
        deny_button = tk.Button(master=submission_frame,text="Deny",command=deny)
        deny_button.grid(row=2,column=2,sticky=NSEW)
        
        approval_feedback = tk.Label(master=submission_frame,text="")
        approval_feedback.grid(row=3,column=1,columnspan=2)
        
        back_button = tk.Button(master=submission_frame,text="go back",command=go_back)
        back_button.grid(row=4,column=1,columnspan=2)
        
        if yesnt == 0:
            approval_feedback.configure(text=f"Gave {submissions_list[i-1][0]} 0 points")
        elif yesnt == 1:
            approval_feedback.configure(text=f"Gave {submissions_list[i-1][0]} 5 points")
        
        master_view.wait_variable(button_pressed)

def account_treeview(master_view):
    # define columns
    master_view.protocol("WM_DELETE_WINDOW", on_toplevel_close)
    columns = ('Username', 'Password', 'Email', 'Grade', 'Points')

    tree = ttk.Treeview(master = master_view, columns=columns, show='headings')

    # define headings
    tree.heading('Username', text='Username')
    tree.heading('Password', text='Password')
    tree.heading('Email', text='Email')
    tree.heading('Grade', text ='Grade')
    tree.heading('Points', text='Points')

    # generate sample data
    contacts = []
    with open(file_prefix+r'\user_account_details.csv', 'r') as f:
        mycsv = csv.reader(f)
        mycsv = list(mycsv)
        for i in range(len(pd.read_csv(file_prefix+r'\user_account_details.csv'))):
            contact_row = []
            for x in range(5):
                row_number = i+1
                column_number = x
                text = mycsv[row_number][column_number]
                contact_row.append(text)
            contacts.append(contact_row)
        f.close()

    # add data to the treeview
    user_count = 0
    for contact in contacts:
        tree.insert('', tk.END, text=f"user {user_count}",values=contact)
        user_count = user_count+1


    def item_selected(event):
        global user_number
        global record
        global item
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']
            user_number = item['text']
            # show a message
            username_entry.delete(0,tk.END)
            username_entry.insert(0, record[0])
            password_entry.delete(0,tk.END)
            password_entry.insert(0, record[1])
            email_entry.delete(0,tk.END)
            email_entry.insert(0, record[2])
            grade_entry.delete(0,tk.END)
            grade_entry.insert(0, record[3])
            points_entry.delete(0,tk.END)
            points_entry.insert(0, record[4])


    tree.bind('<<TreeviewSelect>>', item_selected)

    tree.grid(row=0, column=0, columnspan=5,sticky='nsew')

    # add a scrollbar
    scrollbar = ttk.Scrollbar(master = master_view, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=5, sticky='ns')

    username_label = tk.Label(master = master_view,text="username")
    username_label.grid(row=1,column=0)
    username_entry = tk.Entry(master = master_view)
    username_entry.grid(row=2,column=0)

    password_label = tk.Label(master = master_view,text="password")
    password_label.grid(row=1,column=1)
    password_entry = tk.Entry(master = master_view)
    password_entry.grid(row=2,column=1)

    email_label = tk.Label(master = master_view,text="email")
    email_label.grid(row=1,column=2)
    email_entry = tk.Entry(master = master_view)
    email_entry.grid(row=2,column=2)

    grade_label = tk.Label(master = master_view,text="grade")
    grade_label.grid(row=1,column=3)
    grade_entry = tk.Entry(master = master_view)
    grade_entry.grid(row=2,column=3)

    points_label = tk.Label(master = master_view,text="points")
    points_label.grid(row=1,column=4)
    points_entry = tk.Entry(master = master_view)
    points_entry.grid(row=2,column=4)

    def submit():
        global user_number
        global record
        name_get = username_entry.get()
        pass_get = password_entry.get()
        email_get = email_entry.get()
        grade_get = grade_entry.get()
        points_get = points_entry.get()
        new_data = [name_get, pass_get, email_get, grade_get, points_get]
        selected_item = tree.selection()[0]
        tree.item(selected_item, text=user_number, values=new_data)
        
        with open(file_prefix+r'\user_account_details.csv', mode='r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            data = list(csv_reader)
            csv_file.close()

        for row in data:
            if row[0] == record[0]:
                row[0],row[1],row[2],row[3],row[4] = new_data[0],new_data[1],new_data[2],new_data[3],new_data[4]

        with open(file_prefix+r'\user_account_details.csv', mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(data)
            csv_file.close()
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']
            user_number = item['text']


    submit_button = tk.Button(master = master_view,text="submit changes",command=submit)
    submit_button.grid(row=3,column=2)
    def go_back():
        admin_close(master_view)
    back_button = tk.Button(master=master_view,text="go back",command=go_back)
    back_button.grid(row=4,column=2)

def user_page_buttons(framed):
    def user_home():
        framed.destroy()
        user_home_top()
    def user_account():
        framed.destroy()
        user_account_top()
    def user_submit():
        framed.destroy()
        user_submit_top()
    def user_prizes():
        framed.destroy()
    def user_tracker():
        framed.destroy()
    #defines a function that adds the page buttons to the user's view
    global user_home_frame
    user_home_frame = tk.Frame(master=framed)
    user_home_frame.grid(row=0,rowspan=5,column=0,columnspan=7)
    home_select = tk.Button(master=user_home_frame,width=15,height=3,text="Home",command=user_home)
    home_select.grid(row=0,column=0,sticky=tk.W,pady=3,padx=5)
    ToolTip(home_select, msg="Go home", delay=1)
    account_select = tk.Button(master=user_home_frame,width=15,height=3,text="Account",command=user_account)
    account_select.grid(row=1,column=0,sticky=tk.W,padx=5)
    ToolTip(account_select, msg="Account settings", delay=1)
    submit_select = tk.Button(master=user_home_frame,width=15,height=3,text="Submit",command=user_submit)
    submit_select.grid(row=2,column=0,sticky=tk.W,padx=5)
    ToolTip(submit_select, msg="Submission", delay=1)
    prizes_select = tk.Button(master=user_home_frame,width=15,height=3,text="Prizes",command=user_prizes)
    prizes_select.grid(row=3,column=0,sticky=tk.W,padx=5)
    ToolTip(prizes_select, msg="View prizes", delay=1)
    tracker_select = tk.Button(master=user_home_frame,width=15,height=3,text="Tracker",command=user_tracker)
    tracker_select.grid(row=4,column=0,sticky=tk.W,padx=5)
    ToolTip(tracker_select, msg="Track your points", delay=1)
        
def create_account():
    
    #The window for the creation of an account
    def get_new_info():
        def add_user(username, password):
            with open(file_prefix+r'\user_account_details.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, password])
                file.close()
        #collects the username and password entered, and then deletes the into
        y = username_create_entry.get()
        y1 = password_create_entry.get()
        add_user(y,y1)
        
        #destroys the create account window
        window_create.destroy()
        
    #setting the create accounts root and parameters
    window_create = tk.Tk()
    window_create.columnconfigure([0], minsize=250)
    window_create.rowconfigure([0, 6], minsize=100)
    
    #label for creating an account
    hello = tk.Label(master=window_create,text="Create New Account",font=("Calibri",18))
    hello.grid(row=0,column=0)
    
    #creating and placing the create accounts username and passwords label and entrys
    username_create = tk.Label(master=window_create,text="Username")
    username_create.grid(row=1,column=0)
    username_create_entry = tk.Entry(master=window_create)
    username_create_entry.grid(row=2,column=0)
    password_create = tk.Label(master=window_create,text="Password")
    password_create.grid(row=3,column=0)
    password_create_entry = tk.Entry(master=window_create)
    password_create_entry.grid(row=4,column=0)
    enter_create = tk.Button(master=window_create,text="Create",command=get_new_info)
    enter_create.grid(row=5,column=0)
    
    #starts the create accounts loop
    window_create.mainloop()
    
def login_screen():
    global window
    
    #login screen to define if you are an admin or a user
    def login_top_window():
        def get_login(): 
            global temp_user_username
            global temp_user_password
            #geting the fields text   
            x = username_entry.get()
            x1 = password_entry.get()
            if x == "" or x1 == "":
                answer = tk.Label(master=login_top,text="Missing Field(s)")
                answer.grid(row=11,column=0)
                return False
            
            def check_user_login(username, password):
                with open(file_prefix+r'\user_account_details.csv', 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row[0] == username and row[1] == password:
                            return True
                    file.close()
                    return False
            def check_admin_login(username, password):
                with open(file_prefix+r'\admin_account_details.csv', 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row[0] == username and row[1] == password:
                            return True
                    file.close()
                    return False
                
            #checks the values of x and sees if you can enter an admin or user window
            if check_user_login(x,x1) == True:
                answer = tk.Label(master=login_top,text="User Correct")
                answer.grid(row=11,column=0)
                temp_user_username = x
                temp_user_password = x1
                login_top.destroy()
                user_home_top()
            elif check_admin_login(x,x1) == True:
                answer = tk.Label(master=login_top,text="Admin Correct")
                answer.grid(row=11,column=0)
                login_top.destroy()
                admin_home_function()
            else:
                answer = tk.Label(master=login_top,text="     Incorrect     ")
                answer.grid(row=11,column=0)
                
        def hit_enter_button(event):
            #paths the event key "Enter" to the enter button's command
            get_login()
            
        window.withdraw()
        login_top = Toplevel()
        login_top.geometry("350x300")
        
        login_top.protocol("WM_DELETE_WINDOW", on_toplevel_close)
        #creating an event key for "Enter"
        login_top.bind('<Return>', hit_enter_button)
        
        #creating and placing the school name and software name
        school_name = tk.Label(master=login_top,text="Francis Howell North",font=("Calibri",30))
        school_name.grid(row=0,column=0)
        software = tk.Label(master=login_top,text="Shotty-Ann Software",font=("Calibri",22))
        software.grid(row=1,column=0)
        
        #creating the username and password labels, and entrys
        username_label = tk.Label(master=login_top,text="Username")
        username_label.grid(row=3,column=0)
        username_entry = tk.Entry(master=login_top)
        username_entry.grid(row=5,column=0)
        password_label = tk.Label(master=login_top,text="Password")
        password_label.grid(row=7,column=0)
        password_entry = tk.Entry(master=login_top,show="•")
        password_entry.grid(row=9,column=0)
        
        #creating the enter button to check the entered information
        enter_button = tk.Button(master=login_top,text="Enter",command=get_login)
        enter_button.grid(row=10,column=0)
        
        #creating the create account button
        create_account_button = tk.Button(master=login_top,text="Create Account",command=create_account,pady=2)
        create_account_button.grid(row=12,column=0)
        login_top.mainloop()
    #configuring the login window's root and parameters
    window = tk.Tk()
    window.eval('tk::PlaceWindow . center')
    login_top_window()
    
    #Begins the loop to display the window
    window.mainloop()
def admin_home_function():
    global admin_home_top
    def logout():
        admin_home_top.destroy()
        restart()
    admin_home_top = Toplevel()
    admin_home_top.geometry("240x230")
    admin_home_top.protocol("WM_DELETE_WINDOW", on_toplevel_close)
    admin_home_frame = tk.Frame(master=admin_home_top)
    admin_home_frame.pack()
    accounts_info = tk.Button(master=admin_home_frame,text="Accounts Info",width=15,height=6,command=admin_accounts_top).grid(row=0,column=0,sticky=NSEW)
    prizes_edit = tk.Button(master=admin_home_frame,text="Prizes",width=15,height=6).grid(row=0,column=1,sticky=NSEW)
    submissions = tk.Button(master=admin_home_frame,text="Submissions",width=15,height=6,command=admin_submissions_top).grid(row=1,column=0,sticky=NSEW)
    winners = tk.Button(master=admin_home_frame,text="Winners/report",width=15,height=6,command=admin_winner_top).grid(row=1,column=1,sticky=NSEW)
    log_out = tk.Button(master=admin_home_frame,text="Log Out",command=logout)
    log_out.grid(row=2,column=0,columnspan=2)
    admin_home_top.mainloop()
def admin_submissions_top():
    global admin_submission_top
    global yesnt
    yesnt = 2

    admin_submission_top = Toplevel()
    admin_submission_top.protocol("WM_DELETE_WINDOW", on_toplevel_close)
    admin_home_top.destroy()
    submission_approval(admin_submission_top)
    
    admin_submission_top.grid_propagate(1)
    admin_submission_top.mainloop()
def admin_accounts_top():
    admin_account_top = Toplevel()
    admin_account_top.protocol("WM_DELETE_WINDOW", on_toplevel_close)
    admin_home_top.destroy()
    account_treeview(admin_account_top)
    admin_account_top.grid_propagate(1)
    admin_account_top.mainloop()
def admin_winner_top():
    admin_home_top.destroy()
    def winners():
        highest_value = None
        nine_grade = []
        ten_grade = []
        eleven_grade = []
        twelve_grade = []
        with open(file_prefix+r'\user_account_details.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            # Skip the header row
            next(reader)
            for row in reader:
                # Check if the second column value is greater than 10
                if int(row[3]) == 9:
                    # Append the row to the data list
                    nine_grade.append(row[0])
                elif int(row[3]) == 10:
                    # Append the row to the data list
                    ten_grade.append(row[0])
                elif int(row[3]) == 11:
                    # Append the row to the data list
                    eleven_grade.append(row[0])
                elif int(row[3]) == 12:
                    # Append the row to the data list
                    twelve_grade.append(row[0])
            file.close()
        highest_value = None

        with open(file_prefix+r'\user_account_details.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            # Skip the header row
            next(reader)
            for row in reader:
                # Check if the second column value is greater than the current highest value
                if highest_value is None or int(row[4]) > highest_value:
                    # Update the highest value
                    highest_value = int(row[4])
                    highest_value_name = row[0]
            file.close()

        rndnine, rndten, rndeleven, rndtwelve = rnd.choice(nine_grade), rnd.choice(ten_grade), rnd.choice(twelve_grade), rnd.choice(twelve_grade)
        def prize_selection_high(point_value):
            prize = ""
            with open(file_prefix+r'\student_prizes.csv', mode='r', newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)
                
                for row in csv_reader:
                    if int(point_value) >= int(row[1]):
                        prize = prize + "," + row[0]
                    else:
                        if prize == "":
                            prize = "Nothing"
                        return prize
            return prize
        with open(file_prefix+r'\user_account_details.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader )
            for row in reader:
                if row[0] == rndnine:
                    rndnine_pnt = row[4]
                if row[0] == rndten:
                    rndten_pnt = row[4]
                if row[0] == rndeleven:
                    rndeleven_pnt = row[4]
                if row[0] == rndtwelve:
                    rndtwelve_pnt = row[4]
                if row[0] == highest_value_name:
                    highest_value_name_pnt = row[4]
                
        nine_win.configure(text=f"Nineth Grade Winner\n{rndnine} | Prize = {prize_selection_high(rndnine_pnt)}")
        ten_win.configure(text=f"Tenth Grade Winner\n{rndten} | Prize = {prize_selection_high(rndten_pnt)}")
        eleven_win.configure(text=f"Eleventh Grade Winner\n{rndeleven} | Prize = {prize_selection_high(rndeleven_pnt)}")
        twelve_win.configure(text=f"Twelveth Grade Winner\n{rndtwelve} | Prize = {prize_selection_high(rndtwelve_pnt)}")
        highest_win.configure(text=f"Highest Point Winner\n{highest_value_name} | Prize = {prize_selection_high(highest_value_name_pnt)}")
        
    def report():
        report_top = Toplevel()
        report_title = tk.Label(master=report_top,text="FHN STUDEN REPORT",font=("Calibri",22))
        report_title.grid(row=0,column=0,columnspan=2)
        contacts = []
        with open(file_prefix+r'\user_account_details.csv', 'r') as f:
            mycsv = csv.reader(f)
            mycsv = list(mycsv)
            for i in range(len(pd.read_csv(file_prefix+r'\user_account_details.csv'))):
                contact_row = []
                for x in range(5):
                    row_number = i+1
                    column_number = x
                    text = mycsv[row_number][column_number]
                    contact_row.append(text)
                contacts.append(contact_row)
            f.close()

        first = 0
        extra_dis = 0
        total_divide = len(pd.read_csv(file_prefix+r'\user_account_details.csv')) / 2
        if str(total_divide).endswith('.5'):
            extra_dis = 1
        for x in range(len(pd.read_csv(file_prefix+r'\user_account_details.csv')) // 2):
            for y in range(2):
                label = tk.Label(master=report_top,borderwidth=1,relief="solid",text=f"User: {contacts[first][0]}\nPass: {contacts[first][1]}\nEmail: {contacts[first][2]}\nGrade: {contacts[first][3]}\nPoints: {contacts[first][4]}")
                label.grid(column=y,row=x+1,sticky=NSEW)
                first += 1
        if extra_dis == 1:
            label_row = label.grid_info()['row']
            label = tk.Label(master=report_top,borderwidth=1,relief="solid",text=f"User: {contacts[first][0]}\nPass: {contacts[first][1]}\nEmail: {contacts[first][2]}\nGrade: {contacts[first][3]}\nPoints: {contacts[first][4]}")
            label.grid(column=0,row=label_row+1,sticky=NSEW)
        report_top.grid_propagate(1)
        report_top.mainloop()
    admin_winner_top = Toplevel()
    admin_winner_top.protocol("WM_DELETE_WINDOW", on_toplevel_close)
    
    generate_winners = tk.Button(master=admin_winner_top,text="Generate Winners",command=winners)
    generate_winners.grid(row=0,column=1,sticky=NSEW)
    
    generate_report = tk.Button(master=admin_winner_top,text="Generate Report",command=report)
    generate_report.grid(row=0,column=2,sticky=NSEW)
    
    nine_win = tk.Label(master=admin_winner_top,wraplength=200,borderwidth=1,relief="solid",text="Nineth Grade Winner")
    nine_win.grid(row=1,column=0,sticky=NSEW)
    
    ten_win = tk.Label(master=admin_winner_top,wraplength=200,borderwidth=1,relief="solid",text="Tenth Grade Winner")
    ten_win.grid(row=1,column=1,sticky=NSEW)
    
    eleven_win = tk.Label(master=admin_winner_top,wraplength=200,borderwidth=1,relief="solid",text="Eleventh Grade Winner")
    eleven_win.grid(row=1,column=2,sticky=NSEW)
    
    twelve_win = tk.Label(master=admin_winner_top,wraplength=200,borderwidth=1,relief="solid",text="Twelveth Grade Winner")
    twelve_win.grid(row=1,column=3,sticky=NSEW)
    
    highest_win = tk.Label(master=admin_winner_top,wraplength=200,borderwidth=1,relief="solid",text="Highest Point Winner")
    highest_win.grid(row=2,column=1,columnspan=2,sticky=NSEW)
    
    def go_back():
        admin_close(admin_winner_top)
    back_button = tk.Button(master=admin_winner_top,text="go back",command=go_back)
    back_button.grid(row=3,column=1,columnspan=2)
    
    admin_winner_top.grid_propagate(1)
    admin_winner_top.mainloop()
def user_home_top():
    global temp_user_username
    global temp_user_password
    global counter
    counter = 0
    #creating the user's root window
    user_home_top = Toplevel()
    user_home_top.protocol("WM_DELETE_WINDOW", on_toplevel_close)
    user_home_top.geometry("650x315")
    
    #calls the page buttons function
    user_page_buttons(user_home_top)
    
    #creating the calendar
    home_page_name = tk.Label(master=user_home_top,text="FHN EVENT SOFTWARE",font=("Times New Roman",25))
    home_page_name.grid(row=0,column=1,columnspan=9,rowspan=2)
    calendargrid1 = tk.Label(master=user_home_frame,relief="solid",text="3/20/23 6pm Men's Basketball",wraplength=60,borderwidth=1,width=10,height=4)
    calendargrid1.grid(row=2,column=1,sticky=tk.S,padx=0,pady=0)
    calendargrid2 = tk.Label(master=user_home_frame,relief="solid",text="3/21/23 No Event",wraplength=60,borderwidth=1,width=10,height=4)
    calendargrid2.grid(row=2,column=2,sticky=tk.S,padx=0,pady=0)
    calendargrid3 = tk.Label(master=user_home_frame,relief="solid",text="3/22/23 No Event",wraplength=60,borderwidth=1,width=10,height=4)
    calendargrid3.grid(row=2,column=3,sticky=tk.S,padx=0,pady=0)
    calendargrid4 = tk.Label(master=user_home_frame,relief="solid",text="3/23/23 No Event",wraplength=60,borderwidth=1,width=10,height=4)
    calendargrid4.grid(row=2,column=4,sticky=tk.S,padx=0,pady=0)
    calendargrid5 = tk.Label(master=user_home_frame,relief="solid",text="3/24/23 5pm Football Game",wraplength=60,borderwidth=1,width=10,height=4)
    calendargrid5.grid(row=2,column=5,sticky=tk.S,padx=0,pady=0)
    calendargrid6 = tk.Label(master=user_home_frame,relief="solid",text="3/25/23 4:30pm Bowling League",wraplength=60,borderwidth=1,width=10,height=4)
    calendargrid6.grid(row=2,column=6,sticky=tk.S,padx=0,pady=0)
    calendargrid7 = tk.Label(master=user_home_frame,relief="solid",text="3/26/23 No Event",wraplength=60,borderwidth=1,width=10,height=4)
    calendargrid7.grid(row=2,column=7,sticky=tk.S,padx=0,pady=0)
    calendargrid8 = tk.Label(master=user_home_frame,relief="solid",text="3/27/23 5pm Women's Basketball",wraplength=60,borderwidth=1,width=10,height=4)
    calendargrid8.grid(row=3,column=1,sticky=tk.S,padx=0,pady=0)
    calendargrid9 = tk.Label(master=user_home_frame,relief="solid",text="3/28/23 5:30pm Choir Concert",wraplength=60,borderwidth=1,width=10,height=4)
    calendargrid9.grid(row=3,column=2,sticky=tk.S,padx=0,pady=0)
    calendargrid10 = tk.Label(master=user_home_frame,relief="solid",text="3/29/23 No Event",wraplength=60,borderwidth=1,width=10,height=4)
    calendargrid10.grid(row=3,column=3,sticky=tk.S,padx=0,pady=0)
    calendargrid11 = tk.Label(master=user_home_frame,relief="solid",text="3/30/23 5pm Women's Volleyball",wraplength=60,borderwidth=1,width=10,height=4)
    calendargrid11.grid(row=3,column=4,sticky=tk.S,padx=0,pady=0)
    calendargrid12 = tk.Label(master=user_home_frame,relief="solid",text="3/31/23 6pm Band Concert",wraplength=60,borderwidth=1,width=10,height=4)
    calendargrid12.grid(row=3,column=5,sticky=tk.S,padx=0,pady=0)
    calendargrid13 = tk.Label(master=user_home_frame,relief="solid",text="4/1/23 No Event",wraplength=60,borderwidth=1,width=10,height=4)
    calendargrid13.grid(row=3,column=6,sticky=tk.S,padx=0,pady=0)
    calendargrid14 = tk.Label(master=user_home_frame,relief="solid",text="4/2/23 No Event",wraplength=60,borderwidth=1,width=10,height=4)
    calendargrid14.grid(row=3,column=7,sticky=tk.S,padx=0,pady=0)
    calendargrid15 = tk.Label(master=user_home_frame,relief="solid",text="4/3/23 5pm Foortball Game",wraplength=60,borderwidth=1,width=10,height=4)
    calendargrid15.grid(row=4,column=1,sticky=tk.S,padx=0,pady=0)
    calendargrid16 = tk.Label(master=user_home_frame,relief="solid",text="4/4/23No Event",wraplength=60,borderwidth=1,width=10,height=4)
    calendargrid16.grid(row=4,column=2,sticky=tk.S,padx=0,pady=0)
    calendargrid17 = tk.Label(master=user_home_frame,relief="solid",text="4/5/23 4:30pm Men's Basketball",wraplength=60,borderwidth=1,width=10,height=4)
    calendargrid17.grid(row=4,column=3,sticky=tk.S,padx=0,pady=0)
    calendargrid18 = tk.Label(master=user_home_frame,relief="solid",text="4/6/23 6pm Chess Tourney",wraplength=60,borderwidth=1,width=10,height=4)
    calendargrid18.grid(row=4,column=4,sticky=tk.S,padx=0,pady=0)
    calendargrid19 = tk.Label(master=user_home_frame,relief="solid",text="4/7/23 5:40pm Football Game",wraplength=60,borderwidth=1,width=10,height=4)
    calendargrid19.grid(row=4,column=5,sticky=tk.S,padx=0,pady=0)
    calendargrid20 = tk.Label(master=user_home_frame,relief="solid",text="4/8/23 No Event",wraplength=60,borderwidth=1,width=10,height=4)
    calendargrid20.grid(row=4,column=6,sticky=tk.S,padx=0,pady=0)
    calendargrid21 = tk.Label(master=user_home_frame,relief="solid",text="4/9/23 5pm Women's Basketball",wraplength=60,borderwidth=1,width=10,height=4)
    calendargrid21.grid(row=4,column=7,sticky=tk.S,padx=0,pady=0)
    
    #starts the loop for the user's window
    user_home_top.mainloop()
def user_account_top():
    def logout():
        user_account_top.destroy()
        restart()
    user_account_top = Toplevel()
    user_account_top.protocol("WM_DELETE_WINDOW", on_toplevel_close)
    user_account_top.geometry("650x330")  
    
    with open(file_prefix+r'\user_account_details.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            # Skip the header row
            next(reader)
            for row in reader:
                if row[0] == temp_user_username:
                    temp_user_email = row[2]
                    temp_user_points = row[4]
    
    user_account_frame = tk.Frame(master=user_account_top)
    user_account_frame.grid(column=7,row=1,columnspan=3,rowspan=3,sticky=tk.W)
    
    user_info_label = tk.Label(master=user_account_frame,borderwidth=1,relief="solid",text=f"Account Info",font=("Calibri",25))
    user_info_label.grid(row=0,column=0,columnspan=3,sticky=NSEW)
    user_info_username = tk.Label(master=user_account_frame,borderwidth=1,relief="groove",text=f"Username: {temp_user_username}",font=("Calibri",15))
    user_info_username.grid(row=1,column=0,columnspan=2,sticky=NSEW)
    user_info_password = tk.Label(master=user_account_frame,borderwidth=1,relief="groove",text=f"Password: {temp_user_password}",font=("Calibri",15))
    user_info_password.grid(row=2,column=0,columnspan=2,sticky=NSEW)
    user_info_email = tk.Label(master=user_account_frame,borderwidth=1,relief="groove",text=f"Email: {temp_user_email}",font=("Calibri",15))
    user_info_email.grid(row=1,column=2,sticky=NSEW)
    user_info_points = tk.Label(master=user_account_frame,borderwidth=1,relief="groove",text=f"Points: {temp_user_points}",font=("Calibri",15))
    user_info_points.grid(row=2,column=2,sticky=NSEW)
    
    log_out = tk.Button(master=user_account_frame,text="Log Out",command=logout)
    log_out.grid(row=3,column=1)
    
    user_page_buttons(user_account_top)
    
    user_account_top.mainloop()
def user_submit_top():
    global counter
    global event_get
    global file_path
    global file_path_confirmation
    global file_name
    file_path = ""
    event_get = ""
    file_name = ""
    file_path_confirmation = 0
    def UploadAction(event=None):
        global file_path
        global file_path_confirmation
        global file_name
        file_path = filedialog.askopenfilename()
        if file_path.lower().endswith((".ppm",".png","jpeg",".gif",".tiff",".bmp")):
            file_name = os.path.basename(file_path)
            file_path_confirmation = 1
            file_submit_feedback.configure(wraplength=120,text=f"Submitted {file_path}")
        elif file_path == "":
            file_submit_feedback.configure(text="Missing Photo")
            file_path = ""
        else:
            file_submit_feedback.configure(text="Not valid file")
            file_path = ""
    def get_submission():
        global event_get
        global file_name
        date_ent = cal.get_date()
        if event_get == "":
            submit_drop_feedback.configure(text="Missing Field")
            submit_final_feedback.configure(text="")
        elif date_ent == "":
            submit_drop_feedback.configure(text="")
        elif file_path_confirmation == 0:
            submit_drop_feedback.configure(text="")
            submit_final_feedback.configure(text="")
            file_submit_feedback.configure(text="Missing Field")
        else:
            submit_final_feedback.configure(text="Submitted")
            with open(file_prefix+r'\user_submissions.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([temp_user_username, temp_user_password, event_get, date_ent, file_name])
                file.close()
    
    user_submit_top = Toplevel()
    user_submit_top.protocol("WM_DELETE_WINDOW", on_toplevel_close)
    user_submit_top.geometry("615x330")
    user_page_buttons(user_submit_top)
    
    user_submit_frame = tk.Frame(master=user_submit_top)
    user_submit_frame.grid(column=7,row=0,columnspan=8,rowspan=7,sticky=tk.E)
    
    submit_label = tk.Label(master=user_submit_frame,borderwidth=1,relief="solid",text="Submit",font=("Calibri",35))
    submit_label.grid(row=0,column=0,columnspan=8,sticky=tk.NSEW)
    
    submit_drop_text = tk.Label(master=user_submit_frame,text="Event")
    submit_drop_text.grid(row=1,column=0,sticky=tk.W)
    submit_drop_var = ttk.Combobox(user_submit_frame, values=["Band","Basketball","Chess","Choir","Football","Golf","Iron Chef","Prom","Robotics","Spirit Week","Swimming","Vollyball"])
    submit_drop_var.grid(row=2,column=0,sticky=tk.W)
    submit_drop_feedback = tk.Label(master=user_submit_frame,text="")
    submit_drop_feedback.grid(row=3,column=0,sticky=tk.W)
    def on_select(event):
        global event_get
        event_get = event.widget.get()

    # Bind the function to the ComboboxSelected event
    submit_drop_var.bind("<<ComboboxSelected>>", on_select)
    
    cal = Calendar(master=user_submit_frame, selectmode='day', year=2023, month=4, day=6)
    cal.grid(row=1,column=7,rowspan=7,sticky=tk.E)
    file_submit_button = tk.Button(master=user_submit_frame,text="Submit Photo",command=UploadAction)
    file_submit_button.grid(row=4,column=0,sticky=tk.W)
    file_submit_feedback = tk.Label(master=user_submit_frame,text="")
    file_submit_feedback.grid(row=5,column=0,sticky=tk.W)
    event_date_submit = tk.Button(master=user_submit_frame,text="Submit",command=get_submission)
    event_date_submit.grid(row=6,column=0,sticky=tk.W)
    submit_final_feedback = tk.Label(master=user_submit_frame,text="")
    submit_final_feedback.grid(row=7,column=0,sticky=tk.W)

    user_submit_top.mainloop()

#begins the program from the loging screen
login_screen()