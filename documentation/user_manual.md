# Thesis finder - User manual

Application can be used at <https://morning-garden-53294.herokuapp.com/>. Application may be also installed locally (view installation_guide.md)

The purpose of the application is to connect a thesis writer to an idea and to supervisor. A student preparing to write a thesis may browse and search through the library of thesis topics and ideas provided by the supervisors.

## Site structure 

**Landing page**
User is directed to a landing page. Landing page guides user to navigate to the 'Thesis list' through 'Find thesis' button. If the user has credentials, the user may also login to access authorized content of the application.

**Deeper levels**
Deeper levels consist of navigation pane and action dependent content.  

## Login

Application and the thesis topics may be accessed without registering. Students are expected to browse and search the theses without system credentials.

Theses supervisors and system administrators can access the authorized content by logging in to the system. Authorized content of the application may be accessed (in Heroku) with the following credentials

| Username		   | Password   | User role		|
| ---------------- | ---------- | ------------- |
| admin@gmail.com  | test       | admin         |
| test@gmail.com   | test       | supervisor    |

User with system administrator access rights may create users (see 'Master data management - Users)

User may log in to the system through landing page by pressing 'Login' button. Alternatively, user browsing the deeper levels of the application may login through the navigation pane in by pressing 'Login' button.

After pressing the 'Login' button user is redirected to a login page which requests user to enter their user name and password.

After a successful login, the logged in user and role are displayed to the user. User is redirected to the previous page.

## Logout

User who has logged in to the application may log out through landing page by pressing 'Logout' button. Alternatively, user browsing the deeper levels of the application may log out through the navigation pane by pressing 'Logout' button.

Logout returns the user to the landing page.

## Registering

Supervisor may register to the system. Pressing 'Register' in the landing page opens a registration form. All fields need to be filled. After registration login is possible only after an admin user has verified the account information and activated the user account.

If user tries to login without active account, error will be displayed. User should contact administrator to have the account activated. 

## Thesis list

'Thesis list' may be accessed with or without authentication. The user role determines the shown content.

Thesis list is comprised of the following content
1. Thesis
    * Title
	* Description (click 'Description' button to display the description')
2. Supervisor
3. Email (of the supervisor)
4. Department (of the supervisor)
5. Level
    * Determined after the thesis has been checked out for an author
6. Author
7. Sciences
8. Status
9. Created
10. Reserved
11. Completed
12. Action links (authorization required)

**Browsing**
User may browse the list of submitted theses. List of theses displays ten theses topics ordered alphabetically by the thesis title. User may browse all the submitted theses by navigating between the pages on the bottom of the table.

User may also change the ordering of the theses by any of the table column headers. Theses may be sorted by column header either in ascending or descending order. Sorting is cleared when the page is refreshed. _Note!_ Sorting only applies on the selected page.

**Search**
Sliding search side menu can be displayed by pressing search link on the top right side of the thesis list. Search menu may be closed by pressing the closing 'X' link in the menu. 

User may search the submitted theses by selecting desired search criteria
1. Science (contains all sciences in the system)
2. Supervisor (contains Supervisors who have submitted a thesis topic)
3. Department (contains all departments in the system)
4. Status

After selecting the desired criteria, user may execute the search by clicking 'Search' button. Search may be reset by clicking 'Reset' button which displays all theses submitted in the system.

If several search criteria are entered, theses containing any of the criteria are displayed to the user. If search results no results "There are no theses in the system" is displayed to the user.

On the bottom of the table the count of theses pertaining to the searched criteria is shown.

**Viewing single thesis details**
User may view the single thesis details by double clicking the table of the thesis. Thesis data is shown in read-only mode. User may return to the thesis list by pressing 'Back' button on the bottom of the thesis view window.

**Submitting a new thesis topic**

_Requires authorization_

Logged user can submit a new theses by clicking 'Create' button on top of the 'Thesis list'

After clicking the 'Create' button, user is requrested to enter the working title for the theses (mandatory) and description for the thesis (mandatory). User may also select relevant scientific areas for the thesis.

After completing the form, user may submit a new thesis topic by clicking 'Submit' button. User may also cancel the submission at any time by clicking 'Cancel' button. Both actions redirect the user to 'Thesis list'.

After succesfull thesis submission, new thesis is inserted to 'Thesis list'. Thesis supervisor and department along with the creation and modification dates are inserted automatically.

**Editing a submitted thesis**

_Requires authorization_

Supervisor may edit their self-submitted theses which have 'Available' status by clicking 'Edit'. System admin may edit any of the theses at any time.

**Checkout thesis for an author**

_Requires authorization_

Supervisor may checkout their self-submitted theses which have 'Available' status by clicking 'Edit' in 'Thesis list'. Edit mode offers a possibility to reserve the thesis topic for a student through 'Checkout for a stundet' button. Admin user may access checkout mode at any time for any thesis.

User is requested to enter thesis level and the author for the thesis. User may cancel or submit.

After successful checkout, the status of the thesis changes to 'Progressing' and reserved date is completed automatically.

**Clearing and editing checkout**

_Requires admin authorization_

Admin user may clear or edit student checkout by editing a submitted thesis and entering the checkout mode. Admin may change the level of the thesis or edit the author of the thesis. Admin may also clear the checkout completely by pressing 'Clear student checkout'

If student checkout is cleared, thesis status changes to 'Available' and author and level data is cleared for the thesis.

**Finalizing a thesis**

_Requires authorization_

Supervisor may finalize the self-submitted thesis by clicking 'Finalize' button. Finalization may be executed for theses which are in 'Progressing' state. Admin may finalize any thesis.

After thesis has been finalized, the status of the thesis is changed to 'Completed' and completion date is filled automatically.

**Return thesis from completed state**

_Requires admin authorization_

Admin user may return completed thesis back to 'Progressing' state. This may be done by accessing thesis in checkout mode and saving (no changes are necessary).

**Deleting a theses**

_Requires admin authorization_

Admin may delete theses which are in 'Available' state. Deletion of the theses in other states is prevented. Admin may delete theses in state other than 'Available' by returning the theses to 'Available' state.


## Master data management

This section requires admin authorization.

Admin may administer the following master data in the system
1. Users
2. Scientific areas
3. Departments

Master data editors may be accessed through 'Master data management' drop-down button by browsing the deeper levels of the application.

### Users

User management editors may be accessed by clicking 'Users' link the in the 'Master data management' drop-down button.

'User table' displays the following information regarding the users in the system
1. First name
2. Last name
3. Email address
4. Deparment
5. Admin
6. Created
7. Last modified
8. Action buttons

**Viewing a single user**
Single user record may be viewed by double clicking a user record in the user table

**Activating a registered user**
When user has registered the account will be inactive and user may not login to the system. By clicking 'Activate' button next to the inactive user, the user account will become active.

**Creating and editing a user**
User may be created by pressing 'Create' button on top of the 'User table'. An existing user may be edited by clicking 'Edit' button next to the user record.

User is requested to enter required data for the new user. All information is mandatory. In edit mode, user's first name, last name, and the department may be modified. User may be elevated with admin rights or the admin user may be disevelated to supervisor role in create and edit modes.

After editing or successful user creation entered information is displayed in the 'User table'

**Deleting a user**
User record which is not associated with submitted theses can be deleted from the system by clicking 'Delete' button next to a user record. If user record is associated with a thesis, user record may not be deleted and 'Delete' action is prevented.

### Scientific areas

Scientific areas management editor may be accessed by clicking 'Scientific areas' link the in the 'Master data management' drop-down button.

'Scientific areas table' displays the following information regarding the sciences in the system
1. Science (name of the scientific area)
2. Created

**Creating **
Scientific area may be created by pressing 'Create' button on top of the 'Scientific areas table'. 

User is requested to enter a name for a new scientific area. 

After successful science creation, entered information is displayed in the 'Scientific areas table'

**Deleting a scientific area**
Science which is not associated with submitted theses can be deleted from the system by clicking 'Delete' button next to a science record. If science record is associated with a thesis, science record may not be deleted and 'Delete' action is prevented.
