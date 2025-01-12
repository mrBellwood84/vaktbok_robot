CREATE TABLE Employee
(
	id VARCHAR(36) PRIMARY KEY NOT NULL,
    name VARCHAR(200) UNIQUE NOT NULL
);

CREATE TABLE Workday
(
	id VARCHAR(36) PRIMARY KEY NOT NULL,
    year INT NOT NULL,
    weeknumber INT NOT NULL,
    weekday INT NOT NULL,
    date VARCHAR(10) UNIQUE NOT NULL
);

CREATE TABLE ShiftCode
(
	id VARCHAR(36) PRIMARY KEY NOT NULL,
    code VARCHAR(50),
    start VARCHAR(10),
    end VARCHAR(10)
);

CREATE TABLE Shift
(
	id VARCHAR(36) PRIMARY KEY NOT NULL,
    employee_id VARCHAR(36) NOT NULL,
    workday_id VARCHAR(36) NOT NULL,
    shiftcode_id VARCHAR(36) NOT NULL,
    timestamp DATETIME,
	
    FOREIGN KEY (employee_id) REFERENCES Employee(id),
    FOREIGN KEY (workday_id) REFERENCES Workday(id),
    FOREIGN KEY (shiftcode_id) REFERENCES ShiftCode(id)
);