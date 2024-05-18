from tkinter import *
from tkinter import ttk, messagebox
from datetime import timedelta, datetime, date
import Library_Extras as LE
import Library_Queries as LQ

def main():
    global cart, app_details
    # Create user's cart, made global for accessibility
    cart = [""] * 3

    # Create connection to database
    connection = LQ.db_connect()

    # If connection is successful
    if connection:
        #Create the window
        root = Tk()
        root.title("Book and Borrow")
        root.state("zoomed")
        root.config(bg="beige")

        # Create tuple with connection and window details, made global for accessibility
        app_details = (connection, root)

        # Update any overdue books
        update_status()

        # Display the login/signup start screen
        start_menu()

        root.mainloop()

    # If connection fails
    else:
        # Temp fake window so error screen procedure can be used
        old = Tk()
        app_details = (connection, old)
        LE.error_screen(app_details)


# Procedure to change book status if they're out past their due date
def update_status():
    # Get all book's ISBN and due date that are taken out
    result = LQ.query_select(LQ.SQ1, None, app_details)
    
    # Get the current date
    today = date.today()

    # Loop for every book from the query
    for item in result:
        # If the due date has been passed then change book to be overdue
        if today >= item[1]:
            LQ.query_update(LQ.UQ1, (item[0],), app_details)


# Procedure to display details of start screen
def start_menu():
    #-----Create frames-----
    title_frame = Frame(app_details[1])
    title_frame.pack()

    start_frame = Frame(app_details[1])
    start_frame.pack()
    #-----------------------

    # Colour the background of the window as beige
    LE.colour_all_widgets(app_details[1], "beige")

    #-----Create text displays-----
    title_label = Label(title_frame, text="Book & Borrow", bg="beige")
    title_label.pack()
    title_label.config(font=("Helvetica", 45, "bold"))

    instruction_label = Label(start_frame, text="Please login or Sign up")
    instruction_label.pack(pady = 15)
    #------------------------------

    # Colour background of the widgets as beige
    LE.colour_all_widgets(start_frame, "beige")

    #-----Buttons for user-----
    login_button = Button(start_frame, text = "Login", 
                   command = lambda: [start_frame.destroy(), login_screen()])
    login_button.pack(side = TOP, pady = 10)
    
    signup_button = Button(start_frame, text = "Sign up", 
                    command = lambda: [start_frame.destroy(), sign_up_screen()])
    signup_button.pack(side = TOP, pady = 10)
    #--------------------------

    # Make all the rest of the text and buttons have a font and size
    LE.font_all_widgets(start_frame, ("Helvetica", 30))

    
# Procedure to display details of login screen
def login_screen():
    # Make the username enered global, for later use at cart
    global username

    # Procedure for the validation of user login
    def validate_login():
        global username
        #-----Get the user's inputs-----
        username = user_username.get()
        # Hash the password as soon as its retrieved
        password_hash = LE.hash_password(user_password.get())
        #-------------------------------

        # Find if username exists in the database, using binary search algorithm
        position = LE.binary_search(result, username, 0)

        # If username is found in database
        if position != -1:
            #-----Get the other user details from the query result-----
            stored_password = result[position][1]
            user_type = result[position][2]
            #----------------------------------------------------------

            # If entered password matches database password
            if stored_password == password_hash:
                # Create welcome message for user depending on the type of user they are
                welcome_message = "Welcome " + username + " to the " + ('librarian' if user_type == 1 else 'Book & Borrow') + " system"
                
                # Create popup with that welcome message
                messagebox.showinfo("Access granted", welcome_message)

                # Destroy all the current frames in the window
                LE.delete_all_widgets(app_details[1])

                # Send the user to the appropriate scrren depending on user type
                if user_type == 1:
                    librarian_menu()
                else:
                    catalogue_screen()

            # Else then the password is incorrect
            else:
                messagebox.showerror("Error", "Password is incorrect")
        
        # Else then the username doesn't exist
        else:
            messagebox.showerror("Error", "Username does not exist")

    # Event for entry box binding 
    # Enables the submit button if both entry boxes have text in them 
    def enable_submit_button(*args):
        if user_username.get() and user_password.get():
            submit_button["state"] = NORMAL
        else:
            submit_button["state"] = DISABLED

    # -----Create frames-----
    title_frame = Frame(app_details[1])
    title_frame.pack(pady=30)

    login_frame = Frame(app_details[1])
    login_frame.pack()
    # -----------------------

    # Colour every frame's backgrounds as beige
    LE.colour_all_widgets(app_details[1], "beige")

    # Use query SQ2, Gets all the current user's usernames and passwords
    result = LQ.query_select(LQ.SQ2, None, app_details)

    #-----Create text, entry boxes and submit button for user-----
    title_label = Label(title_frame, text = "Login", bg = "beige", font = ("Helvetica", 30, "underline"))
    title_label.pack()

    username_label = Label(login_frame, text = "USERNAME: ", bg = "beige")
    username_label.pack()

    user_username = Entry(login_frame, width=30)
    user_username.pack(pady = 10)

    password_label = Label(login_frame, text="PASSWORD:", bg="beige")
    password_label.pack()

    user_password = Entry(login_frame, show="*", width=30)
    user_password.pack(pady = 10)
    
    submit_button = Button(login_frame, text="SUBMIT", command=validate_login, state=DISABLED)
    submit_button.pack(pady = 30)
    #-------------------------------------------------------------

    # Button to return to start screen
    return_button = Button(login_frame, text = "Return", 
                    command = lambda: [LE.delete_all_widgets(app_details[1]), start_menu()])
    return_button.pack(pady = 10)

    # Change the font of all labels, entry boxes and buttons
    LE.font_all_widgets(login_frame, ("Helvetica", 25))

    # Bind the entry boxes to an event for every key release
    user_username.bind("<KeyRelease>", enable_submit_button)
    user_password.bind("<KeyRelease>", enable_submit_button)

