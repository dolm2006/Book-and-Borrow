# Book & Borrow system extras
# Daniel Monaghan

from tkinter import *
from datetime import datetime
import textwrap
import hashlib

# Function to do a binary search on a 2D array, with given second index
def binary_search(array, target, index):
    position = -1
    found = False
    low = 0
    high = len(array) - 1

    while not found and low <= high:
        mid = (low + high) // 2
        
        if array[mid][index] == target:
            found = True
            position = mid
            
        elif array[mid][index] > target:
            high = mid - 1
            
        else:
            low = mid + 1

    return position

# Function to hash passwords
def hash_password(password):
    m = hashlib.sha256()

    password_mid = password.encode('utf-8')
    
    m.update(password_mid)
    
    return m.hexdigest()

#-----Procedures to use if the query returns nothing-----
def no_results(centre): # Used for borrower section
    title = Label(centre, text="Sorry currently there are no books available")
    title.pack()
    title.config(font="Helvetica 30 bold", bg = "beige")

def no_results_res(centre): # Used for librarian section
    title = Label(centre, text="There are currently no reservations")
    title.pack()
    title.config(font="Helvetica 30 bold", bg = "beige")
#--------------------------------------------------------

# Procedure to display an error screen
def error_screen(app_details):
    # Destroy old window
    app_details[1].destroy()

    # Create new window
    root_error = Tk()
    root_error.title("Error")
    root_error.state("zoomed")

    # Display text
    message = Label(root_error, text="We are sorry but there has been an error with the database connection").pack()
    instruct = Label(root_error, text="Please close and reopen the software").pack()

    # Close connection if it exists
    if app_details[0]:
        app_details[0].close()
    
    font_all_widgets(root_error, ("Helvetica", 20))

    root_error.mainloop()


# Function to count the number of items in the user's cart
def count_cart(cart):
    items = 0
    for counter in range(len(cart)):
        if cart[counter] != "":
            items += 1
    return items

#-----Formatting procedures-----
# Function to combine title and sub title if they both exist
def title_combine(title, sub_title):
    if sub_title is None:
        full_title = title
    else:
        full_title = title + "-" + sub_title
    return full_title

# Function to wrap text within given character amount
def wrap_text(text, width):
    full_title = textwrap.wrap(text, width)
    title_format = "\n".join(full_title)
    return title_format

# Procedure to change the bg colour of all widgets in a window/frame
def colour_all_widgets(centre, colour):
    for widget in centre.winfo_children():
        widget.config(bg=colour)

# Procedure to destroy all widgets in a frame
def delete_all_widgets(centre):
    for widget in centre.winfo_children():
        widget.destroy()

# Procedure to change the font of all the widgets in a window/frame
def font_all_widgets(centre, font_set):
    for widget in centre.winfo_children():
        widget.config(font=font_set)

# Procedurevto convert date format from YYYY-MM-DD to DD-MM-YYYY
def convert_date(current):
    updated = datetime.strptime(str(current), "%Y-%m-%d").strftime("%d-%m-%Y")
    return updated

# Procedure to destroy all the frames in a window
def destroy_frames(window_frames):
    for frame in window_frames:
        frame.destroy()
#-------------------------------



