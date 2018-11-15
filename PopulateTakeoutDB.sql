-- this is a test sql to populate the TAKEOUT database

INSERT INTO Account
(AccountType, 		AccountPassword)
VALUES
('User', 			'123456'),
('User', 			'123456'),
('User', 			'654321'),
('User', 			'110110'),
('Rest',			'abcabc'),#1
('Rest',			'abcabc'),#2
('Rest',			'abcabc'),#3
('Rest',			'abcabc'),#4
('Rest',			'abcabc'),#5
('Rest',			'abcabc'),#6
('Rest',			'abcabc'),#7
('Rest',			'abcabc'),#8
('Rest',			'abcabc'),#9
('Rider',			'zxczxc'),#1
('Rider',			'zxczxc'),#2
('Rider',			'zxczxc'),#3
('Rider',			'zxczxc'),#4
('Rider',			'zxczxc'),#5
('Rider',			'zxczxc'),#6
('Rider',			'zxczxc'),#7
('Rider',			'zxczxc');#8


# populate the Users table
INSERT INTO Users
(UserName,			AccountID,			UserTel)
VALUES
('Zhang Zhiming',	1,		'15201770060'),
('Yu Chunjiao',		2,		'15201770161'),
('Zhi Zunbao',		3,		'15201770262'),
('Zi Xia',			4,		'15201770363');

# populate the Loc table
INSERT INTO Loc
(UserID,	LocString,			LocX,		LocY)
VALUES
(1,			'D7-401',			121.38,		31.12),
(2,			'D7-402',			121.38,		31.12),
(3,			'D8-502',			121.38,		31.12),
(4,			'SEIEE-2-202',		121.38,		31.12);	# 1 longitude = 111 km

# populate the Rest table
INSERT INTO Rest
(RestName,		RestTel,		LocX,		LocY,		AccountID)
VALUES
('KFC',			'4008823823',	121.00,		31.00,		5),
('McDonald',	'4008517517',	121.50,		31.10,		6),
('StarBucks',	'4008077895',	121.60,		31.15,		7),
('Costa Coffee','4008130999',	121.15,		31.13,		8),
('PizzaHut',	'4008123123',	120.88,		31.45,		9),
('BurgerKing',	'4008988788',	121.05,		30.98,		10),
('Dicos',		'4006639797',	120.95,		31.60,		11),
('YOSHINOYA',	'4008197197',	121.44,		30.80,		12),
('Christine',	'4008205000',	121.30,		31.00,		13);

# populate the Course table
INSERT INTO Course
(CourseName,		RestID,		Price)
VALUES
('Hamburger',		1,			15),
('French Fries',	1,			12),
('Hamburger',		2,			18),
('Chicken',			2,			14),
('Coffee',			3,			28),
('Tiramisu',		3,			18),
('Coffee',			4,			25),
('Chocolate Cake',	4,			22),
('Pizza',			5,			38),
('Orange Juice',	5,			10),
('Hamburger',		6,			35),
('Coke',			6,			8),
('Hamburger',		7,			16),
('Red Tea',			7,			11),
('Takoyaki',		8,			12),
('Miso Soup',		8,			9),
('Sandwich',		9,			16.5),
('Cheese',			9,			15);

# populate the Riders table
INSERT INTO Rider
(RiderName,		RiderTel,		AccountID)
VALUES
('Senna',		'15201770464',	14),
('Schumacher',	'15201770565',  15),
('Hamilton',	'15201770666',	16),
('Alonso',		'15201770767',	17),
('Raikkonen',	'15201770868',	18),
('Massa',		'15201770969',	19),
('Weber',		'15201770050',	20),
('Vettel',		'15201770040',	21);

# populate the Orders table
# insert when a new order is placed

# populate the OrderCourse table
# insert when a new order is placed

# populate the RestRider table
INSERT INTO RestRider
(RestID,		RiderID)
SELECT	RestID,	RiderID
FROM 	Rest,	Rider;