# Procedure to display the sign up screen information
def sign_up_screen():
    # Procedure to validate user details
    def validate_signup():
        #-----Get all the user's inputs-----
        first_name, last_name, username = user_f_name.get(), user_s_name.get(), user_username.get()
        password, password_conf = user_password.get(), user_password_conf.get()
        #-----------------------------------

        # Search to see if the username already entered already exists
        position = LE.binary_search(result, username, 0)

        # If username is not unique, display popup saying so
        if position > -1:
            messagebox.showerror("ERROR: Username", "Username already in use")

        # If username isn't in correct range (10-20 characters), display popup saying so
        elif not (10 <= len(username) <= 20):
            messagebox.showerror("ERROR: Username", "Username must be 10-20 characters")
        
        # If the password isn't long enough (12 characters minimum), display popup saying so
        elif len(password) < 12:
            messagebox.showerror("ERROR: Password", "Password must be at least 12 characters ")

        # If the password entry doesn't match the re-entry of the password, display popup saying so
        elif password != password_conf:
            messagebox.showerror("ERROR: Password", "Passwords must match")
        
        # Else everything is correct, user can be created
        else:
            #-----Insert new user into database-----
            values = (username, first_name, last_name, LE.hash_password(password), False)
            LQ.query_insert(LQ.IQ1, values, app_details)
            #---------------------------------------

            # Confirmation popup
            messagebox.showinfo("Confirmed", "Welcome new user\nPlease login now")

            #-----Remove the frames used here-----
            sign_up_frame.destroy()
            title_frame.destroy()
            #-------------------------------------

            # Display the login screen to make them sign in fully
            login_screen()

    # Event for text boxes key release
    # Keeps the submit button disabled until there is text in every entry box
    def enable_submit_button():
        if user_f_name.get() and user_s_name.get() and user_username.get() and user_password.get() and user_password_conf.get():
            submit_button["state"] = NORMAL
        else:
            submit_button["state"] = DISABLED

    #-----Create frames and style them-----
    title_frame = Frame(app_details[1])
    title_frame.pack(pady=30)

    sign_up_frame = Frame(app_details[1])
    sign_up_frame.pack()

    LE.colour_all_widgets(app_details[1], "beige")
    #--------------------------------------

    # Get all the usernames currently in the database
    result = LQ.query_select(LQ.SQ3, None, app_details)

    # Create a title for this screen
    title_label = Label(title_frame, text="Sign up", bg="beige", font=("Helvetica 30 underline"))
    title_label.pack()

    #-----Create labels, entry box and submit button for user-----
    f_name_text = Label(sign_up_frame, text="First name:", bg="beige").pack()
    user_f_name = Entry(sign_up_frame)
    user_f_name.pack(pady=5)

    s_name_text = Label(sign_up_frame, text="Surname:", bg="beige").pack()
    user_s_name = Entry(sign_up_frame)
    user_s_name.pack(pady=5)

    username_text = Label(sign_up_frame, text="Username:", bg="beige").pack()
    user_username = Entry(sign_up_frame)
    user_username.pack(pady=5)

    password_text = Label(sign_up_frame, text="Password:", bg="beige").pack()
    user_password = Entry(sign_up_frame, show="*")
    user_password.pack(pady=5)

    conf_password_text = Label(sign_up_frame, text="Confirm Password:", bg="beige").pack()
    user_password_conf = Entry(sign_up_frame, show="*")
    user_password_conf.pack(pady=5)

    submit_button = Button(sign_up_frame, text = "SUBMIT", 
                           command = lambda: validate_signup(), 
                           state = DISABLED)
    submit_button.pack(pady=30)
    #-------------------------------------------------------------

    # Button to return to start screen
    return_button = Button(sign_up_frame, text = "Return", 
                    command = lambda: [LE.delete_all_widgets(app_details[1]), start_menu()])
    return_button.pack()

    # Change the font of all the widgets (except the title)
    LE.font_all_widgets(sign_up_frame, ("Helvetica", 25))

    # Bind all the text boxes the user can use to an event of key release
    text_boxes = [user_f_name, user_s_name, user_username, user_password, user_password_conf]
    for widget in text_boxes:
        widget.bind("<KeyRelease>", lambda event: enable_submit_button())


