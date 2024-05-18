#Book & Borrow system queries
#Daniel Monaghan

# XQYA
#X - Query type (S for SELECT, U for UPDATE, I for INSERT)
#Q - Indicates query
#Y - ID number (1,2,3,4 etc.)
#A - A, B, C (A is main query, B will be a smaller query near it)

import Library_Extras as LE
import mysql.connector

# Function to connect to the database and return a connection variable
def db_connect():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user="root",
            passwd="Steamgame101.",
            database="library_end_user",
        )
    except:
        return None
    else:
        return conn

# Function for SELECT queies
def query_select(query, values, app_details):
    my_cursor = app_details[0].cursor()

    try:
        my_cursor.execute(query, values)
    except:
        LE.error_screen(app_details)
    else:
        my_result = my_cursor.fetchall()
        return my_result

# Procedure for INSERT queries
def query_insert(query, values, app_details):
    my_cursor = app_details[0].cursor()

    try:
        my_cursor.execute(query, values)
    except:
        LE.error_screen(app_details)
    else:
        app_details[0].commit()

# Procedure for UPDATE queries
def query_update(query, values, app_details):
    my_cursor = app_details[0].cursor()

    try:
        my_cursor.execute(query, values)
    except:
        LE.error_screen(app_details)
    else:
        app_details[0].commit()


#-----SELECT queries-----
# Get all the ISBNs and DUe dates of Taken out books
SQ1 = """SELECT B.ISBN, R.dueDate
         FROM books AS B, bookreservation AS bR, reservations AS R
         WHERE B.ISBN = bR.ISBN
         AND bR.reservationID = R.reservationID
         AND B.bookStatus='Taken out'"""

# Get the user details and order them ascending (case sensitive)
SQ2 = """SELECT username, passwordHash, librarian
         FROM users
         ORDER BY BINARY username ASC"""

# Get all the usernames and order them ascending (case sensitive)
SQ3 = """SELECT username
         FROM users
         ORDER BY BINARY username ASC"""

# All available books, no filter
SQ4A = """SELECT ISBN, title, subTitle, genre, firstName, surname 
          FROM books, authors 
          WHERE books.authorID = authors.authorID
          AND bookStatus="Available" 
          ORDER BY title ASC"""

# All available books, filtered by a [SPECIFIED] genre
SQ4B = """SELECT ISBN, title, subTitle, genre, firstName, surname
          FROM books, authors
          WHERE books.authorID = authors.authorID
          AND bookStatus="Available"
          AND genre=%s
          ORDER BY title ASC"""

# Get all the details of a [SPECIFIED] book
SQ5 = """SELECT ISBN, title, subTitle, firstName, surname, genre, starRating, datePublished, blurb 
         FROM books AS B, authors AS A 
         WHERE B.authorID = A.authorID 
         AND ISBN = %s"""

# Get the title of a book using a [SPECIFIED] ISBN (for the Cart screen)
SQ6 = """SELECT title, subTitle
         FROM books
         WHERE ISBN = %s"""

# GEt the reservation ID of the newly made reservations
SQ7 = """SELECT reservationID
         FROM reservations
         WHERE username = %s
         AND dateOfOrder = %s
         AND timeOfOrder = %s"""

# Get all the reservations which have a [Reserved or Taken out] books in them
SQ8 = """SELECT u.username, u.firstName, r.reservationID, COUNT(br.ISBN)
         FROM Users u, Reservations r,bookReservation br
         WHERE u.username = r.username 
         AND r.reservationID = br.reservationID
         AND br.ISBN IN (SELECT ISBN 
                         FROM Books 
                         WHERE bookStatus = %s)
         GROUP BY u.username, u.firstName, r.reservationID"""

# Get the book details of [SPECIFIED] ID and the [SPECIFIED] book status
SQ9A = """SELECT B.ISBN, B.title, B.subTitle, B.genre
            FROM books as B, reservations as R, bookreservation as BR
            WHERE B.ISBN = BR.ISBN
            AND BR.reservationID = R.reservationID
            AND R.reservationID=%s
            AND bookStatus=%s"""

# Get time and date of reservation
SQ9B = """SELECT dateOfOrder, timeOfOrder
          FROM reservations
          WHERE reservationID = %s"""

# Get username and number of overdue books
SQ10 = """SELECT U.username, COUNT(DISTINCT B.ISBN)
          FROM Users AS U, Reservations AS R, bookReservation as bR, Books as B
          WHERE U.username = R.username
          AND R.reservationID = bR.reservationID
          AND bR.ISBN = B.ISBN
          AND bookStatus = "Overdue"
          GROUP BY U.username"""

# Get all overdue books of a [SPECIFIED] user
SQ11 = """SELECT B.ISBN, title, subTitle, dueDate
          FROM Books as B, bookReservation AS bR, Reservations as R, Users AS U
          WHERE B.ISBN = bR.ISBN
          AND bR.reservationID = R.reservationID
          AND R.username = U.username
          AND bookStatus = "Overdue"
          AND R.username = %s"""
#------------------------

#-----UPDATE queries-----
# Change book status to Overdue
UQ1 = """UPDATE books
         SET bookStatus="Overdue"
         WHERE ISBN=%s"""

# Change book status to Reserved
UQ2 = """UPDATE books
         SET bookStatus="Reserved"
         WHERE ISBN=%s"""

# Change book status to Taken out
UQ3 = """UPDATE books
       SET bookStatus="Taken out"
       WHERE ISBN = %s"""

# Change book status to Avilable
UQ4 = """UPDATE books
       SET bookStatus="Available"
       WHERE ISBN = %s"""
#------------------------

#-----INSERT queries-----
# Make a new user using details from program
IQ1 = """INSERT INTO Users (username, firstName, surname, passwordHash, librarian)
         VALUES(%s, %s, %s, %s, %s)"""

# Make a new reservation using details from the program
IQ2 = """INSERT INTO reservations(username, dateOfOrder, timeOfOrder, dueDate)
         VALUES(%s,%s, %s, %s)"""

# Make a new book reservation using details from the program
IQ3 = """INSERT INTO bookreservation(reservationID, ISBN)
       VALUES(%s, %s)"""






