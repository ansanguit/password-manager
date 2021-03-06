FONT = ("Arial", 12, "normal")
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    # Password Generator Project
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for letter in range(nr_letters)]
    password_symbols = [random.choice(symbols) for symbol in range(nr_symbols)]
    password_numbers= [random.choice(numbers) for number in range(nr_numbers)]

    #for char in range(nr_letters):
        #password_list.append(random.choice(letters))

    #for char in range(nr_symbols):
        #password_list += random.choice(symbols)

    #for char in range(nr_numbers):
        #password_list += random.choice(numbers)

    password_list = password_letters+password_symbols+password_numbers

    random.shuffle(password_list)

    password = "".join(password_list) # to reduce the code and get a string from a list of characters.
    #for char in password_list:
        #password += char
    password_entry.insert(0, password)
    pyperclip.copy(password) # to get the password in the clipboard

    print(f"Your password is: {password}")

# ---------------------------- SAVE PASSWORD ------------------------------- #


def add_password():

    # how to create pop ups. Standard dialogs - message boxes
    website = website_entry.get()
    email = user_entry.get()
    password = password_entry.get()
    new_data={
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title= "Oops", message="Please make sure you have entered a password and website")
    else:
       is_ok =messagebox.askokcancel(title=website, message= f"These are the details entered  {email} | {password} is this ok to save?")

       if is_ok:
           try:
               with open("data.json", "r") as data_file:
                   data = json.load(data_file)
           except FileNotFoundError:
               with open("data.json", "w") as data_file:
                   json.dump(new_data, data_file, indent =4)
           else:
               #updating with the new data
               data.update(new_data)
               with open("data.json", "w") as data_file:
                   # saving the updated data
                   json.dump(data, data_file, indent=4)

          # f = open("password_db.txt", "a")
          # f.write(f"{website_entry.get()} | {user_entry.get()} | {password_entry.get()}\n")
          # f.close()
           finally:
               messagebox.showinfo(title="Hurray", message=f"Password for {website} successfully saved")
               print(f"Password for {website} successfully saved")
               website_entry.delete(4, END)
               password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    website_search = website_entry.get()
    try:
        with open("data.json") as data_file:
            data =json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo("Error", message="No data file found.")
    else:
        if website_search in data:
            email = data[website_search]["email"]
            password = data[website_search]["password"]
            messagebox.showinfo(title=website_search, message=f"Email={email} \n Password: {password}")
        else:
            messagebox.showinfo(title= "Error", message=f"No password saved for {website_search}")


# ---------------------------- UI SETUP ------------------------------- #



window = Tk()
window.title("Password Generator")
window.config(padx =50, pady=50)


canvas = Canvas(width =200, height =200)
lock_img = PhotoImage(file="lock.png") # important to add the file=
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

website = Label(text="Website:", font= FONT)
website.grid(column= 0, row= 1)

user = Label(text="Email/Username:", font= FONT)
user.grid(column = 0, row=2)

password = Label(text="Password:", font = FONT)
password.grid(column=0, row=3)

web = StringVar()
website_entry = Entry(width = 35, textvariable = web)
website_entry.focus() # this gets the cursor on this entry when we open
website_entry.grid(column=1, row= 1, columnspan =1, sticky="w")

user_entry= Entry(width= 45, font= FONT)
user_entry.insert(0, "ansanguit@gmail.com") #this is to prepopulate the user
user_entry.grid(column=1, row= 2, columnspan =2, sticky= "w") # columnspan to take more than one column

password_entry = Entry(width=45, font= FONT)
password_entry.grid(column=1, row= 3, sticky="w")

generate = Button(text="Generate Password", font= FONT, command= generate_password, fg= "green", activebackground="black")
generate.grid(column=2, row = 3)

add= Button(width = 30, text="Add", font=FONT, fg= "pink", activebackground="black", command= add_password)
add.grid(column= 1, row= 4, columnspan=2)  # sticky to align the label, entry or button

search = Button(width = 17, text="Search", font=FONT, fg= "green", activebackground="black", command= find_password)
search.grid(column= 2, row= 1)  # sticky to align the label, entry or button



window.mainloop()
