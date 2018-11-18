-- this is a test sql for the takeout mission

DROP DATABASE IF EXISTS TAKEOUT;
CREATE DATABASE TAKEOUT;

USE TAKEOUT;

CREATE TABLE Account
(
	AccountID SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	AccountType VARCHAR(20) NOT NULL CHECK(AccountType='User' or AccountType='Rest' or AccountType='Rider'),
	AccountPassword VARCHAR(20) NOT NULL
)ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

-- users table
CREATE TABLE Users
(
	UserID 			SMALLINT		UNSIGNED	NOT NULL	AUTO_INCREMENT,
    UserName		VARCHAR(20)		NOT NULL,
    AccountID       SMALLINT        UNSIGNED    NOT NULL,
    UserTel			VARCHAR(15)		NOT NULL,
    UserLoginTime	SMALLINT		NOT NULL	DEFAULT 0,
    PRIMARY KEY	(UserID),
    FOREIGN KEY (AccountID) 		REFERENCES Account(AccountID)
)ENGINE=InnoDB	AUTO_INCREMENT=0	DEFAULT CHARSET=utf8;

-- the Location of restuarants
CREATE TABLE Loc
(
    LocIdx		SMALLINT		UNSIGNED	NOT NULL	AUTO_INCREMENT,
    UserID		SMALLINT		UNSIGNED	NOT NULL,
    LocString	VARCHAR(80)		NOT NULL,
    LocX		DECIMAL(5,2)	NOT NULL,	# longitude
    LocY		DECIMAL(4,2)	NOT NULL,	# altitude	# may calculate the freights
    PRIMARY KEY	(LocIdx),
    FOREIGN KEY	(UserID)	REFERENCES 	Users(UserID) 	ON DELETE CASCADE	ON UPDATE CASCADE
)ENGINE=InnoDB	AUTO_INCREMENT=0	DEFAULT CHARSET=utf8;

-- restuarants table
CREATE TABLE Rest
(
	RestID		SMALLINT		UNSIGNED	NOT NULL	AUTO_INCREMENT,
    RestName	VARCHAR(20)		NOT NULL,
    RestTel		VARCHAR(15)		NOT NULL,
    Score		DECIMAL(2,1)	NULL		DEFAULT 4.0,		# check
    LocX		DECIMAL(5,2)	NOT NULL,	# longitude
    LocY		DECIMAL(4,2)	NOT NULL,	# altitude	# may calculate the freights
    AccountID   SMALLINT  		UNSIGNED 	NOT NULL,
    PRIMARY KEY	(RestID),
    FOREIGN KEY (AccountID) REFERENCES Account(AccountID)
)ENGINE=InnoDB	AUTO_INCREMENT=0	DEFAULT CHARSET=utf8;

-- courses for each restuarant
CREATE TABLE Course
(
	CourseID	SMALLINT		UNSIGNED	NOT NULL	AUTO_INCREMENT,
    CourseName	VARCHAR(20)		NOT NULL,
    RestID		SMALLINT 		UNSIGNED	NOT NULL,
    Price		DECIMAL(5,2)	NOT NULL,
    Score		DECIMAL(2,1)	NOT NULL	DEFAULT 4.0,
    Photo		VARCHAR(50)		NULL, 		# record the path of the photos, if not uploaded, a fixed pic could be used
#	Dicount		DECIMAL(2,2)	NOT NULL	DEFAULT 0,	# actual price = Price * (1-Discount)
    PRIMARY KEY	(CourseID),
    FOREIGN KEY	(RestID)	REFERENCES 	Rest(RestID) 	ON DELETE CASCADE	ON UPDATE CASCADE
)ENGINE=InnoDB	AUTO_INCREMENT=0	DEFAULT CHARSET=utf8;

-- rider table
CREATE TABLE Rider
(
	RiderID		SMALLINT		UNSIGNED	NOT NULL	AUTO_INCREMENT,
    RiderName	VARCHAR(10)		NOT NULL,
    RiderTel	VARCHAR(15)		NOT NULL,
    Score		DECIMAL(2,1)	NOT NULL	DEFAULT 4.0,
    AccountID   SMALLINT		UNSIGNED    NOT NULL,
    FOREIGN KEY (AccountID) REFERENCES Account(AccountID),
    PRIMARY KEY	(RiderID)
)ENGINE=InnoDB	AUTO_INCREMENT=0	DEFAULT CHARSET=utf8;

-- orders table
CREATE TABLE Orders
(
	OrderID		INT				UNSIGNED	NOT NULL	AUTO_INCREMENT,
    UserID		SMALLINT		UNSIGNED	NOT NULL,
    RestID		SMALLINT		UNSIGNED	NOT NULL,
    State		INT				UNSIGNED	DEFAULT 0,	# if the order is completed
    # state:	0:order placed	1:rest confirm	2:rider delivering	3:user received
    RiderID		SMALLINT		UNSIGNED	NULL,
    #RiderState	BOOL			NOT NULL	DEFAULT FALSE,	# if a rider is assigned to this order
    OrderTime	TIMESTAMP 		NOT NULL 	DEFAULT 	CURRENT_TIMESTAMP 	ON UPDATE CURRENT_TIMESTAMP,	# not sure
    ScoreRest	DECIMAL(2,1)	UNSIGNED	NULL,
    ScoreRider	DECIMAL(2,1)	UNSIGNED	NULL,
    CommentTxt	TEXT			NULL,
    PRIMARY KEY	(OrderID),
    FOREIGN KEY (UserID)	REFERENCES UserS(UserID) 	ON DELETE CASCADE	ON UPDATE CASCADE,
    FOREIGN KEY (RestID)	REFERENCES Rest(RestID) 	ON DELETE CASCADE	ON UPDATE CASCADE,
    FOREIGN KEY (RiderID)	REFERENCES Rider(RiderID) 	ON DELETE CASCADE	ON UPDATE CASCADE
)ENGINE=InnoDB	AUTO_INCREMENT=0	DEFAULT CHARSET=utf8;

-- the 1:n relationship between orders and courses
CREATE TABLE OrderCourse
(
	OrderID		INT 			UNSIGNED	NOT NULL,
    CourseID	SMALLINT		UNSIGNED	NOT NULL,
    Num			INT 			UNSIGNED 	NOT NULL,
    PRIMARY KEY (OrderID,CourseID),
	FOREIGN KEY (OrderID)	REFERENCES Orders(OrderID) 	ON DELETE CASCADE	ON UPDATE CASCADE,
    FOREIGN KEY (CourseID)	REFERENCES Course(CourseID)	ON DELETE CASCADE	ON UPDATE CASCADE
)ENGINE=InnoDB	DEFAULT CHARSET=utf8;

-- the n:n relationship between restuarants and riders
CREATE TABLE RestRider
(
	RestID		SMALLINT		UNSIGNED	NOT NULL,
    RiderID		SMALLINT		UNSIGNED	NOT NULL,
    PRIMARY KEY (RestID,RiderID),
    FOREIGN KEY (RestID)	REFERENCES Rest(RestID) 	ON DELETE CASCADE	ON UPDATE CASCADE,
    FOREIGN KEY (RiderID)	REFERENCES Rider(RiderID) 	ON DELETE CASCADE	ON UPDATE CASCADE
)ENGINE=InnoDB	DEFAULT CHARSET=utf8;


