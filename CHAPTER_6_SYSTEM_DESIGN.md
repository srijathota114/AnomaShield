# Chapter 6  
# SYSTEM DESIGN

This chapter describes the system design of AnomaShield. It covers the overall architecture, the flow of data through the system (explained in terms of a data flow diagram), and the UML design in the form of use case and activity diagram explanations. The diagrams themselves can be drawn using the descriptions given here; the text focuses on what each part represents and how the pieces fit together.

---

## 6.1 System Architecture

AnomaShield is built as a three-tier web application. The three tiers are the presentation layer, the business logic layer, and the data layer. Each tier has a clear role and communicates with the others in a structured way.

**Presentation layer (front end)**  
This is what the user sees and interacts with in the browser. It consists of HTML pages (Django templates), CSS for styling (Bootstrap and custom styles), and JavaScript for client-side behaviour (e.g. file validation, tooltips, chart drawing with Chart.js). The presentation layer does not run the detection algorithms; it only sends user input (e.g. uploaded file, login credentials, settings) to the server and displays the responses (e.g. results page, charts, download link). All pages share a common base template that provides the navigation bar, footer, and loading of common scripts and styles. This keeps the look and behaviour consistent and makes it easy to add or change pages.

**Business logic layer (back end)**  
This layer runs on the server and contains the core functionality. It receives requests from the presentation layer and coordinates the work. Django handles routing: each URL is mapped to a view function. The view checks authentication, validates input (using forms), and then calls the right logic. For file upload, the view saves the file and the upload record, then calls the detection engine. The detection engine reads the file, detects numeric columns, splits data into chunks, runs the four detection methods (Z-Score, IQR, Isolation Forest, One-Class SVM), applies the consensus rule, and returns the results. The view then saves these results to the database and redirects the user to the results page. For other actions (e.g. view history, download clean data, change settings), the view queries the database or the configuration module and returns the appropriate response. So the business logic layer is responsible for authentication, file handling, detection, configuration, and all decision making. It sits between the user interface and the data.

**Data layer**  
This layer is responsible for storing and retrieving data. It has two parts. First, the database: Django’s ORM is used to define models (e.g. User, CSVUpload, DetectionResult). The database stores user accounts, upload metadata (filename, timestamps, row counts, status), and row-level detection results (which rows were flagged and by which methods). Second, the file storage: uploaded CSV and Excel files are saved on disk in a designated folder (e.g. `media/csv_files/`). The configuration file (e.g. `detector_config.json`) is also part of the data layer in the sense that it persists the detection parameters. The business logic layer reads from and writes to the data layer; the presentation layer does not access the database or files directly.

**Flow between layers**  
When a user uploads a file, the browser (presentation layer) sends the file to the server. The view (business logic) receives it, validates it, saves the file to disk (data layer), and creates an upload record in the database (data layer). Then the view calls the detection engine (business logic), which reads the file from disk (data layer) and reads parameters from the config file (data layer). The engine processes the data and returns results. The view saves the results to the database (data layer) and sends back a redirect to the results page. The browser then requests the results page; the view fetches data from the database (data layer) and renders the HTML (presentation layer). So data flows from user to presentation, then to business logic, then to data layer, and back through business logic to presentation and finally to the user. This separation makes it easier to change one layer (e.g. replace the front end or the database) without rewriting the whole system.

---

## 6.2 Data Flow Diagram Explanation

A data flow diagram (DFD) shows how data moves through the system. The explanation below describes what a Level 0 and Level 1 DFD would show for AnomaShield.

**Level 0 (context diagram)**  
At Level 0, the system is shown as a single process (a black box) with external entities around it. The external entities are the User and the System Administrator. The User sends data into the system: login credentials, file upload requests, CSV or Excel files, configuration changes (if they use the settings page), delete requests, and download requests. The system sends back to the User: authentication result (success or error), upload confirmation, detection results, charts and visualisations, the cleaned dataset (CSV file), error messages when something goes wrong, and upload history when the user visits the history page. The System Administrator may send admin credentials and configuration or user-management requests, and the system may send back admin authentication results, system statistics, or user management data. There are no data stores drawn at Level 0 because the focus is on the system as one unit and its inputs and outputs. This diagram helps to define the boundary of the system and who interacts with it.

**Level 1 (top-level processes and data stores)**  
At Level 1, the single process is broken into several processes and the main data stores appear. The processes are: (1) Authenticate User, (2) Manage File Upload, (3) Process Detection, (4) Manage Results, (5) Generate Visualisations, (6) Manage Configuration, and (7) Export Clean Data. The data stores are: D1 User Database (user accounts), D2 Upload Database (upload metadata), D3 Detection Results Database (row-level results), D4 Configuration File (detection parameters), and D5 File Storage (uploaded files).

