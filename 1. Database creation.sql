CREATE SCHEMA library_main_test;

CREATE TABLE Authors(
	authorID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	firstName VARCHAR(30) NOT NULL,
    surname VARCHAR(30)
);


CREATE TABLE Books(
	ISBN VARCHAR(13) NOT NULL, 
    authorID INT NOT NULL,
    title VARCHAR(45) NOT NULL,
    subTitle VARCHAR(30),
    bookStatus VARCHAR(9) NOT NULL,
    starRating DECIMAL(3,2),
    genre VARCHAR(15) NOT NULL,
    blurb VARCHAR(1000),
    datePublished DATE NOT NULL,
    PRIMARY KEY (ISBN),
    FOREIGN KEY(authorID) REFERENCES Authors(authorID),
    CHECK(length(ISBN)=13),
    CHECK(bookStatus IN("Available","Reserved","Taken out","Overdue")),
    CHECK(starRating BETWEEN 0 AND 5),
	CHECK(genre IN("Non-fiction","Fantasy","Science fiction","Romance","Horror"))
);

CREATE TABLE Users(
	username VARCHAR(20) NOT NULL,
    firstName VARCHAR(30) NOT NULL,
    surname VARCHAR(30) NOT NULL,
    passwordHash VARCHAR(64) NOT NULL,
    librarian BOOLEAN NOT NULL,
    PRIMARY KEY(username),
    CHECK(LENGTH(username) >= 10  and LENGTH(username) <=20),
    CHECK(LENGTH(passwordHash) = 64)
);

CREATE TABLE Reservations(
	reservationID INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL,
    dateOfOrder DATE NOT NULL,
    timeOfOrder TIME NOT NULL,
    dueDate DATE NOT NULL,
    PRIMARY KEY(reservationID),
    FOREIGN KEY(username) REFERENCES Users(username)
);

CREATE TABLE bookReservation(
	reservationID INT NOT NULL,
    ISBN VARCHAR(13) NOT NULL,
    PRIMARY KEY (reservationID, ISBN),
    FOREIGN KEY(reservationID) REFERENCES Reservations(reservationID),
    FOREIGN KEY(ISBN) REFERENCES Books(ISBN)
);