#Procedure to display catalogue screen
def catalogue_screen():

    # Event procedure for if user scrolls the scrollbar
    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    # Event procedure for if user changes the genre to filter by
    def selection_change(*args):
        # Get value in the drop-down box
        genre = value_inside.get()

        # If no genre is selected
        if genre == "None" or genre == "Genre Filter":
            # Title of page
            title_label.config(text="Available books:")
            
            # All available books with no genre filter used
            result = LQ.query_select(LQ.SQ4A, None, app_details)
        
        # Otherwise use the selected genre
        else:
            # Title of page with the specified genre to filter by
            title_label.config(text="Available books for: \n" + genre)
            
            # All available books using the specified genre as a filter
            result = LQ.query_select(LQ.SQ4B, (genre,), app_details)

        # Delete all the previously shown books
        LE.delete_all_widgets(inner_frame)

        # Generate buttons for books if there are any from query
        if len(result) != 0:
            generate_buttons(result)
        else:
            LE.no_results(inner_frame)

    # Procedure to generate buttons for all available books
    def generate_buttons(result):
        col = 0
        rows = 1

        # Loop for every available book
        for book in result:
            #-----Create display for the current book button-----
            isbn = book[0]
            title = LE.title_combine(book[1], book[2])
            genre = book[3]
            author = book[4] + " " + book[5]

            text_display = LE.wrap_text(title,20) + "\nBy: " + author + "\n\nGenre: " + genre
            #---------------------------------------------

            # Create button for current book
            button_book = Button(inner_frame, text=text_display,
                                 command = lambda isbn = isbn: [LE.destroy_frames((top_frame, bottom_frame)),
                                                           book_details_screen(isbn)],
                                 width = 20, height = 10)
            button_book.grid(row=rows, column=col, padx=5, pady=5)

            #-----Create grid of buttons-----
            col += 1
            # If maximum columns is reached,  move to next row
            if col == 4:
                col = 0
                rows += 1
            #--------------------------------
        
        # Change the font for all the book buttons
        LE.font_all_widgets(inner_frame, ("Helvetica", "25"))

    # Create frame for title, cart button and genre filter drop-down box
    top_frame = Frame(app_details[1], bg = "beige")
    top_frame.pack(side = TOP, fill = X)

    # Set drop-down choices
    choices = ["None", "Non-fiction", "Horror", "Science fiction", "Romance", "Fantasy"]

    # Make a variable to store the option in the drop-down menu and set it to Genre filter initially
    value_inside = StringVar(top_frame)
    value_inside.set("Genre Filter")

    # Create the drop-down box
    genre_menu = OptionMenu(top_frame, value_inside, *choices)

    # Create the title
    title_label = Label(top_frame, text="Available books:", bg="beige")

    # Create a cart button
    cart_button = Button(top_frame, text= "Cart", 
                         command = lambda:
                         [LE.delete_all_widgets(app_details[1]), cart_screen()])

    # Format the three previous widgets
    for widget in [genre_menu, title_label, cart_button]:
        widget.pack(side = LEFT)
        widget.pack_configure(fill=BOTH, expand=True)

    # Change drop-down variable when another option is selected
    value_inside.trace_add("write", selection_change)

    # Change the font of all the previous widgets
    LE.font_all_widgets(top_frame, ("Helvetica", "25"))

    # Create a frame for the catalogue
    bottom_frame = Frame(app_details[1])

    # Create a canvas in the newly made frame
    canvas = Canvas(bottom_frame)

    # Create a scrollbar in the newly made canvas
    scroll = Scrollbar(bottom_frame, orient="vertical", command=canvas.yview, width=30)
    scroll.pack(side="right", fill="y")

    # Format and display the canvas
    canvas.pack(side=LEFT, fill="both", expand=True)
    canvas.configure(yscrollcommand=scroll.set)
    canvas.config(bg="beige")

    # Create a frame inside the canvas
    inner_frame = Frame(canvas)

    # Colour the new frame
    inner_frame.config(bg="beige")

    # Create a window using the new frame
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # Bind the new canvas to an event for whenever the scrollbar is moved
    inner_frame.bind("<Configure>", on_configure)

    # Get all available books, no genre filter applied
    result = LQ.query_select(LQ.SQ4A, None, app_details)

    # Display buttons for all books if there are any returned
    if len(result) != 0:
        generate_buttons(result)
    else:
        LE.no_results(inner_frame)

    # Add the bottom_frame containg the canvas to the screen
    bottom_frame.pack(side=TOP, fill=BOTH, expand=True)