The flow can be described as follows. The User sends login credentials to process 1.0 (Authenticate User), which queries D1 and returns an authentication result. For upload, the User sends a file and an upload request to process 2.0 (Manage File Upload). Process 2.0 stores the file in D5 and saves an upload record in D2, then sends a “process file” request to process 3.0 (Process Detection). Process 3.0 reads the file from D5 and the configuration from D4, runs the detection algorithms, and sends the detection results to process 4.0 (Manage Results). Process 4.0 saves the results in D3 and updates the upload record in D2, and sends result data to process 5.0 (Generate Visualisations) and to the User. Process 5.0 prepares chart data and sends charts to the User. When the User requests a download, the request goes to process 7.0 (Export Clean Data), which reads clean rows from D3, formats them as CSV, and sends the file to the User. When the User or Administrator views or changes settings, process 6.0 (Manage Configuration) reads from and writes to D4. So the DFD shows how data moves from the user and between the processes and data stores, without going into the internal steps of each process. A Level 2 DFD would break down one or more of these processes (e.g. Process 3.0) into smaller steps such as “Load Data,” “Detect Numeric Columns,” “Apply Z-Score,” “Apply IQR,” “Apply Isolation Forest,” “Apply One-Class SVM,” “Apply Consensus,” and “Aggregate Results.”

---

## 6.3 UML Design (Use Case and Activity Diagram Explanation)

**Use case diagram (explanation in text)**  
A use case diagram shows the actors and the use cases (actions) they can perform, and how use cases relate to each other.

*Actors:* There are two main actors. The first is the User (a registered user who uses the system to upload files and view results). The second is the System Administrator, who may manage the system or users via the admin interface or configuration.

*Use cases for the User:* The User can log in, register, view the home page, upload a file, view detection results, download clean data, view upload history, delete an upload, change detection settings (and optionally reset to defaults), view method details (e.g. which methods flagged each row), and log out. So the main use cases are: Login, Register, Upload File, View Results, Download Clean Data, View History, Delete Upload, Configure Settings, View Method Details, and Logout.

*Use cases for the System Administrator:* The administrator can access the admin panel (e.g. Django admin), manage users, and view system logs or statistics, depending on how the admin is set up.

*Relationships between use cases:* “Upload File” includes “Validate File” (validation is a necessary part of every upload). “View Results” can extend to “Download Clean Data” (the user may optionally download after viewing) and to “View Method Details” (the user may optionally see the per-method breakdown). “Configure Settings” can extend to “Reset to Defaults” (the user may optionally reset while on the settings page). These include and extend relationships are shown on the use case diagram as labelled arrows so that the reader understands which actions are mandatory parts of another action and which are optional extensions.

*How to read the diagram:* The system boundary is drawn as a rectangle. All use cases appear as ovals inside it. The User and System Administrator are shown as stick figures outside the rectangle. Lines connect each actor to the use cases they can perform. The diagram gives a high-level view of system functionality from the user’s perspective and is useful for explaining the scope of the system to stakeholders.

**Activity diagram (explanation in text)**  
An activity diagram shows the flow of activities (steps) and decisions from start to end. For AnomaShield, the main flow is the “upload and detect” workflow.

*Start:* The flow starts when the user initiates an action (e.g. opens the site or submits an upload).

*Authentication:* The first decision is whether the user is logged in. If not, the activity “Show Login Page” is performed, then “User Enters Credentials” and “Validate Credentials.” If validation fails, an error is shown and the flow may return to the login page. If it succeeds, or if the user was already logged in, the next activity is “Show Home Page.”

*Upload and validation:* The user selects a file and submits. The activity “Validate File Format” checks that the file is CSV or Excel. If not, a format error is shown. Then “Validate File Size” checks that the file is under the size limit. If not, a size error is shown. If both pass, the activities “Save File to Storage” and “Create Upload Record” are performed.

*Detection:* The system loads the configuration, reads the file, and performs “Detect Numeric Columns.” If no numeric columns are found, an error is set and the upload is marked as failed (end of flow for that upload). If numeric columns exist, the activity “Split Data into Chunks” is performed. Then a loop runs for each chunk: for the current chunk, the activities “Apply Z-Score Detection,” “Apply IQR Detection,” “Apply Isolation Forest Detection,” and “Apply One-Class SVM Detection” are performed, then “Collect Method Results” and “Apply Consensus Threshold.” After all chunks are processed, the activities “Aggregate Results,” “Calculate Statistics,” and “Create Row-Level Results” are performed. If any step fails, the upload is marked as failed; otherwise “Update Upload Statistics” and “Save Detection Results” are performed, and the upload is marked as processed.

*Results and user actions:* The user is redirected to the results page. The system “Prepare Chart Data,” “Query Results,” “Render Results Page,” and “Display Charts.” The user sees the results. Then the flow can branch based on what the user does next: view method details, download clean data, view history, upload another file, or log out. Each of these is an activity or a path that may lead to another page or back to an earlier step (e.g. upload another file returns to the upload step).

*End:* The flow ends when the user logs out or when an error state is reached (e.g. processing failed). In the diagram, end states are usually drawn as a filled circle inside a larger circle.

*How to read the diagram:* Activities are shown as rounded rectangles, decisions as diamonds (with “yes” and “no” or other labels on the outgoing arrows), and the flow direction with arrows. The activity diagram is useful for understanding the order of steps, where decisions are made, and where the flow can split or loop. It complements the DFD by showing the control flow and sequence inside the system rather than only the movement of data.

---

Together, the system architecture, the data flow diagram explanation, and the use case and activity diagram explanations describe how AnomaShield is structured and how data and control move through it. These descriptions can be used to draw the actual diagrams for the project report or presentation.
