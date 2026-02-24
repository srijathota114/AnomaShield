# Chapter 5  
# PROJECT DESCRIPTION

This chapter describes how AnomaShield is organised and how it works. It is divided into three parts: the main modules of the system, the backend and admin side, and the frontend that the user sees in the browser.

---

## 5.1 Modules

The application is organised into the following logical modules. Each module has a clear responsibility and works with the others to complete the full workflow.

**Authentication module**  
This module handles user registration, login, and logout. When a user registers, the system checks that the username and email are not already taken and that the two password fields match. The password is stored in a hashed form. On login, the username and password are checked against the database; if they match, the user is marked as logged in and is redirected to the home page. Only logged-in users can access the upload, results, history, and settings pages. The authentication module uses Django’s built-in User model and session management.

**File upload and validation module**  
This module is responsible for accepting the file from the user and checking that it is allowed. The system accepts CSV and Excel files (.csv, .xlsx, .xls) up to 10 MB. The form checks the file extension and size on the server. If validation passes, the file is saved in a dedicated folder (e.g. `media/csv_files/`) and a new record is created in the database to store the filename, upload time, and initial status. The user can also tick an option to mark the dataset as “already cleaned,” which enables lenient mode for detection.

**Detection engine module**  
This is the core processing module. It reads the uploaded file with pandas, detects which columns are numeric, and splits the data into chunks (default three). For each chunk it runs four detection methods: Z-Score, IQR, Isolation Forest, and One-Class SVM. Each method returns the row indices it considers anomalous. The engine then applies the consensus rule: a row is marked as poisoned only if at least two methods flagged it. The number of methods required (consensus threshold) is configurable. After all chunks are processed, the results are merged and summary statistics (total rows, flagged rows, clean rows, detection rate, per-method counts) are computed. The engine uses a configuration module to read thresholds and parameters (e.g. Z-Score threshold, IQR multiplier, contamination, nu) so that behaviour can be changed without editing code.

**Configuration module**  
This module loads and saves detection parameters from a JSON file (e.g. `detector_config.json`). It stores the Z-Score threshold, IQR multiplier, consensus threshold, number of chunks, and the contamination/nu values for small, medium, and large datasets. It also provides helper functions that return the right contamination or nu value based on the number of rows in the dataset. The settings page in the web interface reads and updates this configuration so that users can tune the system without touching the config file directly.

**Results storage and retrieval module**  
After the detection engine finishes, the summary statistics are written to the upload record in the database. For each row in the dataset, a result record is created that stores the row index, whether the row is flagged overall, which of the four methods flagged it, and a JSON copy of the row data. This allows the results page to show detailed tables (e.g. “View Data” for each row) and to know which methods agreed. When the user requests the results page or the clean-data download, this module is used to query the database and return the relevant records.

**Download module**  
This module generates the cleaned dataset. It fetches all result records for the upload that are not flagged, orders them by row index, and builds a CSV file from the stored row data. The file is sent to the browser with the appropriate headers so that the user gets a downloadable CSV containing only the rows that were not marked as poisoned.

**History and delete module**  
The history page lists all uploads for the user (or all uploads if the system does not filter by user), showing filename, date, size, status, and basic counts. The user can open a past result or delete an upload. On delete, the system removes the file from disk and deletes the upload record and all associated result records from the database.

Together, these modules cover the full path from login and upload to detection, storage, display, download, and management of past uploads.

---

## 5.2 Backend and Admin Dashboard

**Backend (Django application)**  
The backend is implemented in Python using the Django framework. The main application lives inside the `detector` app. Django handles incoming HTTP requests, matches them to URLs, and calls the right view function for each page.

- **URLs:** The `urls.py` file defines the routes. For example, the home page is at `/`, login at `/login/`, results at `/results/<id>/`, history at `/history/`, settings at `/settings/`, and so on. Each route is linked to a view function.

- **Views:** The `views.py` file contains the view functions. Each function receives the request, performs the required logic (e.g. validate form, call detection engine, query database), and returns an HTTP response. For most pages this response is rendered HTML: the view passes data to a template and returns the resulting page. For the download page, the response is a CSV file. Views use the models to read and write the database and call the detection engine and configuration module where needed.

- **Models:** The `models.py` file defines the database tables. The `CSVUpload` model stores each upload (file reference, filename, timestamps, row counts, per-method counts, processing status, error message, and whether lenient mode was used). The `DetectionResult` model stores row-level results (upload reference, row index, overall flag, four method flags, and row data as JSON). Django’s ORM is used to create, update, and query these records.

- **Forms:** The `forms.py` file defines the upload form (file field and “already cleaned” checkbox) and the settings form (all configurable parameters). Forms handle validation and error messages so that invalid input does not reach the detection engine or the config file.