# Procedure to display the book details screen information after being given a specific ISBN
def book_details_screen(isbn):
    
    # Procedure for when the user adds a book to their cart
    def add_book():
        #-----Linear search the global cart for next available space-----
        found = False
        n = 0
        while not found and n < 3:
            # If the current cart space is blank, add the book to cart, and display a popup
            if cart[n] == "":
                found = True
                cart[n] = isbn
                messagebox.showinfo("Confirmed", "Book has been added")

            # Otherwise if the cart ISBN is the same as the on they try to add, display a poup saying so
            elif cart[n] == isbn:
                messagebox.showwarning("Cart error", "Book already in cart")
                # Leave the conditional loop
                found = True

            # Otherwise increment n
            else:
                n += 1
        
        # If blank space or ISBN not found in cart
        if not found:
            messagebox.showerror("Cart error", "Cart is full")
        #----------------------------------------------------------------

    #-----Create frames-----
    top_frame = Frame(app_details[1])
    top_frame.pack(fill=X)

    detail_frame = Frame(app_details[1])
    detail_frame.pack()
    
    bottom_frame = Frame(app_details[1], bg="beige")
    bottom_frame.pack(fill=X)
    #-----------------------

    # Get all the book details for this specific book
    result = LQ.query_select(LQ.SQ5, (isbn,), app_details)

    # Create return button to go back to the catalogue
    return_button = Button(top_frame, text = "Return to catalogue",
                           command = lambda:
                               [LE.delete_all_widgets(app_details[1]), catalogue_screen()])

    # Create a title for the screen
    title_label = Label(top_frame, text="Book details", bg="beige")

    # Create a button to go to the cart screen
    cart_button = Button(top_frame, text = "Cart", 
                         command = lambda:
                             [LE.delete_all_widgets(app_details[1]),cart_screen()])

    # Change the font of the title, cart button and return button
    LE.font_all_widgets(top_frame, ("Helvetica", "30"))

    # Format the previous widgets and add them to the screen
    for widget in [return_button, title_label, cart_button]:
        widget.pack(side = LEFT)
        widget.pack_configure(fill = BOTH, expand = True)

    #-----Retrieve and format all the book detail text-----
    title = LE.title_combine(result[0][1], result[0][2])

    author = result[0][3] + " " + result[0][4]

    genre = result[0][5]

    rating = str(result[0][6]) + "/5"

    # Change date into correct format (YYYY-MM-DD to DD-MM-YYYY)
    date = LE.convert_date(result[0][7])

    blurb = result[0][8]

    # Wraps blurb within width of 100 characters per line
    blurb_format = LE.wrap_text(blurb, 75)
    #------------------------------------------------------

    # Get the maximum line length of the blurb, will be used for creatiion of treeview table
    line_length = max(len(line) for line in LE.textwrap.wrap(blurb, 100))

    # Create an array of tuple to hold the data to go in the treeview table
    data = [("Title:", title), ("By: ", author), ("Genre: ", genre), ("Star rating: ", rating),
            ("Date published:", date), ("Blurb: ", blurb_format)]

    # Create a style for the treeview table and set the font s for the columns
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Helvetica', 15))
    style.configure("Treeview", font=('Helvetica', 15), rowheight=50)

    # Create a treeview table to display book details
    table = ttk.Treeview(detail_frame, columns=("Headings", "Data"), show="headings")
    
    # Set the column width to be 8 times the maximum line length
    table.column("Data", width = line_length * 8)

    # Insert all the data into the treeview table
    for i, (heading, data_value) in enumerate(data, start=len(data)):
        table.insert("", i, values=(heading, data_value))

    # Display the treeview table and format the frame
    table.grid(row=0, column=0, sticky="nsew")
    detail_frame.columnconfigure(0, weight=1)
    detail_frame.rowconfigure(0, weight=1)

    # Create a button to add the current book to cart
    add_to_cart_button = Button(bottom_frame, text="Add to cart", command=lambda: add_book(), font=("Helvetica", "25"))
    add_to_cart_button.pack(side=TOP, anchor=N, pady=5)



