# Use cases

Please read Readme to learn about the application overview

## Use case list

1. Thesis writer (i.e. student / author) use cases

	1.1. Listing theses
	- (All) users may search and view theses by 
	     * scientific area 
		 * by supervisor
		 * by supervisor's department
		 * by availability
	
	1.2. Contacts to thesis supervisors
	- Each thesis discloses supervisor's
	   * email
	   * name
	   * department
	   for contacting regarding the thesis proposal

2. Supervisor use cases
	
	2.1 Registrating to the system
	
	2.2. Authenticating to the system
	- Execution of actions which require authentication and supervisor level authorization
	
	2.3. Entering new theses proposals into the system
	- Adding new thesis proposals by entering:
		* Title and / or description
		* Scientific field(s)
	
	2.4. Reserving a thesis for a student
	- Access the self-created theses for editing
	    * Fill level (MSc. / BSc. thesis)
		* Fill author information
	
	2.5. Finalizing the thesis
	- Changing the status of the thesis to be completed	

3. Administrator use cases
	
	3.1. Authentication to the system
	- Execution of actions which require authentication and administrator level authorization
	
	3.2. Administering the theses
	- User may edit any theses at any time
	- User may delete theses which are in available state
	- User may change the status of any theses at any time
	- User may create theses
	
	3.3. Administering the master data
	- Add/edit/delete users 
	    * Add users
		* Activate registered account
		* Change user details
		* Elevate user permissions
		* Delete irrelevant users
	- Manage departments (add, delete)
	- Manage scientific areas (e.g. Greek Philosophy, Economics, Microeconomics, Mathematics, Econometrics...) (add, delete)

## SQL queries related to the main use cases
1.1 Listing and searching theses
- Listing and ordering alphabetically by thesis title

```sql
SELECT * FROM thesis ORDER BY LOWER(title) asc
```

- Searching by foreign key assiociation (e.g. status)

```sql
SELECT * FROM thesis LEFT JOIN account
ON thesis.userID = account.userID
where account.userID = ? 
```

2.2 Entering new theses into system
- Inserting a new thesis

```sql
INSERT INTO thesis ("createdOn", "modifiedOn", title, description, level, author, status, "completedOn", "reservedOn", "userID") VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?, ?)
```

- Updating / Adding a science associations
```sql
INSERT INTO science2thesis ("thesisID", "scienceID") VALUES (?, ?)
```

2.3 Reserving thesis for a student

```sql
UPDATE thesis SET "modifiedOn"=CURRENT_TIMESTAMP, level=?, author=?, status=?, "reservedOn"=? WHERE thesis."thesisID" = ?
```

2.4 Finalizing the thesis
```sql
UPDATE thesis SET "modifiedOn"=CURRENT_TIMESTAMP, status=?, "completedOn"=? WHERE thesis."thesisID" = ?
```

3.3 Administering the master data (Users)
- Select user to be edited

```sql
SELECT account."createdOn" AS "account_createdOn", account."modifiedOn" AS "account_modifiedOn", account."userID" AS "account_userID", account."firstName" AS "account_firstName", account."lastName" AS "account_lastName", account.password AS account_password, account.admin AS account_admin, account.department AS account_department
FROM account
WHERE account."userID" = ?
```

- Edit the user (e.g. change admin rights)
```sql
UPDATE account SET "modifiedOn"=CURRENT_TIMESTAMP, admin=? WHERE account."userID" = ?
```

- Removing a user
```sql
DELETE FROM account WHERE account."userID" = ?
```

_Aggregate queries are sligtly different based on the SQL (here SQLite)_

- Getting notification about registered users (aggregate query)
```sql
SELECT COUNT(userID) FROM account WHERE inactive
```

- Displaying the number of submitted theses of the supervisor (aggregate query)
```sql
SELECT account.userID, COUNT(thesis.thesisID) FROM account
    LEFT JOIN thesis ON thesis.userID = account.userID
    GROUP BY account.userID
```



**Create table statements**

```sql
CREATE TABLE science (
        "createdOn" DATETIME,
        "modifiedOn" DATETIME,
        "scienceID" INTEGER NOT NULL,
        name VARCHAR(144) NOT NULL,
        PRIMARY KEY ("scienceID")
);

CREATE TABLE department (
        "createdOn" DATETIME,
        "modifiedOn" DATETIME,
        "departmentID" INTEGER NOT NULL,
        name VARCHAR(144) NOT NULL,
        PRIMARY KEY ("departmentID")
);

CREATE TABLE account (
        "createdOn" DATETIME,
        "modifiedOn" DATETIME,
        "userID" VARCHAR(100) NOT NULL,
        "firstName" VARCHAR(144) NOT NULL,
        "lastName" VARCHAR(144) NOT NULL,
        password VARCHAR(144) NOT NULL,
        admin INTEGER,
        inactive BOOLEAN,
        department INTEGER,
        PRIMARY KEY ("userID"),
        CHECK (inactive IN (0, 1)),
        FOREIGN KEY(department) REFERENCES department ("departmentID")
);

CREATE TABLE thesis (
        "createdOn" DATETIME,
        "modifiedOn" DATETIME,
        "thesisID" INTEGER NOT NULL,
        title VARCHAR(144) NOT NULL,
        description VARCHAR(500) NOT NULL,
        level BOOLEAN,
        author VARCHAR(144),
        status INTEGER,
        "completedOn" DATETIME,
        "reservedOn" DATETIME,
        "userID" VARCHAR NOT NULL,
        PRIMARY KEY ("thesisID"),
        CHECK (level IN (0, 1)),
        FOREIGN KEY("userID") REFERENCES account ("userID")
);

CREATE TABLE science2thesis (
        "thesisID" INTEGER,
        "scienceID" INTEGER,
        FOREIGN KEY("thesisID") REFERENCES thesis ("thesisID"),
        FOREIGN KEY("scienceID") REFERENCES science ("scienceID")
);
```