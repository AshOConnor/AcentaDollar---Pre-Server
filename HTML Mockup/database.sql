CREATE TABLE	users (
	username	VARCHAR(30) NOT NULL,
	user_email	VARCHAR(50) NOT NULL,
	PRIMARY KEY	(user_email)
);

CREATE TABLE	revenue (
	user_email		VARCHAR(10),
	revenue_date	DATE NOT NULL,
	source			VARCHAR (20),
	r_amount		DECIMAL(8,2),
	PRIMARY KEY	(user_email, revenue_date, source, r_amount),
	FOREIGN KEY	(user_email)	REFERENCES	users(user_email)
);

CREATE TABLE	expenses (
	user_email		VARCHAR(10),
	expense_date	DATE NOT NULL,
	description		VARCHAR (30),
	e_amount		DECIMAL(8,2),
	PRIMARY KEY	(user_email, expense_date, description, e_amount),
	FOREIGN KEY	(user_email)	REFERENCES	users(user_email)
);
