### DB structure

Following structure follows QuickDBD chart syntax. You may insert the syntax to https://app.quickdatabasediagrams.com/#/ (select free trial) to visually view the DB chart

account
-
userID PK string #email
firstName string
lastName string
password string
admin boolean, #1 thesis supervisor, 0 system admin
departmentID string FK >- department.departmentID
createdOn datetime
modifiedOn datetime

thesis
-
thesisID PK string
userID string FK >- account.userID
title string
description string
level int # 0    BSc., 1 MSc. thesis
author string
status int #0 available, 1 in progress, 2 completed
createdOn datetime #date when entered as available thesis
reservedOn datetime #date when reserved for a student
completedOn datetime #date when submitted/graded, finalization date
modifiedOn datetime

department
-
departmentID PK int
name string
createdOn datetime
modifiedOn datetime

science
-
scienceID PK int
name string
createdOn datetime
modifiedOn datetime

science2thesis
-
thesisID int FK >- thesis.thesisID
scienceID int FK >- science.scienceID