# Procedure to display the cart screen information
def cart_screen():

    # Procedure to remove the selected book from the cart
    def remove_book(cart, n):
        cart[n] = ""

        # Confirmation popup
        messagebox.showinfo("Cart", "Book was removed")

        # Refresh the cart display
        LE.delete_all_widgets(bottom_frame)
        display_books()

    # Procedure to display all books in the cart
    def display_books():

        # For every item in cart
        for counter in range(len(cart)):
            book_frame = Frame(bottom_frame, bg = "beige")
            book_frame.pack()
            
            # If there is no book in this slot, display a message saying so
            if cart[counter] == "":
                book_text = Label(book_frame, text = "\t" + str(counter + 1) + ". No book selected")
                book_text.pack(side=TOP, pady = 5)
                book_text.config(font = ("Helvetica", 15), bg = "beige")
            
            # Otherwise, display book
            else:
                # Get the titles of the current book from the database
                result = LQ.query_select(LQ.SQ6, (cart[counter],), app_details)

                # Create a display message for the current book
                display = "\t" + str(counter + 1) + "." + LE.title_combine(result[0][0], result[0][1])

                # Label for the current book
                book_text = Label(book_frame, text = display, bg = "beige")
                book_text.pack(side = LEFT, pady = 5)

                # Create a button which is used to remove the current book from the cart
                remove_button = Button(book_frame, text="X",
                                       command = lambda counter=counter:
                                           [remove_book(cart, counter)])
                remove_button.pack(side = RIGHT, pady = 5)
                
                LE.font_all_widgets(book_frame, ("Helvetica", 25))

    #-----Create frames-----
    top_frame = Frame(app_details[1])
    top_frame.pack(fill=X)

    bottom_frame = Frame(app_details[1], bg = "beige")
    bottom_frame.pack(fill=BOTH)
    #-----------------------

    # Create button to return to the catalogue
    return_button = Button(top_frame, text = "Return to catalogue",
                           command = lambda:
                               [LE.delete_all_widgets(app_details[1]), catalogue_screen()])

    # Create a title for this screen
    title_label = Label(top_frame, text="Your current cart:", bg = "beige")

    # Create a button for the user checking out their books
    checkout_button = Button(top_frame, text = "Checkout", 
                             command = lambda:
                                 [LE.delete_all_widgets(app_details[1]), checkout_screen()],
                             state = DISABLED)


    # Format the widgets in the title frame
    for widget in [return_button, title_label, checkout_button]:
        widget.pack(side = LEFT)
        widget.pack_configure(fill=BOTH, expand=True)

    LE.font_all_widgets(top_frame, ("Helvetica", 30))

    items = LE.count_cart(cart)
    if items > 0:
        checkout_button.config(state = NORMAL)

    # Call the procedure to display the user's current cart books
    display_books()


# Procedure to display checkout screen information
def checkout_screen():
    global username

    # Create a frame
    checkout_frame = Frame(app_details[1], bg = "beige")
    checkout_frame.pack()

    # get current date and time and calculate when the due date will be
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    due_date = current_date + timedelta(days=28)

    # Insert a new reservation with these details into the database
    values_reserve = (username, current_date, current_time, due_date)
    LQ.query_insert(LQ.IQ2, values_reserve, app_details)

    # Get the newly made reservation ID
    values_id = (username, current_date, current_time)
    result = LQ.query_select(LQ.SQ7, values_id, app_details)

    # Seperate out the reservation ID for easier use
    reservation_id = result[0][0]

    # Count how many items the user had in their cart
    items = LE.count_cart(cart)

    # Create a title
    title_label = Label(checkout_frame, text="Confirmed\n")
    title_label.pack()

    # Calculate and display the time to prepare these books
    time_label = Label(checkout_frame, text="Your books will be ready in:\n" + str((items * 5) + 2) + " minutes\n")
    time_label.pack()

    # Calculate and display the cost per day for overdue books
    fee_label = Label(checkout_frame, text="The overdue fees will be:\n£" + str(items * 0.2) + " per day\n")
    fee_label.pack()

    # Display the due date of the books in this order
    due_date_label = Label(checkout_frame, text="The book(s) are due on: " + LE.convert_date(due_date) + "\n\n")
    due_date_label.pack()

    # Loop for every book in the users cart
    for ISBN in range(len(cart)):
        
        # If there is an item in this cart spot
        if cart[ISBN] != "":
            # Change the book to resered
            LQ.query_update(LQ.UQ2, (cart[ISBN],), app_details)

            # Insert a bookReservation of the current book in the newly made reservation
            values_to_insert = (reservation_id, cart[ISBN])
            LQ.query_insert(LQ.IQ3, values_to_insert, app_details)

    # Create a label telling the user to go to the library and pck up their books
    instruction_label = Label(checkout_frame, text="Please exit the program and come to the library to pick up your books\n\n")
    instruction_label.pack(pady=10)

    LE.colour_all_widgets(checkout_frame, "beige")
    
    # Create a button to destroy the window as this is the end of the borrower section
    exit_button = Button(checkout_frame, text = "Exit",
                         command = lambda: [app_details[1].destroy(), app_details[0].close()])
    exit_button.pack(pady = 10)

    LE.font_all_widgets(checkout_frame,("Helvetica", 25))
    title_label.config(font = ("Helvetica", 30, "underline"))


# Procedure to display the options for a librarian to do 
def librarian_menu():
    #-----Create frames-----
    title_frame = Frame(app_details[1], bg = "beige")
    title_frame.pack()

    options_frame = Frame(app_details[1], bg = "beige")
    options_frame.pack()
    #-----------------------

    #-----Create title and prompt for librarian-----
    title_label = Label(title_frame, text="Welcome Librarian")
    title_label.pack(pady = 10)
    title_label.config(font = ("Helvetica", 30, "bold"), bg = "beige")

    instruction_label = Label(options_frame, text="What would you like to do?")
    instruction_label.pack(pady = 5)
    instruction_label.config(bg = "beige")
    
    #-----------------------------------------------

    #-----Create button options for user-----
    browse_button = Button(options_frame, text = "Browse books", 
                          command = lambda:
                        [messagebox.showinfo("Confirmed","Book browing selected"), LE.delete_all_widgets(app_details[1]), catalogue_screen()])
    browse_button.pack(side = TOP, pady = 10)

    manage_button = Button(options_frame, text = "Manage books", 
                           command = lambda:
                            [messagebox.showinfo("Confirmed","Book managing selected"), LE.delete_all_widgets(app_details[1]), actions_menu()])
    manage_button.pack(side = TOP, pady = 10)
    #----------------------------------------

    LE.font_all_widgets(options_frame, ("Helvetica", 25))

