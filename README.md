These are the files detailing my Advanced Higher Computing Science Project.

TO RUN: 
 - Create a MySQL database with the provided SQL files
 - Add connection details to the db_connect module of the Library_Queries file
 - Execute the Library_Main file with the mysql connector module installed using PIP.

The project I took on was to make a sort of Amazon book store but for library books. To read more in-depth with my bad Analysis and Designs you can read the full report pdf.

It uses a MySQL database that I just set up on workbench. It doesn't contain links to an online database.
I wasn't sure if I could use an author's names or their book names. So, I made some really bad parody names of the authors and books. 
(I probably could of just used their actual names as this isn't for profit)

The program is written in Python (since it was the only language I knew at the time) and is pretty bad.
There are 3 files:
 - Main: Contains the main procedures of the program. All the screens that show up and all the logic handling.
 - Queries: Contains all the queries and connection to the database. Also contains modules that will execute given queries.
 - Extras: Contains all the extra styling modules for the screens. Also contains all the extra non-screen modules (everything that doesn't fit into the main file).
I'd love to rework this. The main file contains around 1000 lines of code due to the sheer number of screens and repeated code.

Files:
 - Database creation: Contains all the SQL to create the database and the tables to be used.
 - Adding Authors: Contains the SQL to insert all the authors I used
 - Adding Books: Contains the SQL to insert all the books I used
 - Adding Librarians: Contains the SQL to add the librarian users I had.
 - DM AH Project Report: The monstrous 180 page report detailing all phases of development
 - The 3 program files as described above

Librarians:
These are the librarian login details
 - Username: johnAndrews23       Password: agathaAndrews!
 - Username: agathaAndrews23     Password: johnAndrews!
 - Username: maryCampbell53      Password: ILoveBooks!!!
 - Username: janeDoe1279         Password: janeLovesBooks
 - Username: seanMacavoy97       Password: jamesMacavoyCool
The final librarian is one that I can't remember the password for.

Improvements:
 - There are still a large number of errors in the program that I didn't fix before project submission.
 - It's not super efficient or maintainable either
 - The program is procedurally programmed, and I would prefer to try a object-oriented program
 - Features that will improve the usability and experience

Lastly I'd like to say that this probably should be a web app that connects to a backend, and I'm planning on doing that eventually.