- **Detection engine:** The `detection_engine.py` file contains the `DataPoisonDetector` class and the logic for numeric column detection, chunking, the four detection methods, consensus, and aggregation. It is called from the home view after a file is uploaded and saved.

- **Configuration:** The `config.py` file defines the `DetectionConfig` class that reads and writes the JSON config file and provides the adaptive parameter helpers.

**Admin dashboard**  
Django provides a built-in admin site that can be used to manage data. By default it is available at `/admin/`. If the `CSVUpload` and `DetectionResult` models are registered in `admin.py`, a superuser can log in to the admin and view, search, or delete uploads and results from there. This is useful for support and maintenance (e.g. inspecting failed uploads or cleaning old data). The main user-facing “dashboard” is the normal web interface: Home, Results, History, and Settings. The Django admin acts as an optional backend dashboard for administrators rather than for end users.

**Database and storage**  
SQLite is used by default; the database file is stored in the project directory. Uploaded files are stored in the `media` folder. For production, the database can be switched to PostgreSQL or MySQL, and file storage can be adjusted if needed (e.g. cloud storage). The application code does not assume a particular database or storage backend beyond what Django supports.

---

## 5.3 Frontend

The frontend is what the user sees and interacts with in the browser. It is built with HTML templates, CSS, and JavaScript.

**Base template and layout**  
All pages extend a base template (`base.html`). The base template defines the overall layout: a navigation bar at the top, a main content area in the middle, and a footer at the bottom. The navbar shows the application name (AnomaShield) and links to Home, History, Settings, and either Login/Register or Logout depending on whether the user is logged in. The main content area is a block that each page fills with its own content. The footer shows a short line of text (e.g. “AnomaShield - Data Poison Detection | Built with Django & Machine Learning”). The base template also loads Bootstrap CSS, Font Awesome icons, Chart.js, and the project’s custom CSS file. This keeps the look and behaviour consistent across all pages.

**Pages and templates**  
Each main feature has its own template inside `templates/detector/`:

- **Login and Register:** Simple forms with fields for username, password (and email, password confirmation for register). Error and success messages are shown at the top. After successful login or register, the user is redirected to the home page.

- **Home:** The main upload page. It shows a heading, a short description, and a file upload form. The user can select a file (CSV or Excel) and optionally check “Already Cleaned Dataset” for lenient mode. After submitting, the file is validated and processed; the user is then redirected to the results page for that upload. Recent uploads may be listed on the same page depending on implementation.

- **Results:** This page shows the outcome of detection. At the top there are summary cards: total rows, flagged rows, clean rows, and detection rate. Below that, two charts are drawn with Chart.js: one bar chart comparing how many rows each method (Z-Score, IQR, Isolation Forest, One-Class SVM) flagged, and one pie chart showing the split between clean and flagged rows. Further down, there are tabs: one for flagged rows and one for clean rows. Each row can be expanded to “View Data” and see the actual values. A “Download Clean Data” button lets the user download a CSV of non-flagged rows. The page can also have a toggle between “Basic” and “Advanced” view to show or hide extra details (e.g. method breakdown).

- **History:** A table lists past uploads with filename, date, file size, status (e.g. Processed/Error), and counts (e.g. flagged/total). The user can open a result or delete an upload. Summary cards may show total uploads, processed count, pending count, and error count.

- **Settings:** A form displays the current detection parameters (Z-Score threshold, IQR multiplier, consensus threshold, number of chunks, and the contamination/nu values for small, medium, and large datasets). The user can change any value and save. Optionally there is a “Reset to defaults” action. After saving, a success message is shown and future uploads use the new settings.

**Styling and behaviour**  
Bootstrap 5 is used for the grid, cards, buttons, forms, navbar, and alerts. This makes the interface responsive: it adapts to different screen sizes. The project’s `style.css` adds any extra styling. JavaScript is used for small improvements such as tooltips, file type/size checks before submit, and toggling between Basic and Advanced views on the results page. Chart.js is used only on the results page to draw the bar and pie charts from data passed by the backend (e.g. in a JSON script tag or in the template context).

**Flow from the user’s point of view**  
The user opens the site, logs in (or registers), and lands on the home page. They choose a CSV or Excel file and optionally enable lenient mode, then click the upload/analyse button. After a short wait, they are taken to the results page where they see the summary, charts, and the list of flagged and clean rows. They can download the cleaned CSV from there. From the navbar they can go to History to see past uploads or to Settings to change parameters. The frontend does not perform detection itself; it only sends the file and request to the server and displays what the backend returns. All processing happens on the server (backend), and the frontend is responsible for presenting the results clearly and making the application easy to use.