# Procedure to display the reservations types to librarian
def actions_menu():
    #-----Create frames-----
    top_frame = Frame(app_details[1], bg = "beige")
    top_frame.pack(fill=X)

    options_frame = Frame(app_details[1], bg = "beige")
    options_frame.pack(fill=X)
    #-----------------------

    return_button = Button(top_frame, text = "Return", 
                          command = lambda:
                          [LE.delete_all_widgets(app_details[1]), librarian_menu()])
    return_button.pack(side = LEFT)

    title_label = Label(top_frame, text="Please select an option:\t")
    title_label.pack(side=TOP, anchor=N)
    title_label.config(bg = "beige")

    #-----Button options for the libraian-----
    to_prepare_button = Button(options_frame, text = "View reservations to prepare",
                              command = lambda: 
                              [LE.delete_all_widgets(app_details[1]), to_prepare()])
    to_prepare_button.pack(pady = 5)
    
    due_books_button = Button(options_frame, text = "View due reservations",
                              command = lambda: 
                              [LE.delete_all_widgets(app_details[1]), due_reserves()])
    due_books_button.pack(pady = 5)
    
    overdue_button = Button(options_frame, text = "View overdue reservations",
                            command = lambda: 
                            [LE.delete_all_widgets(app_details[1]), overdue_reservations()])
    overdue_button.pack(pady = 5)
    #-----------------------------------------

    LE.font_all_widgets(top_frame, ("Helvetica", 30))
    title_label.config(font = ("Helvetica", 30, "bold"))
    LE.font_all_widgets(options_frame, ("Helvetica", 25))

# Procedure to display details of reservations to prepare
def to_prepare():
    # Get reservations with status "Reserved" from the database
    result = LQ.query_select(LQ.SQ8, ("Reserved",), app_details)

    # Create the top frame for navigation
    top_frame = Frame(app_details[1])
    top_frame.pack(fill=X)

    # Create the frame to display reservations
    reservations_frame = Frame(app_details[1])
    reservations_frame.pack()

    # Set the background color of the entire window
    LE.colour_all_widgets(app_details[1], "beige")

    # Create a button to return to the previous menu
    return_button = Button(top_frame, text="Return",
                           command=lambda: [LE.delete_all_widgets(app_details[1]),
                                           actions_menu()])
    return_button.pack(side=LEFT)

    # Create a label to display the title
    title_label = Label(top_frame, text="Here are all the reservations which are to be prepared:")
    title_label.pack(side=TOP)
    title_label.config(bg="beige")

    # Set the font for the title and other widgets
    LE.font_all_widgets(top_frame, ("Helvetica", 30))
    LE.font_all_widgets(reservations_frame, ("Helvetica", 25))

    # Bolden the title label
    title_label.config(font=("Helvetica", 30, "bold"))

    # Check if there are any reservations
    if len(result) != 0:
        # Iterate through each reservation
        for i in range(len(result)):
            username = result[i][0]
            first_name = result[i][1]
            reservation_id = result[i][2]
            num_of_books = result[i][3]

            # Construct the text to display for each reservation
            text_display = "Username: " + str(username) + "\t\tFirst name: " + str(first_name) + "\nReservation ID: " + str(reservation_id) + "\t\tNumber of books: " + str(num_of_books)

            # Create a button for each reservation with a callback to prepare_books
            reservation_button = Button(reservations_frame, text=text_display,
                                        command=lambda ID=reservation_id:
                                        [LE.delete_all_widgets(app_details[1]), prepare_books(ID)])
            reservation_button.pack(side=TOP, pady=5)
            reservation_button.config(font=("Helvetica", 25))
    else:
        # Display a message if there are no reservations
        LE.no_results_res(reservations_frame)


# Procedure to display books to prepare
def prepare_books(reservation_id):
    # Get reserved books and reservation date/time from the database
    values = (reservation_id, "Reserved")
    reserved_books = LQ.query_select(LQ.SQ9A, values, app_details)
    date_time_order = LQ.query_select(LQ.SQ9B, (reservation_id,), app_details)

    #-----Create frames-----
    top_frame = Frame(app_details[1])
    top_frame.pack(fill=X)

    books_frame = Frame(app_details[1])
    books_frame.pack()

    time_frame = Frame(top_frame)
    time_frame.pack(side=RIGHT)
    #-----------------------

    # Set the background color of the entire window
    LE.colour_all_widgets(app_details[1], "beige")

    # Display reservation date and time
    date_label = Label(time_frame, text="Date of reservation: " + LE.convert_date(date_time_order[0][0]))
    date_label.pack()

    time_label = Label(time_frame, text="Time of reservation: " + str(date_time_order[0][1]))
    time_label.pack()

    # Set background color for frames
    LE.colour_all_widgets(top_frame, "beige")
    LE.colour_all_widgets(time_frame, "beige")

    # Create a button to return to the previous menu
    return_button = Button(top_frame, text="Return",
                           command=lambda: [LE.delete_all_widgets(app_details[1]), to_prepare()])
    return_button.pack(side=LEFT)
    return_button.config(font=("Helvetica", 30))

    # Display reserved books and options to change status
    for i in range(len(reserved_books)):
        current_frame = Frame(books_frame, bg="beige")
        current_frame.pack()

        isbn = reserved_books[i][0]
        genre = reserved_books[i][3]
        title = LE.wrap_text(LE.title_combine(reserved_books[i][1], reserved_books[i][2]), 35)

        # Construct text to display for each reserved book
        text_display = "ISBN: " + str(isbn) + "\tGenre: " + str(genre) + "\nTitle: " + str(title)
        book_label = Label(current_frame, text=text_display, bg="beige")
        book_label.pack(pady=5, side=LEFT)

        # Button to change book status to "Taken out"
        change_button = Button(current_frame, text="Change to Taken out",
                               command=lambda search=(isbn,), book_frame=current_frame: [messagebox.showinfo("Confirmed", "Book changed to Taken out"),
                                                               book_frame.destroy(),
                                                               LQ.query_update(LQ.UQ3, search, app_details)])
        change_button.pack(side=RIGHT)

        LE.font_all_widgets(current_frame, ("Helvetica", 25))

    LE.font_all_widgets(time_frame, ("Helvetica", 30))


# Procedure to display taken out reservations    
def due_reserves():
    #-----Create frames-----
    top_frame = Frame(app_details[1])
    top_frame.pack(fill=X)

    reservations_frame = Frame(app_details[1])
    reservations_frame.pack()
    #-----------------------

    # Set the background color of the entire window
    LE.colour_all_widgets(app_details[1], "beige")

    # Create a button to return to the previous menu
    return_button = Button(top_frame, text="Return",
                           command=lambda: [LE.delete_all_widgets(app_details[1]),
                                           actions_menu()])
    return_button.pack(side=LEFT)

    # Create a label to display the title
    title_label = Label(top_frame, text="Here are all the reservations which are currently 'Taken out'", bg="beige")
    title_label.pack(side=TOP)

    # Get reservations with status "Taken out" from the database
    result = LQ.query_select(LQ.SQ8, ("Taken out",), app_details)

    # Check if there are any reservations
    if len(result) != 0:
        # Iterate through each reservation
        for i in range(len(result)):
            username = result[i][0]
            first_name = result[i][1]
            reservation_id = result[i][2]
            num_of_books = result[i][3]

            # Construct the text to display for each reservation
            text_display = "Username: " + str(username) + "\t\tFirst name: " + str(first_name) + "\nReservation ID: " + str(reservation_id) + "\t\tNumber of books: " + str(num_of_books)

            # Create a button for each reservation with a callback to due_books
            reservation_button = Button(reservations_frame, text=text_display,
                                        command=lambda ID=reservation_id: [LE.delete_all_widgets(app_details[1]), due_books(ID)])
            reservation_button.pack(side=TOP)
            reservation_button.config(font=("Helvetica", 25))
    else:
        # Display a message if there are no reservations
        LE.no_results_res(reservations_frame)

    LE.font_all_widgets(top_frame, ("Helvetica", 30))
    title_label.config(font=("Helvetica", 30, "bold"))

    LE.colour_all_widgets(app_details[1], "beige")


# Procedure to display taken out books
def due_books(ID):
    # Get books with status "Taken out" for the given reservation ID
    values = (ID, "Taken out")
    books = LQ.query_select(LQ.SQ9A, values, app_details)

    # Get reservation date and time
    date_time = LQ.query_select(LQ.SQ9B, (ID,), app_details)

    #-----Create frames------
    top_frame = Frame(app_details[1])
    top_frame.pack(fill=X)

    taken_frame = Frame(app_details[1])
    taken_frame.pack()
    #------------------------

    # Set the background color of the entire window
    LE.colour_all_widgets(app_details[1], "beige")

    # Create a frame for displaying reservation date and time
    time_frame = Frame(top_frame, bg="beige")
    time_frame.pack(side=RIGHT)

    # Create a button to return to the previous menu
    return_button = Button(top_frame, text="Return",
                           command=lambda: [LE.delete_all_widgets(app_details[1]), due_reserves()])
    return_button.pack(side=LEFT)

    # Display reservation date and time
    date_label = Label(time_frame, text="Date of reservation: " + str(LE.convert_date(date_time[0][0])))
    date_label.pack()

    time_label = Label(time_frame, text="Time of reservation: " + str(date_time[0][1]))
    time_label.pack()

    LE.colour_all_widgets(time_frame, "beige")

    # Set font for the return button
    return_button.config(font=("Helvetica", 30))

    # Set font for the time frame
    LE.font_all_widgets(time_frame, ("Helvetica", 30))

    # Display taken out books and options to change status
    for i in range(len(books)):
        current_frame = Frame(taken_frame, bg="beige")
        current_frame.pack()

        isbn = books[i][0]
        genre = books[i][3]
        title = LE.wrap_text(LE.title_combine(books[i][1], books[i][2]), 35)

        # Construct text to display for each taken out book
        text_display = "ISBN: " + str(isbn) + "\tGenre: " + str(genre) + "\nTitle: " + str(title)
        book_label = Label(current_frame, text=text_display, bg="beige")
        book_label.pack(side=LEFT)

        # Button to change book status to "Available"
        available_button = Button(current_frame, text="Change to available",
                                  command=lambda Isbn=isbn, FRAME=current_frame:
                                  [messagebox.showinfo("Confirmed", "Book made available"), FRAME.destroy(),
                                   LQ.query_update(LQ.UQ4, (Isbn,), app_details)])
        available_button.pack(side=RIGHT)

        LE.font_all_widgets(current_frame, ("Helvetica", 30))

# Procedure to display overdue users and how many books they have
def overdue_reservations():
    #-----Create frames-----
    top_frame = Frame(app_details[1])
    top_frame.pack(fill=X)

    overdue_frame = Frame(app_details[1])
    overdue_frame.pack()
    #-----------------------

    # Set the background color of the entire window
    LE.colour_all_widgets(app_details[1], "beige")

    # Create a button to return to the previous menu
    return_button = Button(top_frame, text="Return",
                           command=lambda: [LE.delete_all_widgets(app_details[1]),
                                           actions_menu()])
    return_button.pack(side=LEFT)

    # Get overdue reservations from the database
    result = LQ.query_select(LQ.SQ10, None, app_details)

    # Create a label to display the title
    title_label = Label(top_frame, text="Here are users and how many overdue books they have:", bg="beige")
    title_label.pack(side=TOP)

    # Set font for labels
    LE.font_all_widgets(top_frame, ("Helvetica", 30))
    title_label.config(font=("Helvetica", 30, "bold"))

    # Check if there are any overdue reservations
    if len(result) != 0:
        # Iterate through each result
        for i in range(len(result)):
            username = result[i][0]
            overdue_books_count = result[i][1]

            # Construct text to display for each user
            text_display = "Username: " + username + "\tNumber of overdue books: " + str(overdue_books_count) + "\n\tClick to view books"

            # Create a button for each user with a callback to overdue_books
            book_button = Button(overdue_frame, text=text_display,
                                 command=lambda c_username=(username,): [LE.delete_all_widgets(app_details[1]), overdue_books(c_username)])
            book_button.pack(side=TOP, pady=5)
            
            # Set font for labels in the overdue_frame
            LE.font_all_widgets(overdue_frame, ("Helvetica", 25))
    else:
        result_label = Label(overdue_frame, text = "There are no users with overdue books", bg = "beige")
        result_label.pack()
        result_label.config(font = ("Helvetica",25))


# Procedure to display all overdue books of a specific user
def overdue_books(c_username):
    #-----Create frames-----
    top_frame = Frame(app_details[1])
    top_frame.pack(fill=X)

    overdue_frame = Frame(app_details[1])
    overdue_frame.pack()
    #-----------------------

    # Set the background color of the entire window
    LE.colour_all_widgets(app_details[1], "beige")

    # Create a button to return to the previous menu
    return_button = Button(top_frame, text="Return",
                           command=lambda: [LE.delete_all_widgets(app_details[1]), overdue_reservations()])
    return_button.pack(side=LEFT)

    # Set font for labels in the top frame
    LE.font_all_widgets(top_frame, ("Helvetica", 30))

    # Get overdue books for the given username from the database
    result = LQ.query_select(LQ.SQ11, c_username, app_details)

    # Iterate through each overdue book
    for i in range(len(result)):
        current_frame = Frame(overdue_frame, bg="beige")
        current_frame.pack()

        isbn = result[i][0]
        title = LE.title_combine(result[i][1], result[i][2])
        due_date = result[i][3]

        # Construct text to display for each overdue book
        text_display = "ISBN: " + isbn + "\tTitle: " + title + "\nDue date: " + str(due_date) + "\nClick to make available"

        # Create a button for each overdue book with a callback to make_available
        book_button = Button(current_frame, text=text_display,
                             command=lambda ISBN=(isbn,), current=current_frame:
                             [messagebox.showinfo("Confirmed", "Book status changed"), current.destroy(),
                              LQ.query_update(LQ.UQ4, ISBN, app_details)])
        book_button.pack(side=TOP, pady=5)

        LE.font_all_widgets(current_frame, ("Helvetica", 25))


# Call main procedure
main()
